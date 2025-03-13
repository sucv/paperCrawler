import os
import re
from urllib.parse import urlparse
import feedparser
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from scrapy.exceptions import DropItem

OPENALEX_URL = "https://api.openalex.org/works"

def deduplicate_urls(urls):
    unique = {}
    for url in urls:
        parsed = urlparse(url)
        key = parsed.netloc + parsed.path
        # Replace a http URL if a duplicate https exists.
        if key not in unique or (url.startswith("https") and unique[key].startswith("http")):
            unique[key] = url
    return list(unique.values())

# ------------- BooleanSearchParser code (unchanged) -------------
from pyparsing import (
    Word,
    alphanums,
    CaselessKeyword,
    Group,
    Forward,
    Suppress,
    OneOrMore,
    one_of,
    ParserElement,
)

ParserElement.enablePackrat()

alphabet_ranges = [
    [int("0400", 16), int("04FF", 16)],  # CYRILIC
    [int("0600", 16), int("07FF", 16)],  # ARABIC
    [int("0E00", 16), int("0E7F", 16)],  # THAI
    [int("3040", 16), int("30FF", 16)],  # JAPANESE
    [int("3200", 16), int("32FF", 16)],  # Enclosed CJK Letters and Months
    [int("4E00", 16), int("9FFF", 16)],  # CHINESE
    [int("1100", 16), int("11FF", 16)],  # KOREAN
    [int("3130", 16), int("318F", 16)],
    [int("A960", 16), int("A97F", 16)],
    [int("AC00", 16), int("D7AF", 16)],
    [int("D7B0", 16), int("D7FF", 16)],
    [int("FF00", 16), int("FFEF", 16)],  # Halfwidth and Fullwidth Forms
]


class BooleanSearchParser:
    def __init__(self):
        self._methods = {
            "and": self.evaluateAnd,
            "or": self.evaluateOr,
            "not": self.evaluateNot,
            "parenthesis": self.evaluateParenthesis,
            "quotes": self.evaluateQuotes,
            "word": self.evaluateWord,  # if no wildcards
            "wordwildcardprefix": self.evaluateWordWildcardPrefix,
            "wordwildcardsufix": self.evaluateWordWildcardSufix,
        }
        self._parser = self.parser()
        self.text = ""
        self.words = []

    def parser(self):
        operatorOr = Forward()

        alphabet = alphanums
        for lo, hi in alphabet_ranges:
            alphabet += "".join(chr(c) for c in range(lo, hi + 1) if not chr(c).isspace())

        operatorWord = Group(Word(alphabet + "*")).set_results_name("word*")

        operatorQuotesContent = Forward()
        operatorQuotesContent << ((operatorWord + operatorQuotesContent) | operatorWord)

        operatorQuotes = (
            Group(Suppress('"') + operatorQuotesContent + Suppress('"')).set_results_name("quotes")
            | operatorWord
        )

        operatorParenthesis = (
            Group(Suppress("(") + operatorOr + Suppress(")")).set_results_name("parenthesis")
            | operatorQuotes
        )

        operatorNot = Forward()
        operatorNot << (
            Group(Suppress(CaselessKeyword("not")) + operatorNot).set_results_name("not")
            | operatorParenthesis
        )

        operatorAnd = Forward()
        operatorAnd << (
            Group(operatorNot + Suppress(CaselessKeyword("and")) + operatorAnd).set_results_name("and")
            # implicit AND if operator is missing
            | Group(operatorNot + OneOrMore(~one_of("and or") + operatorAnd)).set_results_name("and")
            | operatorNot
        )

        operatorOr << (
            Group(operatorAnd + Suppress(CaselessKeyword("or")) + operatorOr).set_results_name("or")
            | operatorAnd
        )

        return operatorOr.parse_string

    def evaluateAnd(self, argument):
        overall_found = True
        overall_tokens = set()
        for arg in argument:
            found, tokens = self.evaluate(arg)
            if not found:
                return (False, set())
            overall_found = overall_found and found
            overall_tokens |= tokens
        return (overall_found, overall_tokens)

    def evaluateOr(self, argument):
        any_found = False
        union_tokens = set()
        for arg in argument:
            found, tokens = self.evaluate(arg)
            if found:
                any_found = True
                union_tokens |= tokens
        return (any_found, union_tokens if any_found else set())

    def evaluateNot(self, argument):
        found, tokens = self.evaluate(argument[0])
        if found:
            return (False, set())
        else:
            return (True, set())

    def evaluateParenthesis(self, argument):
        return self.evaluate(argument[0])

    def evaluateQuotes(self, argument):
        phrase = " ".join(tok[0] for tok in argument)
        if phrase in self.text:
            return (True, {phrase})
        else:
            return (False, set())

    def evaluateWord(self, argument):
        raw_word = argument[0]
        wildcard_count = raw_word.count("*")
        if wildcard_count > 0:
            # Single '*' at start -> endswith
            if wildcard_count == 1 and raw_word.startswith("*"):
                return self.GetWordWildcard(raw_word[1:], method="endswith")
            # Single '*' at end -> startswith
            if wildcard_count == 1 and raw_word.endswith("*"):
                return self.GetWordWildcard(raw_word[:-1], method="startswith")
            # Otherwise -> treat as regex
            _regex = raw_word.replace("*", ".*")
            matched = set()
            for w in self.words:
                if re.search(_regex, w):
                    matched.add(w)
            return ((len(matched) > 0), matched)
        # no wildcard
        return self.GetWord(raw_word)

    def evaluateWordWildcardPrefix(self, argument):
        return self.GetWordWildcard(argument[0], method="endswith")

    def evaluateWordWildcardSufix(self, argument):
        return self.GetWordWildcard(argument[0], method="startswith")

    def evaluate(self, argument):
        return self._methods[argument.getName()](argument)

    def Parse(self, query):
        parsed = self._parser(query)[0]
        return self.evaluate(parsed)

    def GetWord(self, word):
        if word in self.words:
            return (True, {word})
        return (False, set())

    def GetWordWildcard(self, word, method="startswith"):
        matched = set()
        for w in self.words:
            if getattr(w, method)(word):
                matched.add(w)
        return ((len(matched) > 0), matched)

    def _split_words(self, text):
        words = []
        r = re.compile(r"[\s{}]+".format(re.escape("!\"$%&'()*+,-/:;<=>?[\\]^`{|}~")))
        _words = r.split(text)
        for _w in _words:
            if "." in _w and not _w.startswith("#") and not _w.startswith("@"):
                words.extend(_w.split("."))
            else:
                words.append(_w)
        return [w for w in words if w]

    def match_with_tokens(self, text, expr):
        self.text = text
        self.words = self._split_words(text)
        return self.Parse(expr)

    def match(self, text, expr):
        found, _ = self.match_with_tokens(text, expr)
        return found


# ------------------------------- NEW Code / Changes -------------------------------
import time
import threading


class CrawlPipeline:
    # Rate-limiting attributes:
    rate_limit_lock = threading.Lock()
    last_request_time = 0
    COOLDOWN_SECONDS = 1  # Wait 1s between external requests

    def process_item(self, item, spider):
        parser = BooleanSearchParser()  # Assuming this is defined elsewhere
        abstract = item.get("abstract", "")
        title = item.get("title", "")
        clean_title = re.sub(r'\W+', ' ', title).lower()

        # Parse queries
        if spider.queries == "":
            found = True
            matched_tokens = set()
        else:
            found, matched_tokens = parser.match_with_tokens(text=clean_title, expr=spider.queries)

        if not found:
            raise DropItem("Missing keyword in %s" % item)

        # Initialize variables for storing results
        oa_urls = []
        citation_count = -1
        paper_doi = ""
        paper_categories = ""
        paper_concepts = ""

        # Only call external API if the spider indicates so
        if spider.crossref:
            params = {"search": clean_title}

            # --- Rate-limited API request ---
            with self.rate_limit_lock:
                now = time.time()
                elapsed = now - self.last_request_time
                if elapsed < self.COOLDOWN_SECONDS:
                    time.sleep(self.COOLDOWN_SECONDS - elapsed)
                response = requests.get(OPENALEX_URL, params=params)
                self.last_request_time = time.time()
            # --- End rate-limited block ---

            if response.status_code == 200:
                data = response.json()
                if data.get("results"):
                    # Use top 5 papers (as per your current slice)
                    top_papers = {i: paper for i, paper in enumerate(data["results"][:5])}
                    # Map each index to its title for fuzzy matching
                    titles_dict = {idx: paper["title"] for idx, paper in top_papers.items()}

                    # Perform fuzzy matching; each tuple is (index, score, title)
                    matches = process.extract(title, titles_dict, scorer=fuzz.ratio)
                    relevant_matches = [match for match in matches if match[1] >= 90]

                    if relevant_matches:
                        highest_cited = -1

                        # Traverse through the relevant matches
                        for matched_title, score, idx in relevant_matches:
                            # Use the index (idx) to retrieve the paper from top_papers
                            paper = top_papers[idx]

                            # If the paper is open access and has an OA URL, process it
                            if paper.get("open_access", {}).get("is_oa", False):
                                oa_url = paper.get("open_access", {}).get("oa_url")
                                if oa_url:
                                    if "arxiv.org/abs/" in oa_url:
                                        # Convert the arXiv abstract URL to a PDF URL
                                        oa_url = oa_url.replace("abs", "pdf")
                                        arxiv_id = oa_url.split("/")[-1]
                                        api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
                                        # If no abstract is present, try retrieving it from arXiv
                                        if abstract == "":
                                            feed = feedparser.parse(api_url)
                                            if feed.entries:
                                                abstract = feed.entries[0].summary.replace("\n", " ")
                                    oa_urls.append(oa_url)

                            # Track the highest cited_by_count among the matched papers
                            if paper.get("cited_by_count", 0) > highest_cited:
                                highest_cited = paper["cited_by_count"]

                        citation_count = highest_cited

                        # Get doi, categories, and concepts from the first relevant match
                        first_match_idx = relevant_matches[0][2]
                        first_paper = top_papers[first_match_idx]
                        paper_doi = first_paper.get("doi", "")
                        paper_categories = ",".join(
                            topic['display_name'] for topic in first_paper.get("topics", [])
                        )
                        paper_concepts = ",".join(
                            concept['display_name'] for concept in first_paper.get("concepts", [])
                        )

                        # Set pdf_url if not already set
                        oa_urls_str = ",".join(deduplicate_urls(oa_urls))

                        if not item.get('pdf_url'):
                            item['pdf_url'] = oa_urls_str

        # Update the item with the retrieved metadata
        item["citation_count"] = citation_count
        item["matched_queries"] = ",".join(list(matched_tokens))
        item["categories"] = paper_categories
        item["concepts"] = paper_concepts
        item["doi"] = paper_doi
        item["abstract"] = abstract

        # Extract a code URL from the abstract if present
        if abstract:
            code_url_matches = re.findall(r'(https?://\S+)', abstract)
            code_url = code_url_matches[0].rstrip(".") if code_url_matches else ""
            item["code_url"] = code_url

        if spider.download_pdf > -1 and item.get('pdf_url') and item.get('citation_count') >= spider.download_pdf:
            pdf_urls = item.get("pdf_url").split(",")
            is_downloaded = False
            for pdf_url in pdf_urls:

                if is_downloaded:
                    continue

                response = requests.get(pdf_url)
                if response.status_code == 200:
                    pdf_path = os.path.join(spider.pdf_dir, "_".join(clean_title.strip().split(" ")) + ".pdf")
                    os.makedirs(spider.pdf_dir, exist_ok=True)
                    with open(pdf_path, "wb") as file:
                        file.write(response.content)

        return item
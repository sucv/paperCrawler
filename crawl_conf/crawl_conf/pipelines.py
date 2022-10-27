# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

# For fuzzy match. Sometimes, the title have slight difference between different sources.
from fuzzywuzzy import fuzz

# For regular expression
import re


class CrawlConfPipeline:

    def process_item(self, item, spider):
        # Process the item one at a time.
        abstract = item["abstract"]
        title = item["title"]
        clean_title = re.sub(r'\W+', ' ', title).lower()

        # replace any special characters from the abstract with a space.
        clean_abstract = re.sub(r'\W+\-', ' ', abstract).lower()
        # clean_abstract = re.sub('[^a-zA-Z.-]+', ' ', abstract)
        # Stem each tokens so that different time tensions and plurals are restored.
        clean_abstract_token = clean_abstract.split(" ")
        citation_count = -1

        matched_keys = [keyword for keyword in spider.wanted_keyword_in_title if keyword in clean_abstract_token]

        # If the queries are found in the abstract, then return the item, otherwise drop it.
        if len(matched_keys):

            # Try to get the code url. The code extract any url from the abstract and take them as the code url.
            item["code_url"] = re.findall(r'(https?://\S+)', abstract)

            if hasattr(spider, "count_citation_from_3rd_party_api"):

                # Get the top 3 papers that are most relevant to the query paper.
                # This can be time-consuming. The api provider may even kill the process if too many concurrent requests sent.
                paper_info_list = spider.sch.search_paper(clean_title, limit=3)

                # Get the citation count from SemanticScholar.
                ratio_list = []
                for paper_info in paper_info_list:
                    clean_paper_info_title = re.sub(r'\W+', ' ', paper_info.title).lower()
                    ratio_list.append(fuzz.ratio(clean_paper_info_title, clean_title))
                    if clean_paper_info_title == clean_title:
                        citation_count = paper_info.citationCount
                        break

                # If the paper title does not match the query, then use the most similar one according to the fuzzy matching
                if citation_count == -1:
                    max_ratio = max(ratio_list)
                    idx_max = ratio_list.index(max_ratio)
                    paper_info = paper_info_list[idx_max]
                    citation_count = paper_info.citationCount


            item["citation_count"] = citation_count
            item["matched_keys"] = matched_keys
            return item
        else:
            raise DropItem("Missing keyword in %s" % item)
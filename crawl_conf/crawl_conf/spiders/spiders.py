import scrapy
import re

# To remove consecutive space and special formatting characters like \n
import inspect

# The database to obtain the citation count
from semanticscholar import SemanticScholar

from nltk.stem.porter import PorterStemmer

from ..items import Paper


import scrapy
import re

# To remove consecutive space and special formatting characters like \n
import inspect

from semanticscholar import SemanticScholar

# from nltk.stem.porter import PorterStemmer

# We import the Paper item we defined in `items.py`.
from ..items import Paper

import json

class BaseSpider(scrapy.Spider):

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)

        # Save the conference and keyword arguments.
        years = kwargs.get('years').split(',')
        keys = kwargs.get('keys').split(',')
        cc = kwargs.get('cc')

        # Remove repeated input
        wanted_conf = []
        for year in years:
            if year not in wanted_conf:
                wanted_conf.append(self.name.upper() + year)
        self.wanted_conf = wanted_conf

        self.wanted_keyword_in_title = [x for x in keys]

        self.sch = SemanticScholar()
        # self.stemmer = PorterStemmer()

        # If counting the citations
        if cc:
            self.count_citation_from_3rd_party_api = 1
            # If using 3rd party api, then limit the maximum request rate to 10sec/request.
            # So that the API may not kill your process due to  exceeding requests.
            self.download_delay = 10

    def parse_paper(self, response):
    	# Deliver the scraped item to `pipelines.py`.
        paper = Paper()

        conf, title, pdf_url, clean_title, authors, abstract = self.extract_data(response)

        paper["conf"] = conf
        paper["title"] = title
        paper["pdf_url"] = pdf_url
        paper["clean_title"] = clean_title
        paper["authors"] = authors
        paper["abstract"] = abstract

        yield paper


class CvprScrapySpider(BaseSpider):
	# The name differentiate this crawler class against others. Try to
	# use unique name for each crawler class.

    name = 'cvpr'

    # Where to start the crawling.
    start_urls = [
        "https://openaccess.thecvf.com/menu",
    ]

    def parse(self, response):
        # response contains all the data scraped from the start_url, including the html source code.

        # Here we loop over the target conferences, which are CVPRs in different years.
        # We manually define the target url according to the homework we did on the target website.
        # Then, we send a request to the new target url, and call another method to process it.
        for conf in self.wanted_conf:
            url = response.url.split("menu")[0] + conf.upper()

            # For conferences in 2018 onward, the html elements contain the list of days, instead of the paper list directly
            if conf[4:] >= "2018":

                # Navigate to the day list
                yield scrapy.Request(url, callback=self.parse_day)
            else:

                # Navigate to the paper list
                yield scrapy.Request(url, callback=self.parse_paper_list)

    def parse_day(self, response):
        # Now we navigate to the Day page.
        # Get all the days listed there using the xpath.
        # extract() generates a list of all matched elements.
        day_url_list = response.xpath("//div[@id='content']/dl/dd/a/@href").extract()

        # Traverse every day
        for day_url in day_url_list:

            # Exclude the Day-aLL hyperlink to avoid redundancy.
            if "day=all" in day_url:
                continue

            # For each day, we once again manually generate the new url, visit it,
            # and call yet another method to process it.
            url = response.urljoin(day_url)
            yield scrapy.Request(url, callback=self.parse_paper_list)

    def parse_paper_list(self, response):
        # Now we have all the papers.
        paper_url_list = response.xpath("//div[@id='content']/dl/dt[@class='ptitle']/a/@href").extract()

        # We loop all the paper url, visit them, and call the `parse_paper` method to process.
        for paper_url in paper_url_list:
            url = response.urljoin(paper_url)

            # for each paper, navigate to its detail page
            yield scrapy.Request(url, callback=self.parse_paper)

    @staticmethod
    def extract_data(response):
        # This function specifies how to extract the relevance from the paper detail page of the OpenCVF website.
        # Use the xpath with trial-and-error to rid of any exceptions.

        # Correct the bug caused by slight difference on the elements
        conf = response.url.split("/")[4]
        if conf == "html":
            conf = "".join(response.url.split("/")[3].split("_")[1:]).upper()

        title = inspect.cleandoc(response.xpath("//div[@id='papertitle']/text()").get())
        pdf_url = response.urljoin(response.xpath("//div[@id='content']/dl/dd/a[1]/@href").get())
        clean_title = re.sub(r'\W+', ' ', title).lower()
        authors = inspect.cleandoc(response.xpath("//div[@id='authors']/b/i/text()").get())
        abstract = inspect.cleandoc(response.xpath("//div[@id='abstract']/text()").get())

        return conf, title, pdf_url, clean_title, authors, abstract


class IccvScrapySpider(CvprScrapySpider):
    name = 'iccv'
    start_urls = [
        "https://openaccess.thecvf.com/menu",
    ]


class EccvScrapySpider(CvprScrapySpider):
    name = 'eccv'
    start_urls = [
        "https://www.ecva.net/papers.php",
    ]

    def parse(self, response):

        for conf in self.wanted_conf:
            conf_text = " ".join(["\n\t\t" + conf[:4].upper(), conf[4:], "Papers\n\t"])
            paper_url_list = response.xpath(
                "//div[@class='py-6 container']/button[text()='" + conf_text + "']/following-sibling::div[position()=1]/div[@id='content']/dl/dt/a/@href").extract()

            for paper_url in paper_url_list:
                url = response.urljoin(paper_url)
                yield scrapy.Request(url, callback=self.parse_paper)


class NipsScrapySpider(BaseSpider):
    name = 'nips'
    start_urls = [
        "https://papers.nips.cc/",
    ]

    def parse(self, response):

        for conf in self.wanted_conf:
            conf_url = "/paper/" + conf[4:]
            url = response.urljoin(conf_url)

            yield scrapy.Request(url, callback=self.parse_paper_list)

    def parse_paper_list(self, response):
        paper_url_list = response.xpath("//div[@class='container-fluid']/div[@class='col']/ul/li/a/@href").extract()

        for paper_url in paper_url_list:
            url = response.urljoin(paper_url)
            yield scrapy.Request(url, callback=self.parse_paper)

    @staticmethod
    def extract_data(response):

        conf = "NIPS" + response.xpath("//div[@class='col']/p/a/@href").get().split("/")[2]

        title = inspect.cleandoc(response.xpath("//div[@class='col']/h4/text()").get())
        clean_title = re.sub(r'\W+', ' ', title).lower()
        authors = inspect.cleandoc(response.xpath("//div[@class='col']/p[position()=2]/i/text()").get())

        try:
            abstract = inspect.cleandoc(response.xpath("//div[@class='col']/p[position()=4]/text()").get())
        except:
            abstract = inspect.cleandoc(response.xpath(
                "//div[@class='col']/p[position()=3]/text() | //div[@class='col']/p[position()=3]/span/text()").get())

        pdf_url = response.urljoin(response.xpath("//div[@class='col']/div/a[text()='Paper']/@href").get())

        return conf, title, pdf_url, clean_title, authors, abstract


class AaaiScrapySpider(BaseSpider):
    name = 'aaai'
    start_urls = [
        "https://aaai.org/Library/AAAI/aaai-library.php",
    ]

    def parse(self, response):
        for conf in self.wanted_conf:
            conf_url = conf[:4].lower() + conf[6:] + "contents.php"
            url = response.urljoin(conf_url)
            yield scrapy.Request(url, callback=self.parse_track_list)

    def parse_track_list(self, response):
        track_url_list = response.xpath("//div[@class='content']/ul/li/a/@href").extract()

        for track_url in track_url_list:
            url = response.urljoin(track_url)
            yield scrapy.Request(url, callback=self.parse_paper_list)

    def parse_paper_list(self, response):
        paper_url_list = response.xpath(
            "//div[@id='content']/div[@id='right']/div[@id='box6']/div[@class='content']/p/a[1]/@href").extract()

        for paper_url in paper_url_list:
            url = response.urljoin(paper_url)
            yield scrapy.Request(url, callback=self.parse_paper)

    @staticmethod
    def extract_data(response):

        conf = "AAAI" + response.xpath("//section[@class='sub_item']/div[@class='value']/span/text()").get().split("-")[
            0]

        title = inspect.cleandoc(response.xpath("//article/h1/text()").get())
        clean_title = re.sub(r'\W+', ' ', title).lower()
        authors = inspect.cleandoc(
            ",".join(response.xpath("//ul[@class='authors']/li/span[@class='name']/text()").extract()).replace("\t",
                                                                                                               "").replace(
                "\n", ""))
        abstract = inspect.cleandoc("".join(response.xpath(
            "//section[@class='item abstract']/p/text() | //section[@class='item abstract']/text()").extract()).replace(
            "\t", "").replace("\n", ""))

        pdf_url = response.xpath("//div[@class='entry_details']/div[@class='item galleys']/ul/li/a/@href").get()

        return conf, title, pdf_url, clean_title, authors, abstract


class IjcaiScrapySpider(BaseSpider):
    name = 'ijcai'
    start_urls = [
        "https://www.ijcai.org/past_proceedings",
    ]

    def parse(self, response):
        for conf_url in self.wanted_conf:
            url = "https://www.ijcai.org/proceedings/" + conf_url[5:]
            yield scrapy.Request(url, callback=self.parse_paper_list)

    def parse_paper_list(self, response):
        paper_url_list = response.xpath("//div[@class='paper_wrapper']/div[@class='details']/a[2]/@href").extract()

        for paper_url in paper_url_list:
            url = response.urljoin(paper_url)
            yield scrapy.Request(url, callback=self.parse_paper)

    @staticmethod
    def extract_data(response):

        conf = response.xpath("//div[@class='row'][2]/div/div[2]/a/@href").get().split("/")[4].replace(".", "").upper()

        title = inspect.cleandoc(response.xpath("//div[@class='row'][1]/div/h1/text()").get())
        clean_title = re.sub(r'\W+', ' ', title).lower()
        authors = inspect.cleandoc(response.xpath("//div[@class='row'][1]/div/h2/text()").get())
        abstract = inspect.cleandoc(response.xpath("//div[@class='row'][3]/div/text()").get())
        pdf_url = response.xpath("//div[@class='btn-container']/a/@href").get()

        return conf, title, pdf_url, clean_title, authors, abstract


class IclrScrapySpider(BaseSpider):
    name = 'iclr'
    start_urls = [
        "https://iclr.cc/",
    ]

    def parse(self, response):
        for conf in self.wanted_conf:
            url = response.urljoin("Conferences/" + conf[4:] + "/Schedule?type=Poster")
            yield scrapy.Request(url, callback=self.parse_paper_list)

    def parse_paper_list(self, response):
        paper_id_list = response.xpath(
            "//div[@id='base-main-content']/div[2]/div[3 < position()]/div[@class='maincard narrower poster']/@id").extract()

        for paper_id in paper_id_list:
            url = response.url.split("type=Poster")[0] + "showEvent=" + paper_id.split("_")[1]

            yield scrapy.Request(url, callback=self.parse_paper)

    @staticmethod
    def extract_data(response):

        conf = "".join(response.xpath(
            "//div[@id='sidebar']/div/span/b/text() | //div[@id='sidebar']/div/span/b/span/text()").extract()).replace(
            " | ", "")
        title = inspect.cleandoc(
            response.xpath("//div[@id='base-main-content']/div[2]/div[@id=$pid]/div[@class='maincardBody']/text()",
                           pid="maincard_" + response.url.split("=")[1]).get())
        clean_title = re.sub(r'\W+', ' ', title).lower()
        authors = inspect.cleandoc(
            ",".join(response.xpath("//div[@id='base-main-content']/div[2]/button/text()").extract())).replace("»", "")
        abstract = inspect.cleandoc(response.xpath(
            "//div[@class='abstractContainer']/p/text() | //div[@class='abstractContainer']/text() | //div[@class='abstractContainer']/span/text()").get())

        paper_id = response.xpath("//div[@class='maincard narrower poster']/@id").get()
        pdf_id = response.xpath("//div[@id=$pid]/div/span/a/@href", pid=paper_id).get().split("forum")[1]
        pdf_url = "https://openreview.net/pdf" + pdf_id
        return conf, title, pdf_url, clean_title, authors, abstract


class IcmlScrapySpider(BaseSpider):
    name = 'icml'
    start_urls = [
        "https://icml.cc/",
    ]

    def parse(self, response):
        for conf in self.wanted_conf:
            url = response.urljoin("Conferences/" + conf[4:] + "/Schedule")
            yield scrapy.Request(url, callback=self.parse_paper_list)

    def parse_paper_list(self, response):
        paper_id_list = response.xpath(
            "//div[@id='base-main-content']/div[2]/div[3 < position()]/div[@class='maincard narrower poster']/@id").extract()

        for paper_id in paper_id_list:
            url = response.url + "?showEvent=" + paper_id.split("_")[1]

            yield scrapy.Request(url, callback=self.parse_paper)

    @staticmethod
    def extract_data(response):

        conf = "".join(response.xpath(
            "//div[@id='sidebar']/div/span/b/text() | //div[@id='sidebar']/div/span/b/span/text()").extract()).replace(
            " | ", "")
        title = inspect.cleandoc(
            response.xpath("//div[@id='base-main-content']/div[2]/div[@id=$pid]/div[@class='maincardBody']/text()",
                           pid="maincard_" + response.url.split("=")[1]).get())
        clean_title = re.sub(r'\W+', ' ', title).lower()
        authors = inspect.cleandoc(
            ",".join(response.xpath("//div[@id='base-main-content']/div[2]/button/text()").extract())).replace("»", "")
        abstract = inspect.cleandoc(response.xpath(
            "//div[@class='abstractContainer']/p/text() | //div[@class='abstractContainer']/text() | //div[@class='abstractContainer']/span/text()").get())

        # ICML currently does not provide pdf link in this source. So the code below won't get anything.
        paper_id = response.xpath("//div[@class='maincard narrower poster']/@id").get()
        pdf_id = response.xpath("//div[@id=$pid]/div/span/a/@href", pid=paper_id).get().split("forum")[1]
        pdf_url = "https://openreview.net/pdf" + pdf_id
        return conf, title, pdf_url, clean_title, authors, abstract


class MmScrapySpider(BaseSpider):
    name = 'mm'
    # start_urls = [
    #     "https://dl.acm.org/pb/widgets/proceedings/getProceedings?widgetId=517fcc12-7ff3-4236-84f8-899a672b4a79&pbContext=;taxonomy:taxonomy:conference-collections;topic:topic:conference-collections>mm;page:string:Proceedings;wgroup:string:ACM Publication Websites;csubtype:string:Conference;ctype:string:Conference Content;website:website:dl-site;pageGroup:string:Publication Pages&ConceptID=119833",
    # ]
    start_urls = [
        "https://dl.acm.org/pb/widgets/proceedings/getProceedings?widgetId=517fcc12-7ff3-4236-84f8-899a672b4a79&pbContext=;taxonomy:taxonomy:conference-collections;topic:topic:conference-collections>mm;page:string:Proceedings;wgroup:string:ACM Publication Websites;csubtype:string:Conference;ctype:string:Conference Content;website:website:dl-site;pageGroup:string:Publication Pages&ConceptID=119833",
    ]
    base_url = "https://dl.acm.org"
    download_delay = 3

    def parse(self, response):
        received_data = json.loads(response.text)
        for conf in self.wanted_conf:
            for conf_data in received_data['data']['proceedings']:
                if conf_data['title'].split(":")[0][-2:] == conf[-2:]:
                    link = conf_data['link']
                    break
            url = self.base_url + link
            yield scrapy.Request(url, callback=self.parse_session_list)

    def parse_session_list(self, response):
        session_list = response.xpath("//div[@class='accordion sections']/div[@class='accordion-tabbed rlist']/div/a/@href").extract()

        for session in session_list:
            doi = re.search(pattern=r'10(.+?)\?', string=session)[0][:-1]
            tocHeading = session.split("=")[1]
            url = "https://dl.acm.org/pb/widgets/lazyLoadTOC?tocHeading={}&widgetId=f51662a0-fd51-4938-ac5d-969f0bca0843&doi={}&pbContext=;" \
                  "article:article:doi\:{};" \
                  "taxonomy:taxonomy:conference-collections;" \
                  "topic:topic:conference-collections>mm;" \
                  "wgroup:string:ACM Publication Websites;" \
                  "groupTopic:topic:acm-pubtype>proceeding;" \
                  "csubtype:string:Conference Proceedings;" \
                  "page:string:Book Page;" \
                  "website:website:dl-site;" \
                  "ctype:string:Book Content;journal:journal:acmconferences;" \
                  "pageGroup:string:Publication Pages;" \
                  "issue:issue:doi\:{}".format(tocHeading, doi, doi, doi)

            yield scrapy.Request(url, callback=self.parse_paper_list)

    def parse_paper_list(self, response):
        doi_list = response.xpath("//div[@class='issue-item clearfix']/div/div/h5/a/@href").extract()

        for doi in doi_list:
            url = self.base_url + doi
            yield scrapy.Request(url, callback=self.parse_paper)

    @staticmethod
    def extract_data(response):

        title = response.xpath("//div[@class='article-citations']/div[@class='citation']/div[@class='border-bottom clearfix']/h1/text()").get()
        clean_title = re.sub(r'\W+', ' ', title).lower()

        authors = inspect.cleandoc(",".join(response.xpath(
            "//div[@class='article-citations']/div[@class='citation']/div[@class='border-bottom clearfix']/div[@id='sb-1']/ul/li[@class='loa__item']/a/@title").extract()))

        abstract = inspect.cleandoc(response.xpath("//div[@class='abstractSection abstractInFull']/p/text()").get())
        conf = response.xpath("//div[@class='article-citations']/div[@class='citation']/div[@class='border-bottom clearfix']/div[@class='issue-item__detail']/a/@title").get().split(":")[0]
        pdf_url = ""

        return conf, title, pdf_url, clean_title, authors, abstract
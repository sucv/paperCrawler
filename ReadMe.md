## Table of Contents

- [Paper Crawler for Top CS/AI/ML/NLP Conferences and Journals](#paper-crawler-for-top-csai-mlnlp-conferences-and-journals)
  - [Supported Conferences](#supported-conferences)
  - [Supported Journals](#supported-journals)
  - [Scraped Information](#scraped-information)
- [Installation](#installation)
- [Usage](#usage)
  - [Example Commands](#example-commands)
- [Adding a Custom Spider (Quick & Lazy Solution)](#adding-a-custom-spider-quick--lazy-solution)
  - [Adding a Journal Spider](#adding-a-journal-spider)
  - [Adding a Conference Spider](#adding-a-conference-spider)
  - [Explanation](#explanation)
- [Supported Arguments](#supported-arguments)
- [Change Log](#change-log)

## Paper Crawler for Top CS/AI/ML/NLP Conferences and Journals

This is a [Scrapy](https://docs.scrapy.org/en/latest/intro/tutorial.html)-based crawler. The crawler scrapes accepted papers from top conferences and journals, including:

> &ast; The official sites of these publishers either do not have a consistent HTML structure or block spiders. The spider will attempt to query the title from CrossRef, the abstract could be fetched once the corresponding paper is open-accessed and being hosted on Arxiv. 

### Supported Conferences

| Conference  | Status | Since |
|-------------|--------|-------|
| CVPR        | ✅    | 2013  |
| ECCV        | ✅    | 2018  |
| ICCV        | ✅    | 2013  |
| NIPS        | ✅    | 1987  |
| ICLR        | ✅    | 2016  |
| ICML        | ✅    | 2015  |
| AAAI*       | ✅    | 1980  |
| IJCAI       | ✅    | 2017  |
| ACM MM*     | ✅    | 1993  |
| KDD         | ✅    | 2015  |
| WWW*        | ✅    | 1994  |
| ACL         | ✅    | 2013  |
| EMNLP       | ✅    | 2013  |
| NAACL       | ✅    | 2013  |
| Interspeech | ✅    | 1987  |
| ICASSP      | ✅    | 1976  |

### Supported Journals

| Journal | Status | Since |
|---------|--------|-------|
| TPAMI*  | ✅    | 1979  |
| NMI*    | ✅    | 2019  |
| PNAS*   | ✅    | 1997  |
| IJCV*   | ✅    | 1987  |
| IF*     | ✅    | 2014  |
| TIP*    | ✅    | 1992  |
| TAFFC*  | ✅    | 2010  |
| TSP*    | ✅    | 1991  |

### Scraped Information

The following information is extracted from each paper:

```text
Conference, matched keywords, title, citation count, categories, concepts, code URL, PDF URL, authors, abstract, doi
```

## Installation

```shell
pip install scrapy pyparsing feedparser fuzzywuzzy git+https://github.com/sucv/paperCrawler.git
```

## Usage

First, navigate to the directory where `main.py` is located. During crawling, a CSV file will be generated in the same directory by default unless `-out` is specified.

### Example Commands

#### Get all papers from CVPR, ICCV, and ECCV (2021-2023) and save output to `myresearch/all.csv`, also download papers whose citation count is no smaller than 50
```shell
python main.py -confs cvpr,iccv,eccv -years 2021,2022,2023 -queries "" -out "myresearch/all.csv" -download_pdf 50
```

#### Query papers with titles containing `emotion recognition`, `facial expression`, or `multimodal` without downloading paper
```shell
python main.py -confs cvpr,iccv,eccv -years 2021,2022,2023 -queries "(emotion recognition) or (facial expression) or multimodal"
```
> **Note:** More examples for queries with AND, OR, (), wildcard can be found [here](https://github.com/pyparsing/pyparsing/blob/master/examples/booleansearchparser.py#L329C18-L329C18).

#### Query papers with more advanced boolean expressions
```shell
python main.py -confs cvpr,iccv,eccv -years 2021,2022,2023 -queries "emo* and (visual or audio or speech)" 
```

#### Query papers from all the sources for Year 2021-2023 whose citation count is no smaller than 50
```shell
python main.py -years 2021,2022,2023 -queries "emo* and (visual or audio or speech)" -download_pdf 50
```

## Adding a Custom Spider (Quick & Lazy Solution)

[dblp](https://dblp.org/) provides consistent HTML structures, making it easy to add custom spiders for publishers. You can quickly create a spider for any conference or journal. DBLP provides useful information such as citation count and paper categories. Though the abstract is not available from DBLP, the spider will try to salvage by investigating whether the paper is available on Arxiv and fetch the abstract if available.

### Adding a Spider

In `spiders.py`, add the following code:

A spider for a journal or conference, e.g., TPAMI
```python
class TpamiScrapySpider(DblpScrapySpider):
    name = "tpami"

    start_urls = [
        "https://dblp.org/db/journals/pami/index.html",
    ]
```

A spider for multiple vanues (e.g., Nature and Journal of ACM), please refer to DBLP itself or `venues.py`and manually added your interested venues into `start_urls`.
```python
class ExtraScrapySpider(DblpScrapySpider):
    name = 'extra'

    start_urls = [
        "https://dblp.org/db/journals/nature/index.html",
        "https://dblp.org/db/journals/jacm",
    ]
```

### Explanation

Simply inherit from `DblpScrapySpider`, set `name=`, and provide `start_urls` pointing to your interested DBLP homepage. The rest is handled automatically. Later, you can use the specified `name` to crawl paper information.

## Supported Arguments

- `confs`: A list of supported conferences and journals (must be lowercase, separated by commas), which was defined as `name` in each spider. If not specified, all the available publishers will be queried.
  - Available publisher names so far: `cvpr,iccv,eccv,aaai,ijcai,nips,iclr,icml,mm,kdd,www,acl,emnlp,naacl,tpami,nmi,pnas,ijcv,if,tip,taffc,interspeech,icassp,tsp`. Feel free to add more based on the instruction above.
- `years`: A list of four-digit years (separated by commas). If not specified, will query for recent 10 years (since 2016).
- `queries`: A case-insensitive query string supporting `()`, `and`, `or`, `not`, and wildcard `*`, based on [pyparsing](https://github.com/pyparsing/pyparsing/blob/master/examples/booleansearchparser.py). See examples [here](https://github.com/pyparsing/pyparsing/blob/master/examples/booleansearchparser.py#L329C18-L329C18).
- `out`: Specifies the output csv path. `.csv` will be appended if it does not end with ".csv". The pdfs, if to be downloaded, will be saved in the same directory.
- `download_pdf`: The citation count threshold to decide whether to download a paper. Must be an integer. By default, the value is `-1` which would download nothing.  

## Change Log

+ 13-MAR-2024
  + Fixed a bug so that the pdfs can be downloaded to `pdf_dir`.
  + Fixed a bug in which duplicated pdf urls could be saved.
  + Merged the `DblpScrapySpider` and `DblpConfScrapySpider` as one.
  + Added the top venues from DBLP for CS. 
  + Fixed the Arxiv's abstract line break issue.
+ 12-MAR-2024
  + Improved the `pipeline.py`so that when CrossRef API says the paper is open-accessed, it will not only accumulate all the OA pdf url, but also examine whether the url is from Arxiv. If so, it will further request the abstract from Arxiv API. Since there is a great number of paper being open-accessed, doing so may largely salvage the records from DBLP that do not come with such information.
  + Added `download_pdf`as the citation count threshold for downloading a paper. Only if a paper's citation count is greater than or eqal to the threshold, would the paper be downloaded.
  + Removed `--nocrossref` so that the CrossRef API is always called. Doing so can fetch useful information such as citation count, concepts, etc.
  + Removed `from_dblp` for each spider class. Now it doesn't matter whether the record is from dblp or the original publisher, they all follow the same processing logic.
  + Fixed the `code_url`. If it ends with a period `.`, the latter will be removed.
+ 10-MAR-2025
  + Fixed the last false match bug by thresholding the match score. 
+ 7-FEB-2025
  + Found a bug in which when the paper title cannot be successfully fetched from the top-5 query results, the citation count / categories / concepts from the CrossRef would be false. Haven't figured out how to fix it without importing extra libraries for sophisticated matching. I will leave it for now since it only affect a very small percentage (~0.1%) of the results. 
+ 17-JAN-2025
  + Add spiders for Interspeech, TSP, and ICASSP.
+ 15-JAN-2025
  + Add citation count, concepts, categories for a matched paper based on the Crossref API, with 1s cooldown for each request. For unmatched paper, the download cooldown won't be triggered.
  + Fixed multiple out-of-date crawlers.
  + Removed some arguments such as `count_citations` and `query_from_abstract`. Now it will call Crossref API for extra information by default, and will always query from title, not abstract.
+ 19-JAN-2024
  + Fixed an issue in which the years containing single volume and multiple volumes of a journal from dblp cannot be correctly parsed. 
+ 05-JAN-2024
  + Greatly speeded up journal crawling, as by default only title and authors are captured directly from dblp. Specified `-count_citations` to get `abstract`, `pdf_url`, and `citation_count`.
+ 04-JAN-2024
  + Added support for ACL, EMNLP, and NAACL.
  + Added support for top journals, including TPAMI, NMI (Nature Machine Intelligence), PNAS, IJCV, IF, TIP, and TAAFC via dblp and sematic scholar AIP. Example is provided.
    + You may easily add your own spider in `spiders.py` by inheriting class `DblpScrapySpider` for the conferences and journals as a shortcut. In this way you will only get the paper title and authors. As paper titles can already provide initial information, you may manually search for your interested papers later. 
+ 03-JAN-2024
  + Added the `-out` argument to specify the output path and filename.
  + Fixed urls for NIPS2023.
+ 02-JAN-2024
  + Fixed urls that were not working due to target website updates.
  + Added support for ICLR, ICML, KDD, and WWW.
  + Added support for querying with [pyparsing](https://github.com/pyparsing/pyparsing/blob/master/examples/booleansearchparser.py):
    + 'and', 'or' and implicit 'and' operators;
    + parentheses;
    + quoted strings;
    + wildcards at the end of a search term (help*);
    + wildcards at the beginning of a search term (*lp);
+ 28-OCT-2022
  + Added a feature in which the target conferences can be specified in `main.py`. See Example 4. 
+ 27-OCT-2022
  + Added support for ACM Multimedia. 
+ 20-OCT-2022
  + Fixed a bug that falsely locates the paper pdf url for NIPS.
+ 7-OCT-2022
    + Rewrote `main.py` so that the crawler can run over all the conferences!
+ 6-OCT-2022
    + Removed the use of `PorterStemmer()` from `nltk` as it involves false negative when querying.
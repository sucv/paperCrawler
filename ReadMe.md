## Paper Crawler for Top AI Conferences

This is a Scrapy-based crawler. A tutorial is [at this url](https://www.logx.xyz/scrape-papers-using-scrapy). The scraped information includes:

```text
Conference, matched keywords, title, citation count, code url, pdf url, authors, abstract
```

The crawler scrapes accepted papers from top AI conferences, including:

- CVPR and ICCV since 2013.
- ECCV since 2018.
- AAAI since 1980.
- IJCAI since 2017.
- NIPS since 1987.
- ICML since 2017.
- ICLR 2018, 2019, 2021, and 2022.
  - `pdf_url` may not work for ICML and ICLR (2022) as the website does not provide the url.
- ACM MM since 2001.
  - `pdf url` is not available, as the ACM is not open-access.
  - The `download_delay` is set to 3s to not being banned.

### Change Log

+ 28-OCT-2022
  + Added a feature in which the target conferences can be specified in `main.py`. See Example 4. 
+ 27-OCT-2022
  + Added the crawler for ACM Multimedia. 
+ 20-OCT-2022
  + Fixed a bug that falsely locates the paper pdf url for NIPS.
+ 7-OCT-2022
    + Rewrote `main.py` so that the crawler can run over all the conferences!
+ 6-OCT-2022
    + Removed the use of `PorterStemmer()` from `nltk` as it involves false negative when querying.



### Install

```shell
pip install scrapy semanticscholar fuzzywuzzy git+https://github.com/sucv/paperCrawler.git
```

### Usage

It's a [Scrapy](https://docs.scrapy.org/en/latest/intro/tutorial.html) project. Simply cd to `PaperCrawler/crawlconf/`
then call the spider. Some examples are provided below.

#### For single conference

```shell
scrapy crawl [conference name] -a years=[year1,year2,...,yearn] -a keys=[key1,key2,...,keyn] -a cc=[1 or 0] -o [output_filename.csv] -s JOBDIR=[checkpoint_folder]
```
+ `conference name`: cvpr, iccv, eccv, aaai, ijcai, nips, icml, iclr, mm. Must be lowercase.
+ `year`: Four-digit numbers, use comma to separate.
+ `keys`: The abstract must contain at least one of the keywords. Use comma to separate.
+ `cc`: Set to 1 to count the citations using SemanticScholar API.
+ `output_filename`: The output csv filename. The outputs will attach to previous file if two commands share the same
  output filename.
+ `checkpoint_folder`: The folder to store the spider state.

##### Example 1: 

```shell
scrapy crawl iccv -a years=2021,2019,2017 -a keys=video,emotion -o output.csv
```

The command above can scrape the information of all papers from ICCV2017, ICCV2019, ICCV2021, with "video" OR "emotion"
appeared in the abstracts. The results will be saved in `output.csv`. It won't count the citations and save the
checkpoint. It scrapes really fast.

##### Example 2

```shell
scrapy crawl nips -a years=2020,2021,2022 -a keys=video,emotion -a cc=1 -o output.csv 
```

The command above works in the same manner, it also scrapes the number of citation for each paper. Note that the latter
is done using the free [SemanticScholar API](https://www.semanticscholar.org/product/api). Currently, I use the paper
title to query. Note that the API has a maximum request limit per second. Use this command with cautious, because it
could be dramatically time-consuming. (Or skip the citation count and post-process the `output.csv` on your own.)

##### Example 3

```shell
scrapy crawl ijcai  -a years=2021,2020 -a keys=video -a cc=1 -o output.csv -s JOBDIR=folder1
```

The command above will save the scraping [checkpoint](https://docs.scrapy.org/en/latest/topics/jobs.html#topics-jobs) in
a folder named `folder1`. If the scraping process is interrupted by `CTRL+C` or other incidents, simply execute the same
command so that the scraping can continue.


#### For multiple conferences:

```shell
python main.py -confs [conf1,conf2,...,confn] -years [year1,year2,...,yearn] -keys [key1,key2,...,keyn] -cc 1
```

##### Example 4

```shell
python main -confs cvpr,iccv,eccv -years 2018,2019,2020,2021,2022 -keys emotion,multimodal,multi-modal -cc 1
```
The command would scrape the papers, whose abstracts contain at least one keys, from CVPR, ICCV, and ECCV since 2018. In this case, the scraped data will be saved in `data.csv`, which is defined in `settings.py`. Note, specify`cc` to `0` and exclude `mm` from the `confs` can greatly speed-up the process.


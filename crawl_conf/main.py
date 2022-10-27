# from scrapy import cmdline
#
# cmdline.execute("scrapy crawl mm  -a years=2016,2017,2018,2019,2020,2021,2022 -a keys=emotion,affective -o emotion.csv".split())

# cmdline.execute("scrapy crawl nips  -a years=2016,2017,2018,2019,2020,2021,2022 -a keys=emotion,affective -o emotion.csv".split())
#
# # cmdline.execute("scrapy crawl nips  -a years=2015 -a keys=video -o test.csv".split())
# # cmdline.execute("scrapy crawl eccv  -a years=2020,2021,2022 -a keys=video -o output.csv -s JOBDIR=folder6".split())


from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Hello PhD life!')
    parser.add_argument('-years', default="2016,2017,2018,2019,2020,2021,2022", type=str, help='What years you want to crawl?')
    parser.add_argument('-keys', default="relation, relationship,correlate,correlation", type=str, help='What keywords you want to query?')
    parser.add_argument('-cc', default=0, type=int, help='Count the citations?')

    args = parser.parse_args()

    years = args.years
    keys = args.keys
    count_citation = args.cc

    setting = get_project_settings()
    process = CrawlerProcess(setting)


    for spider_name in process.spiders.list():
        print ("Running spider %s" % (spider_name))
        process.crawl(spider_name,years=years, keys=keys, cc=count_citation)

    process.start()
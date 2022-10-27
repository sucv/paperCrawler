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
    parser.add_argument('-confs', default="cvpr,iccv,eccv,nips,icml,iclr,mm,aaai,ijcai", type=str,
                        help='What years you want to crawl?')
    parser.add_argument('-years', default="2016,2017,2018,2019,2020,2021,2022", type=str, help='What years you want to crawl?')
    parser.add_argument('-keys', default="relation, relationship,correlate,correlation", type=str, help='What keywords you want to query?')
    parser.add_argument('-cc', default=0, type=int, help='Count the citations?')

    args = parser.parse_args()

    confs = args.confs
    years = args.years
    keys = args.keys
    count_citation = args.cc

    setting = get_project_settings()
    process = CrawlerProcess(setting)

    for conf in confs.split(","):
        process.crawl(conf, years=years, keys=keys, cc=count_citation)

    process.start()
import os

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Hello PhD life!')
    parser.add_argument('-confs', default="cvpr,iccv,eccv,aaai,ijcai,nips,iclr,icml,mm,kdd,www,acl,emnlp,naacl,tpami,nmi,pnas,ijcv,if,tip,taffc,interspeech,icassp,tsp", type=str,
                        help='What years you want to crawl?')
    parser.add_argument('-years', default="2016,2017,2018,2019,2020,2021,2022,2023,2024,2025", type=str, help='What years you want to crawl?')
    parser.add_argument('-queries', default="relation, relationship,correlate,correlation", type=str, help='What keywords you want to query?')
    parser.add_argument('-out', default="./downloads/output.csv", type=str, help='Specify the output path as /path/to/filename.csv')
    parser.add_argument('-download_pdf', type=int, default=-1, help='Citation count threshold to download a paper. Will download a paper if its citation count is greater than or equal to it.')
    parser.add_argument('--nocrossref', action='store_true', help='Do not request extra details through API call from Crossref')

    args = parser.parse_args()

    confs = args.confs
    years = args.years
    queries = args.queries
    nocrossref = args.nocrossref

    out_csv = args.out
    if not out_csv.endswith('.csv'):
        print("The output csv must end with .csv!")
        out_csv += '.csv'

    download_pdf = args.download_pdf
    if download_pdf < -1:
        download_pdf = -1

    # ------------------------------------------------------------
    # Get default Scrapy settings and instantiate a CrawlerProcess
    # ------------------------------------------------------------
    setting = get_project_settings()
    process = CrawlerProcess(setting)

    # You have set some feed-output settings
    process.settings.set('FEED_FORMAT', 'csv')          # or 'csv', 'xml', etc.
    process.settings.set('FEED_URI', 'data.csv')        # default output file name

    if args.out is not None:
        # If user specified an output path, override the default
        process.settings.set('FEED_URI', out_csv)


    # ------------------------------------------------------------
    # Now queue up the crawls for each requested conference
    # ------------------------------------------------------------
    for conf in confs.split(","):
        process.crawl(
            conf.lower(),
            years=years,
            queries=queries,
            nocrossref=nocrossref,
            download_pdf=args.download_pdf,
            pdf_dir = os.path.dirname(out_csv)
        )

    process.start()

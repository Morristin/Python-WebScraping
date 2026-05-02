import argparse
import datetime as dt
import logging
import os
from pathlib import Path

import bpython

from web_scraping.actions import get_history_price_on_hp as get_his_history
from web_scraping.actions import get_history_price_on_mmb as get_mmb_history
from web_scraping.actions import get_history_price_on_mmb_direct as get_mmb_history_direct
from web_scraping.actions import search_on_mmb as search
from web_scraping.spider import Spider

# Check all functions are prepared in namespace.
_NAMESPACE = (search, get_mmb_history, get_his_history, get_mmb_history_direct)

logging.getLogger(__name__)

parser = argparse.ArgumentParser(prog='WebScraping', description='Get the history price of goods.')

parser.add_argument('-S', '--search', action='store', default=None,
                    metavar='Good Name', help='Specific the name of the good')
parser.add_argument('--limit', action='store', default=1, type=int,
                    metavar='n', help='Limit the number of goods in search result.')
parser.add_argument('--history', '--get-history-data', action='store_true', default=False,
                    help='Collect each good\'s history prices for every good in search result.')
parser.add_argument('--debug', '--print-log', action='store_true', default=False)
parser.add_argument('--version', action='version', version='WebScraping Preview Version')

if __name__ == '__main__':
    program_args = parser.parse_args()

    log_format = "%(asctime)s : %(levelname)-7s : %(name)-7s : %(message)s"
    if program_args.debug:
        logging.basicConfig(format=log_format, level=logging.INFO)
        logging.warning(f'Debug mode is active. Your search requirement may be ignored.')
        with Spider() as spider:
            bpython.embed(locals_=globals())
    else:
        log_path = Path(f'log/{dt.date.today()}.log')
        if not log_path.parent.exists():
            os.mkdir(log_path.parent)
            log_path.touch()
        logging.basicConfig(filename=log_path, format=log_format, level=logging.INFO)

        with Spider() as spider:
            search(spider, program_args.search, program_args.limit, program_args.history)
            print(f'Successfully search good {program_args.search} and store its prices to database.')

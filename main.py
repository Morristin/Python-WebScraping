import argparse
import datetime as dt
import logging
import os
from pathlib import Path

import bpython

from web_scraping.actions import get_history_price_on_hisprice as get_his_history
from web_scraping.actions import get_history_price_on_manmanbuy as get_mmb_history
from web_scraping.actions import get_history_price_on_manmanbuy_direct as get_mmb_history_direct
from web_scraping.actions import search_on_manmanbuy as search
from web_scraping.spider import Spider

# Check all functions are prepared in namespace.
_NAMESPACE = (search, get_mmb_history, get_his_history, get_mmb_history_direct)

logging.getLogger(__name__)

parser = argparse.ArgumentParser(prog='WebScraping', description='A web scraping tool for you to interact with.')
parser.add_argument('--debug', '--print-log', action='store_true', default=False)
parser.add_argument('--version', action='version', version='WebScraping Preview Version')


def main():
    print(f'You are now on "interact" branch of repository. Please start program in debug mode.')


if __name__ == '__main__':
    program_args = parser.parse_args()

    log_format = "%(asctime)s : %(levelname)-7s : %(name)-7s : %(message)s"
    if program_args.debug:
        logging.basicConfig(format=log_format, level=logging.INFO)
        logging.warning(f'Debug mode is active.')
        with Spider() as spider:
            bpython.embed(locals_=globals())
    else:
        log_path = Path(f'log/{dt.date.today()}.log')
        if not log_path.parent.exists():
            os.mkdir(log_path.parent)
            log_path.touch()
        logging.basicConfig(filename=log_path, format=log_format, level=logging.INFO)
        main()

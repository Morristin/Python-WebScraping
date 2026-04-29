import argparse
import code
import datetime as dt

from web_scraping.spider import *

logging.getLogger(__name__)

parser = argparse.ArgumentParser(prog='WebScraping', description='A web scraping tool for you to interact with.')
parser.add_argument('--print-log', action='store_true', default=False)
parser.add_argument('--version', action='version', version='WebScraping Preview Version')

if __name__ == '__main__':
    program_args = parser.parse_args()

    log_format = "%(asctime)s : %(levelname)-7s : %(name)-7s : %(message)s"
    if program_args.print_log:
        logging.basicConfig(format=log_format, level=logging.INFO)
        logging.warning(f'Debug mode is active.')
    else:
        log_path = Path(f'log/{dt.date.today()}.log')
        if not log_path.parent.exists():
            os.mkdir(log_path.parent)
            log_path.touch()
        logging.basicConfig(filename=log_path, format=log_format, level=logging.INFO)

    code.interact(banner='WebScraping by Morristin', local=locals(), local_exit=True)

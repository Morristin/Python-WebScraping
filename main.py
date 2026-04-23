import argparse
import datetime as dt

from web_scraping.spider import *

logging.getLogger(__name__)

parser = argparse.ArgumentParser(prog='main.py',
                                 description='Search the price of the good given and store to database.')

parser.add_argument('-S', '--search', action='store', default=None,
                    metavar='Good Name', help='Specific the name of the good')
parser.add_argument('--limit', action='store', default=1, type=int,
                    metavar='n', help='Limit the number of pages read from search result')
parser.add_argument('--ai-parser', action='store', default=None, metavar='Model-size(:cloud)',
                    help='The name of AI model you want to use for parser data (must match your ollama model)')
parser.add_argument('--version', action='version', version='WebScraping Preview Version',
                    help='Print the version of the program')


def parse_args(args: argparse.Namespace):
    search = args.search
    if search is None:
        search = input('Please enter the good you want to search: ')
        if len(search.strip()) == 0:
            print('You must enter a valid good name.')
            logging.error(f'User enter an invalid good name. Program exit.')
            exit()
        else:
            args.search = search
            logging.info(f'Get good name from user input: {search}')
    else:
        logging.info(f'Get good name from args: {search}')

    settings.set('ollama_model', args.ai_parser)
    return args


if __name__ == '__main__':
    log_format = "%(asctime)s : %(levelname)-7s : %(name)-7s : %(message)s"
    if settings.debug:
        logging.basicConfig(format=log_format, level=logging.INFO)
        logging.warning(f'Debug mode is active.')
    else:
        log_path = Path(f'log/{dt.date.today()}.log')
        if not log_path.parent.exists():
            os.mkdir(log_path.parent)
            log_path.touch()
        logging.basicConfig(filename=log_path, format=log_format, level=logging.INFO)

    program_args = parse_args(parser.parse_args())
    spider = ManManBuySpider()
    spider.search(program_args.search, program_args.limit)
    print(f'Successfully search good {program_args.search} and store its prices to database.')
    spider.quit()

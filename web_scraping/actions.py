import logging
from pathlib import Path

from database.data_manager import data_manager
from web_scraping.spider import Spider

logging.getLogger(__name__)


# noinspection PyUnresolvedReferences
def search_on_manmanbuy(spider: Spider, keyword: str, page: int = 1):
    search_url = 'https://s.manmanbuy.com/pc/search/result?keyword={}&pageId={}'
    search_result = spider.get(search_url.format(keyword, page), use_cache=True)

    import bs4
    try:
        content = bs4.BeautifulSoup(search_result, 'lxml')
    except bs4.exceptions.FeatureNotFound:
        content = bs4.BeautifulSoup(search_result, 'html.parser')

    import re
    goods = content.find_all('div', class_=re.compile(r'DiscountItem.*itemContent'))
    for good in goods:
        name = good.find('div', class_=re.compile(r'DiscountItem.*itemTitle')).a.attrs['title']

        price = good.find('div', class_=re.compile(r'DiscountItem.*itemSubTitle')).get_text()
        if (re.compile(r'需.*(?:会员|VIP)').search(price) is not None) or (
                re.compile(r'需.*凑单').search(price) is not None):
            logging.info(f'Data is not stored as the price is invalid: {price}')
            continue
        price = re.compile(r'(\d+(\.\d+)?)元').search(price).group(1)

        import datetime as dt
        date = good.find('span', class_=re.compile(r'DiscountItem.*itemTime')).get_text()
        date = dt.datetime.fromisoformat(f'{dt.datetime.today().year}-{date}' if date[:2] != '20' else date)

        platform = good.find('span', class_=re.compile(r'DiscountItem.*itemMall')).get_text()
        link = good.find('div', class_=re.compile(r'DiscountItem.*itemTitle')).a.attrs['href']
        data_manager.add_good(name, price, date, platform, link)


def get_history_price_on_manmanbuy(spider: Spider, good_name: str, good_url: str, good_platform: str = None, /,
                                   load_cookies: bool = True):
    """
    Get manmanbuy history data using webdriver.

    The history data of good is read directly from local data,
    and this function require valid cookie of manmanbuy or manually log in.
    """

    def wait_for_element(xpath: str, click: bool = False):
        from selenium.common import NoSuchElementException
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.expected_conditions import visibility_of_element_located
        from selenium.webdriver.support.wait import WebDriverWait

        wait = WebDriverWait(spider.webdriver, timeout=20, poll_frequency=0.5,
                             ignored_exceptions=[NoSuchElementException])
        wait.until(visibility_of_element_located((By.XPATH, xpath)))
        if click:
            spider.webdriver.find_element(By.XPATH, xpath).click()

    website_url = 'https://www.manmanbuy.com/'
    cookies_path = Path('web_scraping/cookies/manmanbuy_cookies.json')

    if load_cookies:
        try:
            spider.load_cookies(cookies_path=cookies_path, website=website_url)
        except FileNotFoundError:
            spider.get(website_url)
            wait_for_element("//a[@class='pt' and contains(text(), '登录')]", click=True)
            input('No valid cookies. Please manually log in, and press the enter to continue.')
            spider.store_cookies(cookies_path=cookies_path)

    spider.get(good_url)
    wait_for_element("//img[contains(@src, 'trendChartImage')]", click=True)
    spider.webdriver.switch_to.window(spider.webdriver.window_handles[-1])
    wait_for_element("//canvas")
    history_data = spider.webdriver.execute_script('''return flotChart.oldData''')

    import datetime as dt
    for data in history_data:
        date = dt.datetime.fromtimestamp(data[0] / 1000)
        data_manager.add_good(name=good_name, price=data[1], date=date, platform=good_platform)

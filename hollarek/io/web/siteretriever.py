from __future__ import annotations
from .mail_addresses import get_mail_addresses_in_text

import threading
import requests
import logging
from func_timeout import func_timeout
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import Optional

from func_timeout import FunctionTimedOut

# ---------------------------------------------------------

class SiteRetriever:
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SiteRetriever, cls).__new__(cls)
        return cls._instance

    def __init__(self,google_key : Optional[str] = None,
                 searchengine_id : Optional[str] = None,
                 webdriver_count: int = 4):

        if not SiteRetriever._is_initialized:
            if google_key is None or searchengine_id is None:
                raise ValueError(f'Google API key and search engine ID must be provided but one of the arguments is None \n'
                                 f'google_key : {google_key}; searchengine_id : {searchengine_id}')

            self._GOOGLE_API_KEY : str = google_key
            self._SEARCHENGINE_ID : str = searchengine_id

            self.drivers: list[WebDriver] = []
            for _ in range(webdriver_count):
                start_thread = threading.Thread(target=self._make_driver)
                start_thread.start()
            self.is_initialized = True


    def get_urls(self, search_term: str, num_results : int = 4) -> list[str]:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': f'{search_term}',
            'key': self._GOOGLE_API_KEY,
            'cx': self._SEARCHENGINE_ID,
            'num' : num_results
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            logging.warning(f'An error occured during search: {response.status_code} {response.reason}')
            return []

        response_content = response.json()
        search_results = response_content.get('items')
        if search_results is None:
            logging.warning(f'Unable to obtain search results')
            return []
        search_result_urls = [result['link'] for result in search_results]


        return search_result_urls


    def get_mail_addresses(self, site_url : str) -> list[str]:
        return get_mail_addresses_in_text(text=self.get_html(site_url=site_url))


    def get_html(self, site_url: str) -> str:
        driver = self._get_free_driver()
        try:
            result = driver.fetch_site_html(site_url)

        except FunctionTimedOut:
            logging.warning(f'Failed to retrieve text from website {site_url} due to timeout after {WebDriver.max_site_loading_time} seconds')
            result = ''

        return result

    # ---------------------------------------------------------

    def _get_free_driver(self) -> WebDriver:
        unoccupied_drivers = [driver for driver in self.drivers if not driver.is_busy]
        if len(unoccupied_drivers) > 0:
            return unoccupied_drivers[0]

        else:
            return self._make_driver()

    def _make_driver(self):
        new_driver = WebDriver()
        self.drivers.append(new_driver)

        return new_driver


class WebDriver:
    max_site_loading_time = 10

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        prefs = {
            "download.default_directory": "/dev/null",
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        self.engine = webdriver.Chrome(options=chrome_options)
        self.is_busy = False


    def fetch_site_html(self, site_url: str) -> str:
        self.is_busy = True

        def get_website_html():
            self.engine.get(site_url)
            return self.engine.page_source

        content = func_timeout(timeout=WebDriver.max_site_loading_time,func=get_website_html)
        self.is_busy = False
        return content


if __name__ == '__main__':
    from ..configs.config_manager import ConfigManager, StdCategories

    new_conf_manger = ConfigManager()
    google_api_key = new_conf_manger.get_value(key='google_key',category=StdCategories.APIS)
    engine_id = new_conf_manger.get_value(key='search_engine_id', category=StdCategories.APIS)

    tool = SiteRetriever(google_key=google_api_key, searchengine_id=engine_id)
    urls = tool.get_urls('beavers')
    print(urls)
    the_text = "Example emails: user@example.com and user[at]example.com user [at] example.com"
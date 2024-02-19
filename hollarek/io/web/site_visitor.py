from __future__ import annotations

from func_timeout import func_timeout
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .mail_addresses import get_mail_addresses_in_text
from func_timeout import FunctionTimedOut
import logging


class SiteVisitor:
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

        content = func_timeout(timeout=SiteVisitor.max_site_loading_time, func=get_website_html)
        self.is_busy = False
        return content


    def get_mail_addresses(self, site_url : str) -> list[str]:
        return get_mail_addresses_in_text(text=self.get_html(site_url=site_url))


    def get_html(self, site_url: str) -> str:
        try:
            result = self.fetch_site_html(site_url)

        except FunctionTimedOut:
            logging.warning(f'Failed to retrieve text from website {site_url} due to timeout after {SiteVisitor.max_site_loading_time} seconds')
            result = ''

        return result

    # def _get_free_driver(self) -> WebDriver:
    #     unoccupied_drivers = [driver for driver in self if not driver.is_busy]
    #     if len(unoccupied_drivers) > 0:
    #         return unoccupied_drivers[0]
    #
    #     else:
    #         return self._make_driver()
    #
    # def _make_driver(self):
    #     new_driver = WebDriver()
    #     self.drivers.append(new_driver)
    #
    #     return new_driver

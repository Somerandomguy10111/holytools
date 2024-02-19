from __future__ import annotations
import requests
import logging
from typing import Optional



# ---------------------------------------------------------

class SearchEngine:
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SearchEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self,google_key : Optional[str] = None,
                 searchengine_id : Optional[str] = None):

        if not SearchEngine._is_initialized:
            if google_key is None or searchengine_id is None:
                raise ValueError(f'Google API key and search engine ID must be provided but one of the arguments is None \n'
                                 f'google_key : {google_key}; searchengine_id : {searchengine_id}')

            self._GOOGLE_API_KEY : str = google_key
            self._SEARCHENGINE_ID : str = searchengine_id


    def get_urls(self, search_term: str, num_results : int = 5) -> list[str]:
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


if __name__ == '__main__':
    from ..configs.config_manager import ConfigManager, StdCategories

    new_conf_manger = ConfigManager()
    google_api_key = new_conf_manger.get_value(key='google_key',category=StdCategories.APIS)
    engine_id = new_conf_manger.get_value(key='search_engine_id', category=StdCategories.APIS)

    tool = SearchEngine(google_key=google_api_key, searchengine_id=engine_id)
    urls = tool.get_urls('beavers')
    print(urls)
    the_text = "Example emails: user@example.com and user[at]example.com user [at] example.com"
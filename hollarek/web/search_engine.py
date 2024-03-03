from __future__ import annotations
import requests
import logging


# ---------------------------------------------------------

class SearchEngine:
    def __init__(self,google_key : str, searchengine_id : str):
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
    from hollarek.configs import LocalConfigs

    new_conf_manger = LocalConfigs()
    google_api_key = new_conf_manger.get(key='google_key')
    engine_id = new_conf_manger.get(key='search_engine_id')

    tool = SearchEngine(google_key=google_api_key, searchengine_id=engine_id)
    urls = tool.get_urls('beavers')
    print(urls)
    the_text = "Example emails: userIO@example.com and userIO[at]example.com userIO [at] example.com"
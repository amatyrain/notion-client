import time
import traceback
import requests

MAX_RETRY = 3

class NotionClient:
    """
    参照: https://developers.notion.com/reference/intro
    """
    def __init__(self, api_token):
        self.integration_token = api_token
        self.base_url = 'https://api.notion.com/v1'

    def _request(self, method, endpoint, data=None, params=None):
        headers = {
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.integration_token}',
        }

        url = f'{self.base_url}/{endpoint}'
        print(f'url: {url}')
        print(f'method: {method}')
        print(f'data: {data}')

        for i in range(MAX_RETRY):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    params=params
                )

                if response.status_code >= 400:
                    raise Exception(response.text)

                return response
            except Exception as e:
                error = e
                error_traceback = traceback.format_exc()
                print(error)
                print(error_traceback)
                print(f"リトライします。{i+1}回目")
                time.sleep(1)
                continue

        raise Exception(f"リトライ回数を超えました。\n{error}\n{error_traceback}")

    def retrieve_database(self, database_id):
        endpoint = f'databases/{database_id}'
        return self._request('GET', endpoint)

    def query_database(self, database_id, **kwargs):
        """_summary_
        Refs: https://developers.notion.com/reference/post-database-query

        Args:
            database_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        endpoint = f'databases/{database_id}/query'
        return self._request('POST', endpoint, data=kwargs)

    def create_page(self, **kwargs):
        endpoint = 'pages'
        return self._request('POST', endpoint, data=kwargs)

    def retrieve_page(self, page_id):
        endpoint = f'pages/{page_id}'
        return self._request('GET', endpoint)

    def update_page(self, page_id, **kwargs):
        endpoint = f'pages/{page_id}'
        return self._request('PATCH', endpoint, data=kwargs)

    def delete_page(self, page_id):
        endpoint = f'pages/{page_id}'
        return self._request('DELETE', endpoint)

    def list_users(self):
        endpoint = 'users'
        return self._request('GET', endpoint)

    def retrieve_user(self, user_id):
        endpoint = f'users/{user_id}'
        return self._request('GET', endpoint)

    def retrieve_block_children(self, block_id, **kwargs):
        endpoint = f'blocks/{block_id}/children'
        return self._request('GET', endpoint, params=kwargs)

    def append_block_children(self, block_id, **kwargs):
        endpoint = f'blocks/{block_id}/children'
        return self._request('PATCH', endpoint, data=kwargs)

    def update_block(self, block_id, **kwargs):
        endpoint = f'blocks/{block_id}'
        return self._request('PATCH', endpoint, data=kwargs)

    def delete_block(self, block_id):
        endpoint = f'blocks/{block_id}'
        return self._request('DELETE', endpoint)

import requests


class NotionClient:
    def __init__(self):
        self.aws_client = AwsAPIClient()
        notion_secrets = self.aws_client.get_ssm_parameter_with_json('NOTION_SECRETS')
        NOTION_API_TOKEN = notion_secrets['API_TOKEN']
        self.integration_token = NOTION_API_TOKEN
        self.base_url = 'https://api.notion.com/v1'

    def _request(self, method, endpoint, data=None, params=None):
        headers = {
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.integration_token}',
        }

        url = f'{self.base_url}/{endpoint}'
        print(f'url: {url}')
        print(f'data: {data}')

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                params=params
            )
        except Exception as e:
            raise Exception(e)

        response.raise_for_status()

        return response.json()

    def retrieve_database(self, database_id):
        endpoint = f'databases/{database_id}'
        return self._request('GET', endpoint)

    def query_database(self, database_id, **kwargs):
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

    # append block children
    def append_block_children(self, block_id, **kwargs):
        endpoint = f'blocks/{block_id}/children'
        return self._request('PATCH', endpoint, data=kwargs)

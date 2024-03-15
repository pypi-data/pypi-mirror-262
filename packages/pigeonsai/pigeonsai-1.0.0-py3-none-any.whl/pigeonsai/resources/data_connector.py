# resources/data_connector.py
from __future__ import annotations

from typing import TYPE_CHECKING
from .._constants import (BASE_URL_V2)

import httpx
import json
import os

if TYPE_CHECKING:
    from .._client import PigeonsAI


class DataConnector:
    data_connection_pri_global = None  # Class variable to store the global data_connection_pri
    train_set_pri_global = None

    def __init__(self, client: PigeonsAI):
        self.client = client

    def create_connector(
        self,
        connection_name: str,
        connection_type: str,
        db_host: str,
        db_name: str,
        db_username: str,
        db_password: str,
        db_port: int
    ):
        url = f"{BASE_URL_V2}/create-data-connector"
        headers = self.client.auth_headers
        data = {
            "conn_id": connection_name,
            "conn_type": connection_type,
            "host": db_host,
            "login": db_username,
            "password": db_password,
            "port": db_port,
            "schema": db_name
        }

        try:
            response = httpx.post(url, headers=headers, json=data, timeout=300.0)
            response.raise_for_status()
            result = response.json()

            res = result.get('data', {})

            filtered_res = {
                'created_at': res.get('created_at'),
                'created_by': res.get('created_by'),
                'data_connection_pri': res.get('data_connection_pri')
            }

            DataConnector.data_connection_pri_global = filtered_res.get('data_connection_pri')

            print(
                f'\033[38;2;85;87;93mConnector creation successful:\033[0m \033[92m{response.status_code} {response.reason_phrase}\033[0m')
            return filtered_res

        except httpx.HTTPStatusError as e:
            error_message = e.response.text
            try:
                error_details = json.loads(error_message)
                detail_message = error_details.get('message', 'No detail provided')
                print(f"Status code: {e.response.status_code}, Detail: {detail_message}")
            except json.JSONDecodeError:
                print(f"Status code: {e.response.status_code}, Error: {error_message}")
        except Exception as e:
            raise e

    def create_train_set(
        self,
        type: str,
        train_set_name: str,
        file_path: str = None,
        data_connection_pri: str = None,
        table_name: str = None,
    ):

        # Use the global data_connection_pri if not provided
        if not data_connection_pri and DataConnector.data_connection_pri_global:
            data_connection_pri = DataConnector.data_connection_pri_global

        if (file_path and data_connection_pri) or (file_path and table_name):
            print("Only one of file or connector_details with table_name should be provided.")
            return

        elif not file_path and not data_connection_pri and not table_name:
            print("Either file or connector_details with table_name must be provided.")
            return

        type = type.lower()
        if not type:
            print('Please provide type as either file or connection. Use file option if you want to upload file or use connection if you want to fetch data directly from the database using data connector. ')
            return

        headers = self.client.auth_headers

        if type == 'file':
            if not file_path:
                print('Missing file path.')
                return
            return _prepare_data_with_file(
                headers=headers,
                train_set_name=train_set_name,
                file_path=file_path
            )

        if type == 'connection':
            if not table_name:
                print('Missing table name. table_name param is the name of the table you want to fetch data from.')
                return

            # todo: handle missing col name

            result = _prepare_data_with_connector(
                headers=headers,
                train_set_name=train_set_name,
                data_connection_pri=data_connection_pri,
                table_name=table_name
            )

            DataConnector.train_set_pri_global = result.get('res', {}).get('data_source_pri')

            return result

    def revision_train_set_with_file(
        self,
        train_set_pri: str,
        file_path: str,
    ):
        url = f"{BASE_URL_V2}/revision-data-source-with-file"
        headers = self.client.auth_headers
        if 'Content-Type' in headers:
            headers.pop('Content-Type')
        data = {
            'train_set_pri': train_set_pri,
        }

        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path, f)}
                response = httpx.post(url, headers=headers, files=files, data=data, timeout=300.0)
                response.raise_for_status()
                print('Success:')
                return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"Status code: {e.response.status_code}, Error: {e.response.text}"
            print(error_message)
        except Exception as e:
            raise e

    def revision_train_set_with_connector(
        self: str,
        train_set_pri: str,
        table_name: str,
    ):
        url = f"{BASE_URL_V2}/revision-data-source-with-connector"
        headers = self.client.auth_headers
        data = {
            'train_set_pri': train_set_pri,
            'table_name': table_name,
        }

        try:
            response = httpx.post(url, headers=headers, json=data, timeout=300.0)
            response.raise_for_status()
            print('Success:')
            return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"Status code: {e.response.status_code}, Error: {e.response.text}"
            print(error_message)
        except httpx.RequestError as e:
            error_message = f"An error occurred while making the request to {e.request.url}: {e.message}"
            print(error_message)
            raise httpx.RequestError(error_message, request=e.request)
        except Exception as e:
            raise e

    def delete_train_set(
        self,
        train_set_pri: str
    ):
        """
        Sends a request to delete a data source.

        Parameters:
        - train_set_pri: int. The ID of the data source to be deleted.

        Returns:
        - A message indicating the outcome of the operation.
        """

        url = f"{BASE_URL_V2}/delete-data-source"
        data = {"train_set_pri": train_set_pri}
        headers = self.client.auth_headers

        try:
            response = httpx.post(url, headers=headers, json=data, timeout=300.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"Status code: {e.response.status_code}, Error: {e.response.text}"
            print(error_message)
        except Exception as e:
            raise e

    def delete_data_connector(self, data_connector_pri: str):
        """
        Sends a request to delete a data connector.

        Parameters:
        - conn_id: int. The ID of the data connector to be deleted.

        Returns:
        - A message indicating the outcome of the operation.
        """

        url = f"{BASE_URL_V2}/delete-data-connector"
        data = {"data_connector_pri": data_connector_pri}
        headers = self.client.auth_headers

        try:
            response = httpx.post(url, headers=headers, json=data, timeout=300.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"Status code: {e.response.status_code}, Error: {e.response.text}"
            print(error_message)
        except Exception as e:
            raise e


def _prepare_data_with_file(
    headers,
    train_set_name: str,
    file_path: str,
):
    url = f"{BASE_URL_V2}/create-data-source-with-file"

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    if 'Content-Type' in headers:
        headers.pop('Content-Type')

    data = {
        'data_source_name': train_set_name,
        'file_name': file_name,
        'file_size': str(file_size)
    }

    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            response = httpx.post(url, headers=headers, files=files, data=data, timeout=300.0)
            response.raise_for_status()
        print('Success:')
        result = response.json()
        res = result.get('data', {})

        filtered_res = {
            'created_at': res.get('created_at'),
            'created_by': res.get('created_by'),
            'train_set_pri': res.get('data_source_pri'),
        }
        return filtered_res
    except httpx.HTTPStatusError as e:
        # For responses with error status codes (4XX, 5XX)
        error_message = f"Status code: {e.response.status_code}, Error: {e.response.text}"
        print(error_message)
        raise httpx.HTTPStatusError(error_message, request=e.request, response=e.response)
    except Exception as e:
        raise e


def _prepare_data_with_connector(
    train_set_name: str,
    data_connection_pri: str,
    table_name: str,
    headers,
):
    url = f"{BASE_URL_V2}/create-data-source-with-connector"
    data = {
        'data_source_name': train_set_name,
        'data_connection_pri': data_connection_pri,
        'table_name': table_name
    }
    try:
        response = httpx.post(url, headers=headers, json=data, timeout=300.0)
        response.raise_for_status()
        result = response.json()
        res = result.get('data', {})

        filtered_res = {
            'created_at': res.get('created_at'),
            'created_by': res.get('created_by'),
            'train_set_pri': res.get('data_source_pri')
        }

        print(
            f'\033[38;2;85;87;93mData source creation successful:\033[0m \033[92m{response.status_code} {response.reason_phrase}\033[0m')

        return filtered_res
    except httpx.HTTPStatusError as e:
        error_message = f"Status code: {e.response.status_code}, Error: {e.response.text}"
        print(error_message)
    except Exception as e:
        raise e

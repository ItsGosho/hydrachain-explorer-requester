import logging
from typing import List

import requests
from requests import Session

from hydrachain_explorer_requester import __version__
from datetime import datetime

_logger = logging.getLogger(__name__)


class ResponseCodeError(Exception):
    """A not expected response code has been received."""


class ResponseBodyError(Exception):
    """A not expected response body has been received."""


class ExplorerRequester:
    def __init__(self,
                 logger=_logger,
                 timeout=None):
        self.request_user_agent = f'Hydrachain Explorer Requester/{__version__}'
        self.domain = "https://explorer.hydrachain.org"

        self.logger = logger
        self.session = Session()
        self.timeout = timeout
        pass

    def search(self, value: str) -> dict:
        url = f"{self.domain}/7001/search?query={value}"

        return self._request_explorer(url)

    def get_biggest_miners(self, page_number: int = 0, page_size: int = 20) -> dict:
        url = f"{self.domain}/7001/misc/biggest-miners?page={page_number}&pageSize={page_size}"

        return self._request_explorer(url)

    def get_rich_list(self, page_number: int = 0, page_size: int = 20) -> dict:
        url = f"{self.domain}/7001/misc/rich-list?page={page_number}&pageSize={page_size}"

        return self._request_explorer(url)

    def get_daily_transactions(self) -> dict:
        url = f"{self.domain}/7001/stats/daily-transactions"

        return self._request_explorer(url)

    def get_block_interval(self) -> dict:
        url = f"{self.domain}/7001/stats/block-interval"

        return self._request_explorer(url)

    def get_address_growth(self) -> dict:
        url = f"{self.domain}/7001/stats/address-growth"

        return self._request_explorer(url)

    def get_recent_blocks(self) -> dict:
        url = f"{self.domain}/7001/recent-blocks"

        return self._request_explorer(url)

    def get_recent_txs(self) -> dict:
        url = f"{self.domain}/7001/recent-txs"

        return self._request_explorer(url)

    def get_info(self) -> dict:
        url = f"{self.domain}/7001/info"

        return self._request_explorer(url)

    def get_block(self, number: int) -> dict:
        url = f"{self.domain}/7001/block/{number}"

        return self._request_explorer(url)

    def get_blocks(self, date: datetime) -> dict:
        date_format = "%Y-%m-%d"
        date_formatted = date.strftime(date_format)

        url = f"{self.domain}/7001/blocks?date={date_formatted}"

        return self._request_explorer(url)

    def get_tokens(self, page_number: int = 0, page_size: int = 20) -> dict:
        url = f"{self.domain}/7001/qrc20?page={page_number}&pageSize={page_size}"

        return self._request_explorer(url)

    def get_contract(self, contract: str) -> dict:
        url = f"{self.domain}/7001/contract/{contract}"

        return self._request_explorer(url)

    def get_contract_transactions(self, contract: str, page_number: int = 0, page_size: int = 20) -> dict:
        url = f"{self.domain}/7001/contract/{contract}/txs?page={page_number}&pageSize={page_size}"

        return self._request_explorer(url)

    def get_address(self, address: str) -> dict:
        url = f"{self.domain}/7001/address/{address}"

        return self._request_explorer(url)

    def get_address_transactions(self, address: str, page_number: int = 0, page_size: int = 20) -> dict:
        url = f"{self.domain}/7001/address/{address}/txs?page={page_number}&pageSize={page_size}"

        return self._request_explorer(url)

    def get_transaction(self, transaction) -> dict:
        url = f"{self.domain}/7001/tx/{transaction}"

        return self._request_explorer(url)

    def get_transactions(self, transactions: List[str]) -> dict:
        transactions_formatted = ','.join(transactions)
        url = f"{self.domain}/7001/txs/{transactions_formatted}"

        return self._request_explorer(url)


    def _request_explorer(self, url: str) -> dict:
        self.logger.debug(f"Starting a new hydrachain explorer request to {url}")

        response = self.session.get(
            url=url,
            headers=self._get_request_headers(),
            timeout=self.timeout
        )

        self._validate_response(response)

        self.logger.debug(
            f"Received a successful hydrachain explorer response to {response.url} with content {response.content}")

        return response.json()

    def _validate_response(self, response):
        self._validate_response_code(response)
        self._validate_response_content_type(response)

    def _validate_response_code(self, response):
        if response.status_code is not 200:
            raise ResponseCodeError(
                f"GET {response.url} responded with unexpected code {response.status_code} and content {response.content}")

    def _validate_response_content_type(self, response):
        if not 'application/json' in response.headers.get('content-type'):
            raise ResponseBodyError(
                f"GET {response.url} responded with code {response.status_code} and unexpected content {response.content}")

    def _get_request_headers(self) -> dict:
        return {'User-Agent': self.request_user_agent}

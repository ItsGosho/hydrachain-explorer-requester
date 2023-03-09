import logging
from typing import List, Callable
from urllib.parse import urlencode

import requests
from requests import Session
from requests.adapters import HTTPAdapter

from hydrachain_explorer_requester import __version__
from hydrachain_explorer_requester.enum import AddressBalanceCategory
from hydrachain_explorer_requester.explorer_url import ExplorerURL
from hydrachain_explorer_requester.query_parameters import *

_logger = logging.getLogger(__name__)


class ResponseCodeError(Exception):
    """
    A not expected response code has been received.
    We always expect response with code 200 from the Explorer's API.
    """


class ResponseBodyError(Exception):
    """
    A not expected response body has been received.
    We always expect a JSON response from the Explorer's API.
    """


class ExplorerRequester:
    """
    Easy-to-use class that provides function, which return data from the explorer's API.
    Optionally you can customize the logger or properties of the used requester.
    Data retrieved from the explorer is returned in raw format.
    """

    def __init__(self,
                 logger: logging = _logger,
                 timeout_seconds: float = None,
                 hooks: dict = None,
                 http_adapter: HTTPAdapter = HTTPAdapter(),
                 urls: ExplorerURL = ExplorerURL()
                 ):
        self.request_user_agent = f'Hydrachain Explorer Requester/{__version__}'

        self.logger = logger
        self.session = Session()
        self.timeout = timeout_seconds
        self.hooks = hooks
        self.http_adapter = http_adapter
        self.session.mount('http://', self.http_adapter)
        self.session.mount('https://', self.http_adapter)

        self.urls = urls

    def search(self,
               value: str
               ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_search_url(),
            params={'query': value}
        )

    def get_biggest_miners(self,
                           query_parameters: BiggestMinersQueryParameters = BiggestMinersQueryParameters()
                           ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_biggest_miners_url(),
            params={**query_parameters.pairs()}
        )

    def get_rich_list(self,
                      query_parameters: RichListQueryParameters = RichListQueryParameters()
                      ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_rich_list_url(),
            params={**query_parameters.pairs()}
        )

    def get_daily_transactions(self) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_daily_transactions_url()
        )

    def get_block_interval(self) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_block_interval_url()
        )

    def get_address_growth(self) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_address_growth_url()
        )

    def get_recent_blocks(self,
                          query_parameters: RecentBlocksQueryParameters = RecentBlocksQueryParameters()
                          ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_recent_blocks_url(),
            params={**query_parameters.pairs()}
        )

    def get_recent_txs(self) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_recent_txs_url()
        )

    def get_info(self) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_info_url()
        )

    def get_block(self,
                  value: str | int
                  ) -> dict:
        """
        :param value: height or hash
        """

        return self._request_explorer_json(
            url=self.urls.get_block_url(value)
        )

    def get_blocks(self,
                   query_parameters: BlocksQueryParameters = BlocksQueryParameters()
                   ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_blocks_url(),
            params={**query_parameters.pairs()}
        )

    def get_tokens(self,
                   query_parameters: TokensQueryParameters = TokensQueryParameters()
                   ) -> dict:
        return self._request_explorer_json(
            url=self.urls.get_tokens_url(),
            params={**query_parameters.pairs()}
        )

    def get_contract(self,
                     contract: str
                     ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_contract_url(contract)
        )

    def get_contract_transactions(self,
                                  contract: str,
                                  query_parameters: TransactionsQueryParameters = TransactionsQueryParameters()
                                  ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_contract_transactions_url(contract),
            params={**query_parameters.pairs()}
        )

    def get_contract_basic_transactions(self,
                                        contract: str,
                                        query_parameters: TransactionsQueryParameters = TransactionsQueryParameters()
                                        ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_contract_basic_transactions_url(contract),
            params={**query_parameters.pairs()}
        )

    def get_address(self,
                    address: str
                    ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_address_url(address)
        )

    def get_address_utxo(self,
                         address: str
                         ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_address_utxo_url(address)
        )

    def get_address_balance(self,
                            address: str,
                            category: AddressBalanceCategory = AddressBalanceCategory.NO_CATEGORY
                            ) -> str:
        return self._request_explorer_text(
            url=self.urls.get_address_balance_url(address, category)
        )

    def get_address_balance_history(self,
                                    address: str,
                                    query_parameters: AddressBalanceHistoryQueryParameters = AddressBalanceHistoryQueryParameters()
                                    ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_address_balance_history_url(address),
            params={**query_parameters.pairs()}
        )

    def get_address_qrc20_balance_history(self,
                                          address: str,
                                          query_parameters: AddressBalanceHistoryQueryParameters = AddressBalanceHistoryQueryParameters()
                                          ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_address_qrc20_balance_history_url(address),
            params={**query_parameters.pairs()}
        )

    def get_address_qrc20_balance_history_by_token(self,
                                                   address: str,
                                                   token: str,
                                                   query_parameters: AddressBalanceHistoryQueryParameters = AddressBalanceHistoryQueryParameters()
                                                   ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_address_qrc20_balance_history_by_token_url(address, token),
            params={**query_parameters.pairs()}
        )

    def get_address_transactions(self,
                                 address: str,
                                 query_parameters: TransactionsQueryParameters = TransactionsQueryParameters()
                                 ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_address_transactions_url(address),
            params={**query_parameters.pairs()}
        )

    def get_address_qrc20_transactions(self,
                                       address: str,
                                       token: str,
                                       query_parameters: TransactionsQueryParameters = TransactionsQueryParameters()
                                       ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_address_qrc20_transactions_url(address, token),
            params={**query_parameters.pairs()}
        )

    def get_address_basic_transactions(self,
                                       address: str,
                                       query_parameters: TransactionsQueryParameters = TransactionsQueryParameters()
                                       ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_address_basic_transactions_url(address),
            params={**query_parameters.pairs()}
        )

    def get_address_contract_transactions(self,
                                          address: str,
                                          query_parameters: TransactionsQueryParameters = TransactionsQueryParameters()
                                          ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_address_contract_transactions_url(address),
            params={**query_parameters.pairs()}
        )

    def get_address_contract_transactions_by_contract(self,
                                                      address: str,
                                                      contract: str,
                                                      query_parameters: TransactionsQueryParameters = TransactionsQueryParameters()
                                                      ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_address_contract_transactions_by_contract_url(address, contract),
            params={**query_parameters.pairs()}
        )

    def get_transaction(self,
                        transaction: str
                        ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_transaction_url(transaction)
        )

    def get_raw_transaction(self,
                            transaction: str
                            ) -> str:

        return self._request_explorer_text(
            url=self.urls.get_raw_transaction_url(transaction)
        )

    def get_transactions(self, transactions: List[str]) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_transactions_url(transactions)
        )

    def call_contract(self,
                      contract: str,
                      query_parameters: CallContractQueryParameters = CallContractQueryParameters()
                      ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_call_contract_url(contract),
            params={**query_parameters.pairs()}
        )

    def get_search_logs(self,
                        query_parameters: SearchLogsQueryParameters = SearchLogsQueryParameters()
                        ) -> dict:

        return self._request_explorer_json(
            url=self.urls.get_search_logs_url(),
            params={**query_parameters.pairs()}
        )

    def _request_explorer_json(self,
                               url: str,
                               params: dict = {},
                               method: str = 'GET',
                               ) -> dict:
        response = self._request_explorer(url, params, method)
        self._validate_response(response)
        return response.json()

    def _request_explorer_text(self,
                               url: str,
                               params: dict = {},
                               method: str = 'GET',
                               ) -> str:
        response = self._request_explorer(url, params, method)
        return response.text

    def _request_explorer(self,
                          url: str,
                          params: dict = {},
                          method: str = 'GET',
                          ):

        request = requests.Request(
            method=method,
            url=url,
            headers=self._get_request_headers(),
            params=params,
            hooks=self.hooks
        )

        self.logger.debug(f'Starting a new hydrachain explorer request to {request.url}?{urlencode(request.params)}')

        prepared_request = self.session.prepare_request(request)
        response = self.session.send(
            request=prepared_request,
            timeout=self.timeout
        )

        self.logger.debug(
            f'Received a hydrachain explorer response from {response.url} with content {response.content}')

        return response

    def _validate_response(self, response):
        self._validate_response_code(response)
        self._validate_response_content_type(response)

    def _validate_response_code(self, response):
        if response.status_code != 200:
            raise ResponseCodeError(
                f'GET {response.url} responded with unexpected code {response.status_code} and content {response.content}')

    def _validate_response_content_type(self, response):
        if not 'application/json' in response.headers.get('content-type'):
            raise ResponseBodyError(
                f'GET {response.url} responded with code {response.status_code} and unexpected content {response.content}')

    def _get_request_headers(self) -> dict:
        return {'User-Agent': self.request_user_agent}

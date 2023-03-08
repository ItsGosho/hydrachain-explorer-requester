import logging
from typing import List, Callable
from urllib.parse import urlencode

import requests
from requests import Session
from requests.adapters import HTTPAdapter

from hydrachain_explorer_requester import __version__
from datetime import datetime

from hydrachain_explorer_requester.address_balance_category import AddressBalanceCategory
from hydrachain_explorer_requester.query_parameters.address_balance_history_query_parameters import \
    AddressBalanceHistoryQueryParameters
from hydrachain_explorer_requester.query_parameters.address_basic_transactions_query_parameters import \
    AddressBasicTransactionsQueryParameters
from hydrachain_explorer_requester.query_parameters.address_contract_transactions_query_parameters import \
    AddressContractTransactionsQueryParameters
from hydrachain_explorer_requester.query_parameters.address_transactions_query_parameters import \
    AddressTransactionsQueryParameters
from hydrachain_explorer_requester.query_parameters.biggest_miners_query_parameters import BiggestMinersQueryParameters
from hydrachain_explorer_requester.query_parameters.blocks_query_parameters import BlocksQueryParameters
from hydrachain_explorer_requester.query_parameters.contract_transactions_query_parameters import \
    ContractTransactionsQueryParameters
from hydrachain_explorer_requester.query_parameters.pagination_query_parameters import PaginationQueryParameters
from hydrachain_explorer_requester.query_parameters.recent_blocks_query_parameters import RecentBlocksQueryParameters
from hydrachain_explorer_requester.query_parameters.rich_list_query_parameters import RichListQueryParameters
from hydrachain_explorer_requester.query_parameters.tokens_query_parameters import TokensQueryParameters

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
                 http_adapter: HTTPAdapter = HTTPAdapter()):
        self.request_user_agent = f'Hydrachain Explorer Requester/{__version__}'
        self.domain = 'https://explorer.hydrachain.org'

        self.logger = logger
        self.session = Session()
        self.timeout = timeout_seconds
        self.hooks = hooks
        self.http_adapter = http_adapter
        self.session.mount('http://', self.http_adapter)
        self.session.mount('https://', self.http_adapter)

    def search(self,
               value: str
               ) -> dict:

        return self._request_explorer_json(
            path='/7001/search',
            params={
                'query': value
            }
        )

    def get_biggest_miners(self,
                           query_parameters: BiggestMinersQueryParameters = BiggestMinersQueryParameters()
                           ) -> dict:

        return self._request_explorer_json(
            path='/7001/misc/biggest-miners',
            params={
                **self.get_pagination_query_parameters(query_parameters)
            }
        )

    def get_biggest_miners_iterator(self, request_portion: int = 20):

        return self._pageable_iterator(
            function=self.get_biggest_miners,
            data_field='list',
            request_portion=request_portion
        )

    def get_rich_list(self,
                      query_parameters: RichListQueryParameters = RichListQueryParameters()
                      ) -> dict:

        return self._request_explorer_json(
            path='/7001/misc/rich-list',
            params={
                **self.get_pagination_query_parameters(query_parameters)
            }
        )

    def get_rich_list_iterator(self,
                               request_portion: int = 20
                               ):

        return self._pageable_iterator(
            function=self.get_rich_list,
            data_field='list',
            request_portion=request_portion
        )

    def get_daily_transactions(self) -> dict:

        return self._request_explorer_json(
            path='/7001/stats/daily-transactions'
        )

    def get_block_interval(self) -> dict:

        return self._request_explorer_json(
            path='/7001/stats/block-interval'
        )

    def get_address_growth(self) -> dict:

        return self._request_explorer_json(
            path='/7001/stats/address-growth'
        )

    def get_recent_blocks(self,
                          query_parameters: RecentBlocksQueryParameters = RecentBlocksQueryParameters()
                          ) -> dict:

        return self._request_explorer_json(
            path='/7001/recent-blocks',
            params={
                **query_parameters.count.pair()
            }
        )

    def get_recent_txs(self) -> dict:

        return self._request_explorer_json(
            path='/7001/recent-txs'
        )

    def get_info(self) -> dict:

        return self._request_explorer_json(
            path='/7001/info'
        )

    def get_block(self,
                  value: str | int
                  ) -> dict:
        """
        :param value: height or hash
        """

        return self._request_explorer_json(
            path=f'/7001/block/{value}'
        )

    def get_blocks(self,
                   query_parameters: BlocksQueryParameters = BlocksQueryParameters()
                   ) -> dict:

        return self._request_explorer_json(
            path='/7001/blocks',
            params={
                **query_parameters.date.pair()
            }
        )

    def get_tokens(self,
                   query_parameters: TokensQueryParameters = TokensQueryParameters()
                   ) -> dict:
        return self._request_explorer_json(
            path='/7001/qrc20',
            params={
                **self.get_pagination_query_parameters(query_parameters)
            }
        )

    def get_tokens_iterator(self,
                            request_portion: int = 20
                            ):

        return self._pageable_iterator(
            function=self.get_tokens,
            data_field='tokens',
            request_portion=request_portion
        )

    def get_contract(self,
                     contract: str
                     ) -> dict:

        return self._request_explorer_json(
            path=f'/7001/contract/{contract}'
        )

    def get_contract_transactions(self,
                                  contract: str,
                                  query_parameters: ContractTransactionsQueryParameters = ContractTransactionsQueryParameters()
                                  ) -> dict:

        return self._request_explorer_json(
            path=f'/7001/contract/{contract}/txs',
            params={
                **self.get_pagination_query_parameters(query_parameters)
            }
        )

    def get_contract_transactions_iterator(self,
                                           contract: str,
                                           request_portion: int = 20
                                           ):

        return self._pageable_iterator(
            function=self.get_contract_transactions,
            external_arguments={'contract': contract},
            data_field='transactions',
            request_portion=request_portion
        )

    def get_address(self,
                    address: str
                    ) -> dict:

        return self._request_explorer_json(
            path=f'/7001/address/{address}'
        )

    def get_address_utxo(self,
                         address: str
                         ) -> dict:

        return self._request_explorer_json(
            path=f'/7001/address/{address}/utxo'
        )

    def get_address_balance(self,
                            address: str,
                            category: AddressBalanceCategory = AddressBalanceCategory.NO_CATEGORY
                            ) -> str:
        return self._request_explorer_text(
            path=f'/7001/address/{address}/balance/{category.value}',
        )

    def get_address_balance_history(self,
                                    address: str,
                                    query_parameters: AddressBalanceHistoryQueryParameters = AddressBalanceHistoryQueryParameters()
                                    ) -> dict:

        return self._request_explorer_json(
            path=f'/7001/address/{address}/balance-history',
            params={
                **self.get_pagination_query_parameters(query_parameters)
            }
        )

    def get_address_balance_history_iterator(self,
                                             address: str,
                                             request_portion: int = 20
                                             ):

        return self._pageable_iterator(
            function=self.get_address_balance_history,
            external_arguments={'address': address},
            data_field='transactions',
            request_portion=request_portion
        )

    def get_address_qrc20_balance_history(self,
                                          address: str,
                                          query_parameters: AddressBalanceHistoryQueryParameters = AddressBalanceHistoryQueryParameters()
                                          ) -> dict:

        return self._request_explorer_json(
            path=f'/7001/address/{address}/qrc20-balance-history',
            params={
                **self.get_pagination_query_parameters(query_parameters)
            }
        )

    def get_address_qrc20_balance_history_iterator(self,
                                                   address: str,
                                                   request_portion: int = 20
                                                   ):

        return self._pageable_iterator(
            function=self.get_address_qrc20_balance_history,
            external_arguments={'address': address},
            data_field='transactions',
            request_portion=request_portion
        )

    def get_address_qrc20_balance_history_by_token(self,
                                                   address: str,
                                                   token: str,
                                                   query_parameters: AddressBalanceHistoryQueryParameters = AddressBalanceHistoryQueryParameters()
                                                   ) -> dict:

        return self._request_explorer_json(
            path=f'/7001/address/{address}/qrc20-balance-history/{token}',
            params={
                **self.get_pagination_query_parameters(query_parameters)
            }
        )

    def get_address_qrc20_balance_history_by_token_iterator(self,
                                                            address: str,
                                                            token: str,
                                                            request_portion: int = 20
                                                            ):

        return self._pageable_iterator(
            function=self.get_address_qrc20_balance_history_by_token,
            external_arguments={'address': address, 'token': token},
            data_field='transactions',
            request_portion=request_portion
        )

    def get_address_transactions(self,
                                 address: str,
                                 query_parameters: AddressTransactionsQueryParameters = AddressTransactionsQueryParameters()
                                 ) -> dict:

        return self._request_explorer_json(
            path=f'/7001/address/{address}/txs',
            params={
                **self.get_pagination_query_parameters(query_parameters)
            }
        )

    def get_address_transactions_iterator(self,
                                          address: str,
                                          request_portion: int = 20
                                          ):

        return self._pageable_iterator(
            function=self.get_address_transactions,
            external_arguments={'address': address},
            data_field='transactions',
            request_portion=request_portion
        )

    def get_address_basic_transactions(self,
                                       address: str,
                                       query_parameters: AddressBasicTransactionsQueryParameters = AddressBasicTransactionsQueryParameters()
                                       ) -> dict:

        return self._request_explorer_json(
            path=f'/7001/address/{address}/basic-txs',
            params={
                **self.get_pagination_query_parameters(query_parameters)
            }
        )

    def get_address_basic_transactions_iterator(self,
                                                address: str,
                                                request_portion: int = 20
                                                ):

        return self._pageable_iterator(
            function=self.get_address_basic_transactions,
            external_arguments={'address': address},
            data_field='transactions',
            request_portion=request_portion
        )

    def get_address_contract_transactions(self,
                                          address: str,
                                          query_parameters: AddressContractTransactionsQueryParameters = AddressContractTransactionsQueryParameters()
                                          ) -> dict:

        return self._request_explorer_json(
            path=f'/7001/address/{address}/contract-txs',
            params={
                **self.get_pagination_query_parameters(query_parameters)
            }
        )

    def get_address_contract_transactions_iterator(self,
                                                   address: str,
                                                   request_portion: int = 20
                                                   ):

        return self._pageable_iterator(
            function=self.get_address_contract_transactions,
            external_arguments={'address': address},
            data_field='transactions',
            request_portion=request_portion
        )

    def get_address_contract_transactions_by_contract(self,
                                                      address: str,
                                                      contract: str,
                                                      query_parameters: AddressContractTransactionsQueryParameters = AddressContractTransactionsQueryParameters()
                                                      ) -> dict:

        return self._request_explorer_json(
            path=f'/7001/address/{address}/contract-txs/{contract}',
            params={
                **self.get_pagination_query_parameters(query_parameters)
            }
        )

    def get_address_contract_transactions_by_contract_iterator(self,
                                                               address: str,
                                                               contract: str,
                                                               request_portion: int = 20
                                                               ):

        return self._pageable_iterator(
            function=self.get_address_contract_transactions_by_contract,
            external_arguments={'address': address, 'contract': contract},
            data_field='transactions',
            request_portion=request_portion
        )

    def get_transaction(self,
                        transaction
                        ) -> dict:

        return self._request_explorer_json(
            path=f'/7001/tx/{transaction}'
        )

    def get_raw_transaction(self,
                            transaction
                            ) -> str:

        return self._request_explorer_text(
            path=f'/7001/raw-tx/{transaction}'
        )

    def get_transactions(self,
                         transactions: List[str]
                         ) -> dict:
        transactions_formatted = ','.join(transactions)

        return self._request_explorer_json(
            path=f'/7001/txs/{transactions_formatted}'
        )

    def _pageable_iterator(self,
                           function: Callable,
                           data_field: str,
                           external_arguments: dict = {},
                           request_portion: int = 20
                           ):
        """
        Easy-to-use wrapper for removing repeating logic, when calling a functions that have pageable.

        :param function: A function, that have query_parameters argument, which is a class of type PaginationQueryParameters or inheritor of it and returns a dict, when called.
        :param data_field: A field in the returned dict, when the function was called, which contains array of data.
        :param external_arguments: Additional arguments of the functions.
        :param request_portion: How many data to fetch at once
        """
        page_number = 0
        while True:

            pagination_query_parameter = PaginationQueryParameters()
            pagination_query_parameter.set_page(page_number)
            pagination_query_parameter.set_page_size(request_portion)

            external_arguments['query_parameters'] = pagination_query_parameter

            response = function(**external_arguments)

            data = response[data_field]

            if len(data) <= 0:
                break

            for d in data:
                yield d

            page_number = page_number + 1

    def _request_explorer_json(self,
                               path: str,
                               params: dict = {},
                               domain: str = None,
                               method: str = 'GET',
                               ) -> dict:
        response = self._request_explorer(path, params, domain, method)
        self._validate_response(response)
        return response.json()

    def _request_explorer_text(self,
                               path: str,
                               params: dict = {},
                               domain: str = None,
                               method: str = 'GET',
                               ) -> str:
        response = self._request_explorer(path, params, domain, method)
        return response.text

    def _request_explorer(self,
                          path: str,
                          params: dict = {},
                          domain: str = None,
                          method: str = 'GET',
                          ):

        request = requests.Request(
            method=method,
            url=f'{domain or self.domain}{path}',
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

    def get_pagination_query_parameters(self,
                                        query_parameters: PaginationQueryParameters = PaginationQueryParameters()
                                        ):
        """
        Some requests in the explorer are pageable and thus accept pagination query parameters.
        These pagination parameters have requirements. You can't pass them as you want.
        The rules are as follows:
        limit and offset must be passed together if one of them is present.
        from and to must be passed together if one of them is present.
        pageSize and page must be passed together if one of them is present.
        You can't pass different groups like limit and offset with from and to.
        Thus, we make priority.
        1. pageSize and page
        2. limit and offset
        3. from and to
        If you pass multiple groups, only the first one from the priority list will be taken.
        """
        if query_parameters is None:
            return {}

        if query_parameters.is_page_size_page():
            return {
                **query_parameters.page.pair(),
                **query_parameters.page_size.pair()
            }

        if query_parameters.is_from_to_set():
            return {
                **query_parameters.from_.pair(),
                **query_parameters.to.pair()
            }

        if query_parameters.is_limit_offset_set():
            return {
                **query_parameters.limit.pair(),
                **query_parameters.offset.pair()
            }

        return {}

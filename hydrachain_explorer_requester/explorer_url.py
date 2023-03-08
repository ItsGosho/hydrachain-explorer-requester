from typing import List

from hydrachain_explorer_requester.enum import AddressBalanceCategory


class ExplorerURL:

    def __init__(self,
                 domain: str = 'https://explorer.hydrachain.org',
                 base_path: str = '/7001'
                 ):
        self.domain = domain
        self.base_path = base_path

    def get_search_url(self) -> str:
        return f'{self.domain}{self.base_path}/search'

    def get_biggest_miners_url(self) -> str:
        return f'{self.domain}{self.base_path}/misc/biggest-miners'

    def get_rich_list_url(self) -> str:
        return f'{self.domain}{self.base_path}/misc/rich-list'

    def get_daily_transactions_url(self) -> str:
        return f'{self.domain}{self.base_path}/stats/daily-transactions'

    def get_block_interval_url(self) -> str:
        return f'{self.domain}{self.base_path}/stats/block-interval'

    def get_address_growth_url(self) -> str:
        return f'{self.domain}{self.base_path}/stats/address-growth'

    def get_recent_blocks_url(self) -> str:
        return f'{self.domain}{self.base_path}/recent-blocks'

    def get_recent_txs_url(self) -> str:
        return f'{self.domain}{self.base_path}/recent-txs'

    def get_info_url(self) -> str:
        return f'{self.domain}{self.base_path}/info'

    def get_block_url(self, value: str | int) -> str:
        return f'{self.domain}{self.base_path}/block/{value}'

    def get_blocks_url(self) -> str:
        return f'{self.domain}{self.base_path}/blocks'

    def get_tokens_url(self) -> str:
        return f'{self.domain}{self.base_path}/qrc20'

    def get_contract_url(self, contract: str) -> str:
        return f'{self.domain}{self.base_path}/contract/{contract}'

    def get_contract_transactions_url(self, contract: str) -> str:
        return f'{self.domain}{self.base_path}/contract/{contract}/txs'

    def get_contract_basic_transactions_url(self, contract: str) -> str:
        return f'{self.domain}{self.base_path}/contract/{contract}/basic-txs'

    def get_address_url(self, address: str) -> str:
        return f'{self.domain}{self.base_path}/address/{address}'

    def get_address_utxo_url(self, address: str) -> str:
        return f'{self.domain}{self.base_path}/address/{address}/utxo'

    def get_address_balance_url(self, address: str,
                                category: AddressBalanceCategory = AddressBalanceCategory.NO_CATEGORY
                                ) -> str:
        return f'{self.domain}{self.base_path}/address/{address}/balance/{category.value}'

    def get_address_balance_history_url(self, address: str) -> str:
        return f'{self.domain}{self.base_path}/address/{address}/balance-history'

    def get_address_qrc20_balance_history_url(self, address: str) -> str:
        return f'{self.domain}{self.base_path}/address/{address}/qrc20-balance-history'

    def get_address_qrc20_balance_history_by_token_url(self,
                                                       address: str,
                                                       token: str
                                                       ) -> str:
        return f'{self.domain}{self.base_path}/address/{address}/qrc20-balance-history/{token}'

    def get_address_transactions_url(self, address: str) -> str:
        return f'{self.domain}{self.base_path}/address/{address}/txs'

    def get_address_qrc20_transactions_url(self,
                                           address: str,
                                           token: str
                                           ) -> str:
        return f'{self.domain}{self.base_path}/address/{address}/qrc20-txs/{token}'

    def get_address_basic_transactions_url(self, address: str) -> str:
        return f'{self.domain}{self.base_path}/address/{address}/basic-txs'

    def get_address_contract_transactions_url(self, address: str) -> str:
        return f'{self.domain}{self.base_path}/address/{address}/contract-txs'

    def get_address_contract_transactions_by_contract_url(self,
                                                          address: str,
                                                          contract: str
                                                          ) -> str:
        return f'{self.domain}{self.base_path}/address/{address}/contract-txs/{contract}'

    def get_transaction_url(self, transaction: str) -> str:
        return f'{self.domain}{self.base_path}/tx/{transaction}'

    def get_raw_transaction_url(self, transaction: str) -> str:
        return f'{self.domain}{self.base_path}/raw-tx/{transaction}'

    def get_transactions_url(self, transactions: List[str]) -> str:
        transactions_separated_by_comma = ','.join(transactions)
        return f'{self.domain}{self.base_path}/txs/{transactions_separated_by_comma}'

    def get_call_contract_url(self, contract: str) -> str:
        return f'{self.domain}{self.base_path}/contract/{contract}/call'

    def get_search_logs_url(self) -> str:
        return f'{self.domain}{self.base_path}/searchlogs'
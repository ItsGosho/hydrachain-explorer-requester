from dataclasses import dataclass, field

from hydrachain_explorer_requester.query_parameters.block_query_parameters import BlockQueryParameters
from hydrachain_explorer_requester.query_parameters.query_parameter import QueryParameter
from hydrachain_explorer_requester.query_parameters.pagination_query_parameters import PaginationQueryParameters


@dataclass
class AddressBalanceHistoryQueryParameters(PaginationQueryParameters):
    reversed: QueryParameter = field(default_factory=lambda: QueryParameter('reversed', None))

    def set_reversed(self, reversed: str):
        self.reversed.value = reversed

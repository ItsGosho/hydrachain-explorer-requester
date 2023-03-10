from dataclasses import dataclass, field

from hydrachain_explorer_requester.query_parameters.query_parameter import QueryParameter
from hydrachain_explorer_requester.query_parameters.pagination_query_parameters import PaginationQueryParameters


@dataclass
class TokensQueryParameters(PaginationQueryParameters):
    def pairs(self) -> dict:
        return {
            **PaginationQueryParameters.pairs(self)
        }

from dataclasses import dataclass, field

from hydrachain_explorer_requester.query_parameters.query_parameter import QueryParameter
from hydrachain_explorer_requester.query_parameters.pagination_query_parameters import PaginationQueryParameters


@dataclass
class RecentBlocksQueryParameters:
    count: QueryParameter = field(default_factory=lambda: QueryParameter('count', None))

    def set_count(self, count: int):
        self.count.value = count

    def pairs(self) -> dict:
        return {
            **self.count.pair()
        }

from dataclasses import dataclass, field

from hydrachain_explorer_requester.query_parameters.block_query_parameters import BlockQueryParameters
from hydrachain_explorer_requester.query_parameters.query_parameter import QueryParameter
from hydrachain_explorer_requester.query_parameters.pagination_query_parameters import PaginationQueryParameters


@dataclass
class SearchLogsQueryParameters(PaginationQueryParameters, BlockQueryParameters):
    contract: QueryParameter = field(default_factory=lambda: QueryParameter('contract', None))
    topic1: QueryParameter = field(default_factory=lambda: QueryParameter('topic1', None))
    topic2: QueryParameter = field(default_factory=lambda: QueryParameter('topic2', None))
    topic3: QueryParameter = field(default_factory=lambda: QueryParameter('topic3', None))
    topic4: QueryParameter = field(default_factory=lambda: QueryParameter('topic4', None))

    def set_contract(self, contract: str):
        self.contract.value = contract

    def set_topic1(self, topic1: str):
        self.topic1.value = topic1

    def set_topic2(self, topic2: str):
        self.topic2.value = topic2

    def set_topic3(self, topic3: str):
        self.topic3.value = topic3

    def set_topic4(self, topic4: str):
        self.topic4.value = topic4

    def pairs(self) -> dict:
        return {
            **PaginationQueryParameters.pairs(self),
            **BlockQueryParameters.pairs(self),
            **self.contract.pair(),
            **self.topic1.pair(),
            **self.topic2.pair(),
            **self.topic3.pair(),
            **self.topic4.pair(),
        }

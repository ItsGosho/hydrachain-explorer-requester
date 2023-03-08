from dataclasses import dataclass, field

from hydrachain_explorer_requester.query_parameters.block_query_parameters import BlockQueryParameters
from hydrachain_explorer_requester.query_parameters.query_parameter import QueryParameter
from hydrachain_explorer_requester.query_parameters.pagination_query_parameters import PaginationQueryParameters


@dataclass
class CallContractQueryParameters:
    data: QueryParameter = field(default_factory=lambda: QueryParameter('data', None))
    sender: QueryParameter = field(default_factory=lambda: QueryParameter('sender', None))

    def set_data(self, data: str):
        self.data.value = data

    def set_sender(self, sender: str):
        self.sender.value = sender

    def pairs(self) -> dict:
        return {
            **self.data.pair(),
            **self.sender.pair()
        }

from dataclasses import dataclass, field
from datetime import datetime

from hydrachain_explorer_requester.query_parameters.query_parameter import QueryParameter


@dataclass
class BlockQueryParameters:
    from_block: QueryParameter = field(default_factory=lambda: QueryParameter('fromBlock', None))
    to_block: QueryParameter = field(default_factory=lambda: QueryParameter('toBlock', None))
    from_time: QueryParameter = field(default_factory=lambda: QueryParameter('fromTime', None))
    to_time: QueryParameter = field(default_factory=lambda: QueryParameter('toTime', None))

    def set_from_block(self, from_block: int):
        self.from_block.value = from_block

    def set_to_block(self, to_block: int):
        self.to_block.value = to_block

    def set_from_time(self, from_time: datetime):
        self.from_time.value = from_time.isoformat()

    def set_to_time(self, to_time: datetime):
        self.to_time.value = to_time.isoformat()

    def pairs(self) -> dict:
        return {
            **self.from_block.pair(),
            **self.to_block.pair(),
            **self.from_time.pair(),
            **self.to_time.pair(),
        }

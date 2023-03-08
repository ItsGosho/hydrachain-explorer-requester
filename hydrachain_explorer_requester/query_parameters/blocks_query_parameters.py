from dataclasses import dataclass, field
from datetime import datetime

from hydrachain_explorer_requester.query_parameters.query_parameter import QueryParameter
from hydrachain_explorer_requester.query_parameters.pagination_query_parameters import PaginationQueryParameters


@dataclass
class BlocksQueryParameters:
    date: QueryParameter = field(default_factory=lambda: QueryParameter('date', None))

    def set_date(self, date: datetime.date):
        self.date.value = date.strftime('%Y-%m-%d')

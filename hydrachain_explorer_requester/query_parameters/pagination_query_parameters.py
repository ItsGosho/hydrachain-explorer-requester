from dataclasses import dataclass, field

from hydrachain_explorer_requester.query_parameters.query_parameter import QueryParameter

@dataclass
class PaginationQueryParameters:
    limit: QueryParameter = field(default_factory=lambda: QueryParameter('limit', None))
    offset: QueryParameter = field(default_factory=lambda: QueryParameter('offset', None))
    from_: QueryParameter = field(default_factory=lambda: QueryParameter('from', None))
    to: QueryParameter = field(default_factory=lambda: QueryParameter('to', None))
    page_size: QueryParameter = field(default_factory=lambda: QueryParameter('pageSize', None))
    page: QueryParameter = field(default_factory=lambda: QueryParameter('page', None))

    def set_limit(self, limit: int):
        self.limit.value = limit

    def set_offset(self, offset: int):
        self.offset.value = offset

    def set_from(self, from_: int):
        self.from_.value = from_

    def set_to(self, to: int):
        self.to.value = to

    def set_page_size(self, page_size: int):
        self.page_size.value = page_size

    def set_page(self, page: int):
        self.page.value = page

    def is_limit_offset_set(self) -> bool:
        return self.limit.is_set() and self.offset.is_set()

    def is_from_to_set(self) -> bool:
        return self.from_.is_set() and self.to.is_set()

    def is_page_size_page(self) -> bool:
        return self.page_size.is_set() and self.page.is_set()

    def pairs(self) -> dict:
        return {
            **self.limit.pair(),
            **self.offset.pair(),
            **self.from_.pair(),
            **self.to.pair(),
            **self.page_size.pair(),
            **self.page.pair(),
        }

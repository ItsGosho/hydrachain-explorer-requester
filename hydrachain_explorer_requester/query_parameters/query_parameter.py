from dataclasses import dataclass


@dataclass
class QueryParameter:
    name: str
    value: str

    def pair(self) -> dict:
        """
        Useful for unpacking, where you need to construct multiple query parameters in a json object.
        If the query parameter's value wasn't set a {} will be returned.

        Example:
        name: pageSize
        value: 20

        Return will be {'pageSize': '20'}
        """

        if self.is_set():
            return {self.name: self.value}

        return {}

    def is_set(self) -> bool:
        return self.value is not None
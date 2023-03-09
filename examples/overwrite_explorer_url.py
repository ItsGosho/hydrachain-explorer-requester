import logging

from hydrachain_explorer_requester.explorer_requester import ExplorerRequester
from hydrachain_explorer_requester.explorer_url import ExplorerURL

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ExplorerURLCustom(ExplorerURL):

    def get_address_transactions_url(self, address: str) -> str:
        return f'http://localhost:5555/address/{address}'


explorer_url_custom = ExplorerURLCustom()
explorer_requester = ExplorerRequester(
    urls=explorer_url_custom
)

# Address - https://explorer.hydrachain.org/address/HCiMdPYCsdPPvbjxHQMmK8QVBEGwextvir/
address_transactions = explorer_requester.get_address_transactions("HCiMdPYCsdPPvbjxHQMmK8QVBEGwextvir")

logger.info(address_transactions)

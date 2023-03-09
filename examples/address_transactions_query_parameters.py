import logging

from hydrachain_explorer_requester.explorer_requester import ExplorerRequester
from hydrachain_explorer_requester.query_parameters import TransactionsQueryParameters

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

explorer_requester = ExplorerRequester()

# Address - https://explorer.hydrachain.org/address/HCiMdPYCsdPPvbjxHQMmK8QVBEGwextvir/

query_parameters = TransactionsQueryParameters()
query_parameters.set_page(0)
query_parameters.set_page_size(3)
query_parameters.set_from(555555)
query_parameters.set_to_block(666666)
address_transactions = explorer_requester.get_address_transactions("HCiMdPYCsdPPvbjxHQMmK8QVBEGwextvir", query_parameters)

logger.info(address_transactions)

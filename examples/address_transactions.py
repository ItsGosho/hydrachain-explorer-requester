import logging

from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

explorer_requester = ExplorerRequester()

# Address - https://explorer.hydrachain.org/address/HCiMdPYCsdPPvbjxHQMmK8QVBEGwextvir/
address_transactions_iterator = explorer_requester.get_address_transactions_iterator("HCiMdPYCsdPPvbjxHQMmK8QVBEGwextvir")

for address_transactions_response in address_transactions_iterator:
    logger.info(address_transactions_response)

import logging

from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

explorer_requester = ExplorerRequester()

address_transactions_iterator = explorer_requester.get_address_transactions_iterator("H7FYCLijimtbYk7gdN1hmweftuWLQni3m5")

for address_transactions_response in address_transactions_iterator:
    logger.info(address_transactions_response)

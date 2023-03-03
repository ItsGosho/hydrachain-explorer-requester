import logging

from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

explorer_requester = ExplorerRequester()

# Block - https://explorer.hydrachain.org/block/123/
block_response = explorer_requester.get_block(123)

logger.info(block_response)

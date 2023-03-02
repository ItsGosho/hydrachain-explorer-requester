import logging

import requests
from requests.adapters import HTTPAdapter

import hydrachain_explorer_requester
from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#Configure the used requester
timeout_seconds = 0.5 # 500 milliseconds
http_adapter = HTTPAdapter(
    pool_connections=requests.adapters.DEFAULT_POOLSIZE,
    pool_maxsize=requests.adapters.DEFAULT_POOLSIZE,
    max_retries=3,
    pool_block=requests.adapters.DEFAULT_POOLBLOCK,
)

#Place the configured requester configuration
explorer_requester = ExplorerRequester(
    timeout_seconds = timeout_seconds,
    http_adapter=http_adapter
)

# Configure the level of logging.
hydrachain_explorer_requester.explorer_requester._logger.setLevel(logging.INFO)

block = explorer_requester.get_block(1234)
logger.info(block)

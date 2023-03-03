# Hydrachain Explorer Requester
Easy to use library for accessing the [Hydrachain Explorer](https://explorer.hydrachain.org/) endpoints. Functionality for easy iteration over the pageable requests is provided. Optional configuration of the used requester in the library is also provided. Validation of the response is present.

## Installation

#### PyPI:

```
pip install TODO
```

#### Local:

Download the [latest release](https://github.com/ItsGosho/hydrachain-explorer-requester/releases) and run the below command to install it globally:

```
pip install .
```

## Examples

#### Block:

```python
import logging
from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

explorer_requester = ExplorerRequester()

# Block - https://explorer.hydrachain.org/block/123/
block_response = explorer_requester.get_block(123)

logger.info(block_response)
```

#### Address Transactions: 

```python
import logging

from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

explorer_requester = ExplorerRequester()

# Address - https://explorer.hydrachain.org/address/H7FYCLijimtbYk7gdN1hmweftuWLQni3m5/
address_transactions_iterator = explorer_requester.get_address_transactions_iterator("H7FYCLijimtbYk7gdN1hmweftuWLQni3m5")

for address_transactions_response in address_transactions_iterator:
    logger.info(address_transactions_response)
```

- **_iterator** ending functions accept a optional **portion** parameter. The **portion** parameter define how much elements to be taken, when making each request.
  - Multiple requests are needed, because some of the explorer's requests use **pagination**. If you don't want to use the **_iterator** - you can use the standard function. For the example above, the standard function will be `get_address_transactions`

#### Search:

```python
import logging

from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def search(value: str) -> dict:
    search_response = explorer_requester.search(value)

    if 'type' not in search_response:
        return {}

    type = search_response['type']
    match type:
        case 'block':
            return explorer_requester.get_block(int(value))
        case 'transaction':
            return explorer_requester.get_transaction(value)
        case 'address':
            return explorer_requester.get_address(value)
        case 'contract':
            address = search_response['address']
            return explorer_requester.get_contract(address)
        case _:
            logger.warning(f'Type {type} not implemented!')
            return {}


explorer_requester = ExplorerRequester()

# Block - https://explorer.hydrachain.org/block/1234
print(search('1234'))

# Transaction - https://explorer.hydrachain.org/tx/23ebd8cb30e701b1dce693bb427092dcbf7091dd5cb263d9962b9245a38662f6
print(search('23ebd8cb30e701b1dce693bb427092dcbf7091dd5cb263d9962b9245a38662f6'))

# Address - https://explorer.hydrachain.org/address/H7FYCLijimtbYk7gdN1hmweftuWLQni3m5
print(search('H7FYCLijimtbYk7gdN1hmweftuWLQni3m5'))

# Contract/Token - https://explorer.hydrachain.org/contract/4ab26aaa1803daa638910d71075c06386e391147
print(search('LockTrip'))
```

- Why we didn't implement the search?
  - Because the idea of the library is provide you with the raw responses, without any modification.

#### Configuration: (Optional)

```python
import logging

import requests
from requests.adapters import HTTPAdapter

import hydrachain_explorer_requester
from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#Configure the used requester
http_adapter = HTTPAdapter(
    pool_connections=requests.adapters.DEFAULT_POOLSIZE,
    pool_maxsize=requests.adapters.DEFAULT_POOLSIZE,
    max_retries=3,
    pool_block=requests.adapters.DEFAULT_POOLBLOCK,
)

#Place the configured requester configuration
explorer_requester = ExplorerRequester(
    timeout_seconds = 0.5, # 500 milliseconds
    http_adapter=http_adapter
)

# Configure the level of logging.
hydrachain_explorer_requester.explorer_requester._logger.setLevel(logging.INFO)

block = explorer_requester.get_block(1234)
logger.info(block)
```

## Functionalities:

- All of the explorer requests are supported
- Some of the requests on the explorer use pagination, you can get the information on portions. In the library a two options are present for the requests that use pagination.
  - Raw: You can specify the page and size you want and execute the request with
  - Iterable: **_iterator** ending functions, which will iterate over all elements for you. Specify portion parameter to define how much elements to be fetch at each request.
- You can configure the used requester in the library using the **timeout_seconds** and **http_adapter**. Specify **hooks** if you want via hooks and also configure the **logger**.



## Versions

This library supports **Python 3.11+**. 

`hydrachain-explorer-requester` uses a modified version of [Semantic Versioning](https://semver.org) for all changes to the helper library. It is strongly encouraged that you pin at least the major version and potentially the minor version to avoid pulling in breaking changes.

Semantic Versions take the form of `MAJOR.MINOR.PATCH`

When bugs are fixed in the library in a backwards-compatible way, the `PATCH` level will be incremented by one. When new features are added to the library in a backwards-compatible way, the `PATCH` level will be incremented by one. `PATCH` changes should *not* break your code and are generally safe for upgrade.

When a new large feature set comes online or a small breaking change is introduced, the `MINOR` version will be incremented by one and the `PATCH` version reset to zero. `MINOR` changes *may* require some amount of manual code change for upgrade. These backwards-incompatible changes will generally be limited to a small number of function signature changes.

The `MAJOR` version is used to indicate the family of technology represented by the helper library. Breaking changes that require extensive reworking of code will cause the `MAJOR` version to be incremented by one, and the `MINOR` and `PATCH` versions will be reset to zero. We understand that this can be very disruptive, so we will only introduce this type of breaking change when absolutely necessary. New `MAJOR` versions will be communicated in advance with `Release Candidates` and a schedule.

> Only the current `MAJOR` version of `hydrachain-explorer-requester` is supported. New features, functionality, bug fixes, and security updates will only be added to the current `MAJOR` version.

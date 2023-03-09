# Hydrachain Explorer Requester

[![PyPI](https://img.shields.io/pypi/v/hydrachain-explorer-requester.svg)](https://pypi.python.org/pypi/hydrachain-explorer-requester)
[![PyPI](https://img.shields.io/pypi/pyversions/hydrachain-explorer-requester.svg)](https://pypi.python.org/pypi/hydrachain-explorer-requester)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/ItsGosho/hydrachain-explorer-requester/blob/main/LICENSE)

Easy to use library for accessing the [Hydrachain Explorer](https://explorer.hydrachain.org/) endpoints. Postman collection of all request can be found [here](https://www.postman.com/itsgosho/workspace/public-workspace).

## Installation

#### PyPI:

```
pip install hydrachain-explorer-requester
```

#### Local:

Download the [latest release](https://github.com/ItsGosho/hydrachain-explorer-requester/releases) and run the below command to install it globally:

```
pip install .
```

## Examples

#### Block:

```python
from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

explorer_requester = ExplorerRequester()

# Block - https://explorer.hydrachain.org/block/123/
block_response = explorer_requester.get_block(123)

print(block_response)
```

#### Address Transactions: 

```python
from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

explorer_requester = ExplorerRequester()

# Address - https://explorer.hydrachain.org/address/HCiMdPYCsdPPvbjxHQMmK8QVBEGwextvir/
address_transactions = explorer_requester.get_address_transactions("HCiMdPYCsdPPvbjxHQMmK8QVBEGwextvir")

print(address_transactions)
```

#### Address Transactions - Query Parameters: 

```python
from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

explorer_requester = ExplorerRequester()

# Address - https://explorer.hydrachain.org/address/HCiMdPYCsdPPvbjxHQMmK8QVBEGwextvir/

query_parameters = TransactionsQueryParameters()
query_parameters.set_page(0)
query_parameters.set_page_size(3)
query_parameters.set_from(555555)
query_parameters.set_to_block(666666)

address_transactions = explorer_requester.get_address_transactions("HCiMdPYCsdPPvbjxHQMmK8QVBEGwextvir", query_parameters)

print(address_transactions)
```

#### Search:

```python
from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

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
            print(f'Type {type} not implemented!')
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
- You can configure the used requester in the library using the **timeout_seconds** and **http_adapter**. Specify **hooks** if you want via hooks and also configure the **logger**.
- You can overwrite specific explorer URL. Examples present under **[/examples](https://github.com/ItsGosho/hydrachain-explorer-requester/tree/main/examples)**
- You can overwrite  a query parameter. Examples present under **[/examples](https://github.com/ItsGosho/hydrachain-explorer-requester/tree/main/examples)**



## Versions

This library supports **Python 3.11+**. 

`hydrachain-explorer-requester` uses a modified version of [Semantic Versioning](https://semver.org) for all changes to the helper library. It is strongly encouraged that you pin at least the major version and potentially the minor version to avoid pulling in breaking changes.

Semantic Versions take the form of `MAJOR.MINOR.PATCH`

When bugs are fixed in the library in a backwards-compatible way, the `PATCH` level will be incremented by one. When new features are added to the library in a backwards-compatible way, the `PATCH` level will be incremented by one. `PATCH` changes should *not* break your code and are generally safe for upgrade.

When a new large feature set comes online or a small breaking change is introduced, the `MINOR` version will be incremented by one and the `PATCH` version reset to zero. `MINOR` changes *may* require some amount of manual code change for upgrade. These backwards-incompatible changes will generally be limited to a small number of function signature changes.

The `MAJOR` version is used to indicate the family of technology represented by the helper library. Breaking changes that require extensive reworking of code will cause the `MAJOR` version to be incremented by one, and the `MINOR` and `PATCH` versions will be reset to zero. We understand that this can be very disruptive, so we will only introduce this type of breaking change when absolutely necessary. New `MAJOR` versions will be communicated in advance with `Release Candidates` and a schedule.

> Only the current `MAJOR` version of `hydrachain-explorer-requester` is supported. New features, functionality, bug fixes, and security updates will only be added to the current `MAJOR` version.

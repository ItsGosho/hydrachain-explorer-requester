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

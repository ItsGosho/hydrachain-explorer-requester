import logging

from hydrachain_explorer_requester.enum.address_balance_category import AddressBalanceCategory
from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

explorer_requester = ExplorerRequester()

# Address - https://explorer.hydrachain.org/address/H7FYCLijimtbYk7gdN1hmweftuWLQni3m5/
address = 'H7FYCLijimtbYk7gdN1hmweftuWLQni3m5'

address_balance_response = explorer_requester.get_address_balance(address)
address_balance_total_received_response = explorer_requester.get_address_balance(address, AddressBalanceCategory.TOTAL_RECEIVED)
address_balance_total_sent_response = explorer_requester.get_address_balance(address, AddressBalanceCategory.TOTAL_SENT)
address_balance_unconfirmed_response = explorer_requester.get_address_balance(address, AddressBalanceCategory.UNCONFIRMED)
address_balance_staking_response = explorer_requester.get_address_balance(address, AddressBalanceCategory.STAKING)
address_balance_mature_response = explorer_requester.get_address_balance(address, AddressBalanceCategory.MATURE)

print(f'No category: {address_balance_response}')
print(f'Total Received: {address_balance_staking_response}')
print(f'Total Sent: {address_balance_total_sent_response}')
print(f'Unconfirmed: {address_balance_staking_response}')
print(f'Staking: {address_balance_mature_response}')
print(f'Mature: {address_balance_mature_response}')

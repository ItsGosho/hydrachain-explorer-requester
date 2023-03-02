import logging

from requests.adapters import HTTPAdapter

from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logging.basicConfig(level=logging.DEBUG)

http_adapter = HTTPAdapter(
    max_retries=2,
)
explorer_requester = ExplorerRequester(
    timeout_seconds=0.5, #seconds
    http_adapter=http_adapter
)
block_156 = explorer_requester.get_block(156)

print(block_156)

# rich_list = explorer_requester.get_rich_list(page_number=1, page_size=2)
# print(rich_list)

# date_string = "03 February 2020"
# date_object = datetime.strptime(date_string, "%d %B %Y")
# print(explorer_requester.get_blocks(date_object))

#params = {'q': 'python', 'page': 2}
#url = urlunsplit(('https', 'www.google.com', '/search', urlencode(params), ''))
#print(url)

transactionIds = [
    "c01c990a3014fb42645172866b94327ac78113ae0575d47db9c008221acf719e",
    "59074b244fc2b9ad090cd53a789e48741c7fcba6714d86d74038791877af43a2",
    "58bf053d0868a242c6f7e698ef55502285717a8d7a374118d6f4e027552a5186"
]

#print(type(transactionIds))
#print(explorer_requester.get_transactions(transactionIds))

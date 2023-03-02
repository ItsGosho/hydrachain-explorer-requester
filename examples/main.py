import logging

from hydrachain_explorer_requester.explorer_requester import ExplorerRequester

logging.basicConfig(level=logging.DEBUG)

def test_hook(request, *args, **kwargs):
    """
    A custom request hook that adds a custom header to the request.
    """
    debug = 5

explorer_requester = ExplorerRequester(hooks={'response': test_hook})
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

from api_request import api_request


def fetch_all_data(URL, token, CONTEXT):
    all_items = []
    page = 1
    items_per_page = 100
    while True:
        data = api_request(url, page, items_per_page, token, context)
        all_items.append(data)
        if len(data) < items_per_page:
            break
        page += 1
    return all_items

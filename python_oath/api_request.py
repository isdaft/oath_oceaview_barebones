

def api_request(url, page_number, page_size, token, context):
    import requests
    import json

    session = requests.Session()    
    
    headers = {
        "Authorization": f"Bearer {token}",
        "accept-language": "en-US,en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "Content-Type": "application/json; charset=utf-8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "X-Xss-Protection": "1; mode=block",
        "X-Pager-Sortfield": context.get("X-Pager-Sortfield", ""),
        "X-Pager-Sortmethod": context.get("X-Pager-Sortmethod", ""),
        "x-pager-pagenumber": str(page_number),
        "x-pager-pagesize": str(page_size),
        "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        #"x-fulltext-searchfields": "name,inventoryCode",
        }
    params = {k: v for k, v in context.items() if k.startswith("filter") or k == "withDisabled"}
    response = session.get(url, headers=headers, params=params)
    # Prepare the URL with parameters
    request_url = requests.Request('GET', url, headers=headers, params=params).prepare().url
    
    print(f"Fetching data from {request_url}")
    print(f"Pagenumber == {page_number}")
    response.raise_for_status()
    #print(json.dumps(response.json(), indent=4))
    return response.json()



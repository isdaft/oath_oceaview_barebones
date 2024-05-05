


def fetch_all_data(URL, token, CONTEXT):
    from api_request import api_request
    all_items = []
    
    page = 1
    items_per_page = 100
    while True:
        data = api_request(URL, page, items_per_page, token, CONTEXT)
        all_items.append(data)
        if len(data) < items_per_page:
            break
        page += 1
    return all_items

# fetch all historical data
# will have to depend on the equipment, per eq, each will have its own api call

def fetch_historical_data2(BASE_URL, token, CONTEXT_SENSOR_HISTORY, equipment_id, sensor_id):
    from api_request import api_request

    all_items = []
    
    page = 1
    items_per_page = 1000
    while True:
        url = f"{BASE_URL}/{CONTEXT_SENSOR_HISTORY['endpoint']}/{sensor_id}/readings/history?equipmentId={equipment_id}"
        data = api_request(url, page, items_per_page, token, CONTEXT_SENSOR_HISTORY)
        all_items.append(data)
        print(f"page number historical {page}- {len(data)}")
        if len(data) < items_per_page:
            break
        
        page += 1
    return all_items

def fetch_historical_data(BASE_URL, token, CONTEXT_SENSOR_HISTORY, equipment_id, sensor_id):
    from api_request import api_request

    all_items = []
    
    page = 1
    items_per_page = 1000
    while True:
        url = f"{BASE_URL}/{CONTEXT_SENSOR_HISTORY['endpoint']}/{sensor_id}/readings/history?equipmentId={equipment_id}"
        response = api_request(url, page, items_per_page, token, CONTEXT_SENSOR_HISTORY)
        data = response['items']
        for item in data:
            if item['value'] is None:
                all_items.append(item)
        #all_items.extend(data)
        print(f"page number historical {page}- {len(data)}")
        if len(data) < items_per_page:
            break
        
        page += 1
    return all_items

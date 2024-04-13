    

BASE_URL = "https://oceaview.merck.com/mtw/api/"
API_ENDPOINT = "Equipments"
    
# Enter Search Params
#filterStartDate = "2023-10-01T00:01:00.000Z"
#filterEndDate = "2023-10-31T23:59:00.000Z"

pagerSortField = "name"
pagerSortMethod = "asc"
#filterSubTypes = "201"
filterTopologies = "17,16,18,21,37,43,25,26,27,28,29,34,38,23,35,24,22,39,40,36,31,42,32"
filterTopologyMode = "in"

# Prepare context
CONTEXT = {
    #"filterStartDate": datetime.strptime(filterStartDate, "%Y-%m-%dT%H:%M:%S.%fZ").isoformat() + "Z",
    #"filterEndDate": datetime.strptime(filterEndDate, "%Y-%m-%dT%H:%M:%S.%fZ").isoformat() + "Z",
    "endpoint": apiEndpoint,
    #"filterSubTypes": filterSubTypes,
    "X-Pager-Sortfield": pagerSortField,
    "X-Pager-Sortmethod": pagerSortMethod,
    "filterSources": str(pagerSortField.count(',') + 1),
    "filterTopologies": filterTopologies,
    "filterToplogyMode": filterTopologyMode,
    "withDisabled": "false"
}
URL = BASE_URL + API_ENDPOINT
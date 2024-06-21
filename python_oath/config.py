    
from datetime import datetime
from re import S

BASE_URL = "https://oceaview.merck.com/mtw/api/"
API_ENDPOINT = "Equipments"
    
# Enter Search Params
filterStartDate = "2024-6-11T23:59:00.000Z"
filterEndDate = "2024-06-12T23:59:00.000Z"
AuditfilterStartDate = "2024-04-01T00:01:00.000Z"
AuditfilterEndDate = "2024-04-30T23:59:00.000Z"
pagerSortField = "name"
pagerSortMethod = "asc"
#filterSubTypes = "201"
# WP75B
filterTopologies = "2,3,4,5,15,19,7,8,9,10,11,6,14";
#filterTopologies = "17,16,18,21,37,43,25,26,27,28,29,34,38,23,35,24,22,39,40,36,31,42,32"
filterTopologyMode = "in"

# Prepare context
CONTEXT = {
    #"filterStartDate": datetime.strptime(filterStartDate, "%Y-%m-%dT%H:%M:%S.%fZ").isoformat() + "Z",
    #"filterEndDate": datetime.strptime(filterEndDate, "%Y-%m-%dT%H:%M:%S.%fZ").isoformat() + "Z",
    "endpoint": API_ENDPOINT,
    #"filterSubTypes": filterSubTypes,
    "X-Pager-Sortfield": pagerSortField,
    "X-Pager-Sortmethod": pagerSortMethod,
    "filterSources": str(pagerSortField.count(',') + 1),
    "filterTopologies": filterTopologies,
    "filterToplogyMode": filterTopologyMode,
    "withDisabled": "false"
}
CONTEXT_SENSOR_HISTORY = {
    "filterStartDate": datetime.strptime(filterStartDate, "%Y-%m-%dT%H:%M:%S.%fZ").isoformat() + "Z",
    "filterEndDate": datetime.strptime(filterEndDate, "%Y-%m-%dT%H:%M:%S.%fZ").isoformat() + "Z",
    "endpoint": "Sensors",
    "X-Pager-Sortfield": "date,source,id",
    "X-Pager-Sortmethod": "desc,desc,desc",
    "filterSources": "3",
}
CONTEXT_AUDIT = {
    #"filterStartDate": datetime.strptime(AuditfilterStartDate, "%Y-%m-%dT%H:%M:%S.%fZ").isoformat() + "Z",
    #"filterEndDate": datetime.strptime(AuditfilterEndDate, "%Y-%m-%dT%H:%M:%S.%fZ").isoformat() + "Z",
    "endpoint": "AuditTrails",
    "X-Pager-Sortfield": "date",
    "X-Pager-Sortmethod": "desc",
    "filterTypes": "4",
    "filterSubTypes":"2",
    "filterSearch": "",
    "filterTopologies": "37,43,21,25,26,27,28,34,29,38,23,35,24,22,39,40,36,31,42,32,16,17,18" #SHIP
}

CONTEXT_CM = {
    "filterStartDate": "2024-4-01T16:07:00.000Z",
    "filterEndDate": "2024-04-29T16:07:00.000Z",
    "endpoint": "Alarms",
    "X-Pager-Sortfield": "startDate",
    "X-Pager-Sortmethod": "desc",
    "filterSubTypes": "201"
}
URL = BASE_URL + API_ENDPOINT

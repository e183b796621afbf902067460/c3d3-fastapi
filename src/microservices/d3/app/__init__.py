import requests as r


url = 'http://35.79.16.29:8000/api/v1/auth/login?self=self'
data = {
  "username": "Evf5UGGi_uDtZ9LVCDz17o6Bjg1rd1Jb0Y66wGYWzCw",
  "password": "o5IzBOM3LRUg12q0wtoqJSd4dOqU-gqVMJs19LE8lVc"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json'}

response = r.post(url=url, json=data, headers=header)
access_token = response.json()['access_token']

# arbitrum_n1v1
url = 'http://35.79.16.29:8000/api/v1/d3/new_bids_and_asks?self=self'
data = {
  "pool_address": "0xcDa53B1F66614552F834cEeF361A8D12a0B8DaD8",
  "network_name": "arbitrum_n1v1",
  "protocol_name": "uni_swap_v3_dex_screener_handler",
  "specification_name": "dex",
  "is_reverse": False
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': access_token}

response = r.post(url=url, json=data, headers=header)
print(response.status_code)
print(response.json())

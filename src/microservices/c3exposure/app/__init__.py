import requests as r


url = 'http://18.177.120.25:8000/api/v1/auth/login?self=self'
data = {
  "username": "'yUtZQv6Lqa17F82tINWF2S7JqG_nrVfseqoGYXkbO_I='",
  "password": "'K1Yfdd47ybxap4xEIxAOSG4MQ5F6W716YqP3Tjz75sU='"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json'}

response = r.post(url=url, json=data, headers=header).json()
access_token = response['access_token']

# arbitrum_n1v1
url = 'http://18.177.120.25:8000/api/v1/d3/new_chain?self=self'
data = {
  "network_name": "arbitrum_n1v1",
  "native_chain_token": "ETH",
  "rpc_node": "https://arb-mainnet.g.alchemy.com/v2/tbTGxrZtO-arK0xLiF6ywsLam2vHQ8-1",
  "block_limit": 12000,
  "network_uri": "https://api.arbiscan.io/api",
  "network_api_key": "FCWJRHV8448G6WUFXYTWD1N1E57JGD2NYC"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': access_token}

response = r.post(url=url, json=data, headers=header)
print(response.json())
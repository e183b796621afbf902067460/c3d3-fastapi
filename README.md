# C3D3 FastAPI Research
No dependencies.

---

C3D3 FastAPI Research backend helps to automate C3D3 Data Vault management.

# Configuration

First of all to configure FastAPI backend correctly need to do next steps:

- Clone current repository:
```
git clone https://github.com/e183b796621afbf902067460/c3d3-fastapi-research.git
```

- Get into the project folder:
```
cd c3d3-fastapi-research/src/microservices
```

- Set environment variables in [.env](https://github.com/e183b796621afbf902067460/c3d3-fastapi-research/blob/master/src/microservices/.env).

# Docker

- Run docker compose (`sudo`):
```
docker-compose up -d --build
```

- Check microservices container's ID and copy them:
```
docker ps
```

- Create PostgreSQL instance in each microservice:
```
docker exec -it <CONTAINER ID> python3 app/orm/scripts/create.py
```

- And setup alembic for each instance:
```
sudo docker exec -it <CONTAINER ID> bash -c 'cd app/orm; alembic upgrade head'
```

- Create default admin user in `auth` container:
```
docker exec -it <CONTAINER ID> python3 app/__init__.py
```

# Exit
- To stop all running containers:
```
docker stop $(docker ps -a -q)
```
- And remove it all:
```
docker rm $(docker ps -a -q)
```

# Alembic
- After any changes in DBs this command should be done in `/app/orm` path:
```
alembic revision --autogenerate
```
- And make migrations:
```
alembic upgrade head
```

# Endpoints

### auth/
- `/api/v1/auth/login`
```python
import requests as r


url = 'http://0.0.0.0:8000/api/v1/auth/login?self=self'
data = {
  "username": "string",
  "password": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json'}

response = r.post(url=url, json=data, headers=header)
```

### c3/

- `/api/v1/c3/new_whole_market_trades_history`
```python
import requests as r


access_token = ''
url = 'http://0.0.0.0:8000/api/v1/c3/new_whole_market_trades_history?self=self'
data = {
  "exchange_name": "string",
  "instrument_name": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': access_token}

response = r.post(url=url, json=data, headers=header)
```

### d3/

- `/api/v1/d3/new_chain`
```python
import requests as r


access_token = ''
url = 'http://0.0.0.0:8000/api/v1/d3/new_chain?self=self'
data = {
  "network_name": "string",
  "native_chain_token": "string",
  "rpc_node": "string",
  "block_limit": 0,
  "network_uri": "string",
  "network_api_key": "string"
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': access_token}

response = r.post(url=url, json=data, headers=header)
```

- `/api/v1/d3/new_bids_and_asks`
```python
import requests as r


access_token = ''
url = 'http://0.0.0.0:8000/api/v1/d3/new_bids_and_asks?self=self'
data = {
  "pool_address": "string",
  "network_name": "string",
  "protocol_name": "string",
  "specification_name": "string",
  "is_reverse": True
}
header = {'accept': 'application/json', 'Content-Type': 'application/json', 'authorization': access_token}

response = r.post(url=url, json=data, headers=header)
```

# Visualizador de Processos Jurídicos

## Requirements
1. Docker
2. Docker-Compose

## Running
Just run `docker-compose up` on the project root and access `localhost:3000` on your browser. You should wait a few seconds while the backend pools are created.

## Optinal Configurations
You can personalize the project by editing the following parameters on `config.py`:
- POOL_SIZE: Amount of workers instances used per court (default=5)
- USE_PROXY: Use proxy to anonimize the crawling process (defalt=False, current proxy services are not very trustable)
- TEST: Flag to indicate of the project is running on test or production (default=False (production))
- DB_NAME: Name of MongoDB database
- COURTS: Python dict containing the info of each court
- PROXY_SERVICES: Links to proxy services which provide a new proxy for every request

## Stack
### Backend
- Python 3
- Selenium
- Tornado
- MongoDB
- Unittest with Parameterized (Tests)
- Nginx load balancer
- Docker

### Frontend
- NodeJS
- Express
- EJS
- Docker

## Architecture
Each *backend* instance has *N=POOL_SIZE* workers. We deploy 3 *backend* instances, one *frontend* instance, one *load_balancer* instance and one MongoDB instance. The frontend makes requests to the backend through the *load_balancer*

## Operational Details
Every crawled process is stored locally to speedup the system and avoid multiple accesses to the same court page

## Tests
1. Install MongoDB
2. Enter `backend` dir
3. Run `pip install -r requirements.txt`
4. Run `python tests/test_workers.py && python tests/test_api.py` on `backend` dir

## Next Features and Improvements
1. Job to periodically check for updates on locally stored processes
2. Job to perform an active search for new processes on court page and store them locally
3. Container orchestration with Kubernetes to ease the system scaling
4. Improve the visualization of the process data
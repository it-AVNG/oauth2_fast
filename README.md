# Introduction
This is a repo study about oauth2 flows with additionall logging features

# File structure
the following are the file structure of this repo
```shell
.
├── README.md : this file
├── app : where our app is
│   ├── __init__.py
│   ├── api : where our backend_api is
│   │   ├── __init__.py
│   │   └── entry.py : api entry gateway
│   ├── logs : all about logs and where our logs will be stored as 'app.log'
│   │   ├── __init__.py
│   │   ├── log_config.yaml : config file for logs format and handlers
│   │   └── log_setup.py : logs setup modules
│   └── tests : where our tests packages would be
├── poetry.lock : lockfile for install using poetry
└── pyproject.toml : toml file for install using poetry
```

# Run the backend api
The api is written with [fastApi](https://fastapi.tiangolo.com/#create-it).
Running the back end after installing dependencies using [`poetry`](https://python-poetry.org/).
+ Step1: navigate to `app' directory
+ Step2: run in dev environment of `fastapi` with
```shell
fastapi dev api/entry.py
```
+ Step3: navigate to 'http://127.0.0.1:8000/docs' to see the SwaggerUI to interract with api

# Run the tests:
All the tests are written in `tests` directory; to run the tests use [`pytest`](https://docs.pytest.org/en/stable/).
The command to run pytest is as follow:
```shell
cd app
pytest -v -s
```

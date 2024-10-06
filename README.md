# BusyBe Cloud

[![Quality](https://github.com/busybeapp/busybe-cloud/actions/workflows/quality.yml/badge.svg)](https://github.com/busybeapp/busybe-cloud/actions/workflows/quality.yml)
[![Test](https://github.com/busybeapp/busybe-cloud/actions/workflows/test.yml/badge.svg)](https://github.com/busybeapp/busybe-cloud/actions/workflows/test.yml)

Backend API for busybe app

## Local development

### Python installation
Ensure you have Python installed, preferably version >= **3.12.x**
```shell
brew install python
python --version
```

### Run & Test

#### Setup venv
```shell
python -m venv venv
source venv/bin/activate
```
#### Install dependencies
```shell
pip install -r requirements.txt
```

#### Run server
```shell
uvicorn service.app:app --reload --host 0.0.0.0 --port 8080
```

#### Tests
Running Tests
```shell
pytest
```

### Pre commit

Install local pre-commit hook
```shell
pip install pre-commit
pre-commit install
```

Install commit-msg hook
```shell
pre-commit install -t commit-msg
```
Run manually on all files
```shell
pre-commit run --all-files
```

# OpenAPI docs
We are using swagger to document the api's !!!

On running locally server you will find the swagger page here:
- swagger http://localhost:8080/docs
- redoc http://localhost:8080/redoc

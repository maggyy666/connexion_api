# Connexion API

The project implements a REST API to retrieve tenant information and anomaly detectors using Connexion (AsyncApp + RestyResolver) and OpenSearch. The API follows SPEC First approach and its specification is in the openapi.yaml file. 

Data is stored in OpenSearch and shared via Async endpoints.

## Env config 

* Docker: required for OpenSearch
* Python 3.10+

## Installation and configuration

Install Poetry using pipx:

```
pip install --user pipx
```
```
pipx ensurepath
```
```
pipx install poetry
```
Then install project dependencies and create venv inside the project folder:
```
poetry install
```
Use poetry run to execute scripts inside the environment:
```
poetry run connexion-api
```
<b>Note:</b> 
Running the app with `poetry run connexion-api` does <b>NOT</b> activate the virtual environment permanently. Instead, it executes the script within the virtual environment context, so dependencies are correctly resolved. To activate the virtual environment manually and work inside it interactively, use: 
```
.\.venv\Scripts\activate
```
## Environment Configuration (.env)

To configure the application using environment variables, create a `.env` file in the root of the project:
```
HOST=127.0.0.1
PORT=8080
DEBUG=false

OPENSEARCH_HOST=your-opensearch-host-url
OPENSEARCH_USER=your-username
OPENSEARCH_PASSWORD=your-password
```
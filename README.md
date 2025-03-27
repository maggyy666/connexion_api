# Connexion API

The project implements a REST API to retrieve tenant information and anomaly detectors using Connexion (AsyncApp + RestyResolver) and OpenSearch. The API follows SPEC First approach and its specification is in the openapi.yaml file. 

Data is stored in OpenSearch and shared via Async endpoints.

## Env config 

* Docker: required for OpenSearch
* Python 3.10+

## Installation and configuration

1. Install Poetry using pipx:

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
To activate the venv:
```
.\.venv\Scripts\activate
```
Or use poetry run to execute scripts inside the environment:
```
poetry run connexion-api
```
Note: 
Running the app with `poetry run connexion-api` does <b>NOT</b> activate the virtual environment permanently. Instead, it executes the script within the virtual environment context, so dependencies are correctly resolved. To activate the virtual environment manually and work inside it interactively, use:
```
.\.venv\Scripts\activate
```
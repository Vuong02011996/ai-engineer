# OryzaAI Backend
## Start server
### Install 
#### Install poetry [poetry](https://python-poetry.org/docs/main/#installing-with-the-official-installer)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
#### Install packages 
```bash
poetry install
```
To get started you need Poetry's bin directory (/home/ptt/.local/bin) in your `PATH`
environment variable.

Add `export PATH="/home/ptt/.local/bin:$PATH"` to your shell configuration file.

Alternatively, you can call Poetry explicitly with `/home/ptt/.local/bin/poetry`.

You can test that everything is set up by executing:

`poetry --version`
#### Activate the virtual environment
```bash
source .venv/bin/activate
```
### Initialize database
Create Oryza Company and Superuser, for example:
```bash
python -m app.db.init_db --email thanh.pt1@oryza.vn --username thanhpt1 --password 1
```
### Create Default Object
These objects are created to handle cases when 2 object are refererenced to each other, but one of them is deleted.

*For models*: Company, TypeService, BrandCamera.

BrandCamera and TypeService are created using constants in the code.

*Other models*:

Ex: If a Service is deleted, all Process from that Service are deleted 
```bash
python -m app.db.init_default_objects
```
### Create Default Geography Units
```bash
python -m app.db.init_geo_units
```

### Run server
```bash
fastapi dev app/main.py --port 8001 --host 0.0.0.0
```
## Modify
### Package management
Add new package
```bash
poetry add <package>
```
Export the current environment to requirements.txt
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```
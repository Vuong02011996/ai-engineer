# Camera AI Backend
## Start server
### Install 
#### Install MQTT Broker
```bash
sudo snap install mosquitto
sudo apt-get install -y mosquitto-clients
```
#### Install RabbitMQ
https://docs.google.com/document/d/1KtN9OHqaAQC9VUJnTG5k7GAWRLu3rETSrJcvpbg2DEU
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
### Run server
```bash
uvicorn app.main:app --reload
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

To update package from requirements.txt
```bash
awk -F ';' '{print $1}' requirements.txt | xargs -n 1 poetry add
```
If not care about the version, just the latest
```bash
awk -F '[=;]' '{print $1}' requirements.txt | xargs -n 1 poetry add
```

### Request Example
api/v1/process/enable
```bash
{
  "process_id": "662760357279e1d222757c9c",
  "name": "OryzaBinhThanh",
  "ip_address": "192.168.111.6",
  "port": 80,
  "username": "admin",
  "password": "Oryza@123"
}
```
api/v1/process/kill
```bash
{
    "process_id": "662760357279e1d222757c9c",
}
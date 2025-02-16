# Set up aws run source holter_processor
## Set up AWS
+ Install aws CLI 
+ Set up AWS profile follow file instruction:
  + `aws configure sso --profile btcy-sso`
    + Step : `SSO registration scopes [sso:account:access]:` just enter to login
  + `aws configure sso --profile btcy-sso-eks`
+ Check setup success by login `aws sso login --profile btcy-sso`
## Run source 
+ Clone source
+ Create virtual environment, and set up env
```
 python3.11 -m venv venv_processor : Create a Python virtual environment
 source venv_processor/bin/activate : Activate the Python virtual environment
 make setup-venv : set env
 pip install -r requirements.txt  : Install the necessary packages
 make setup-lib : set up the library
```


## Error:
+ 1: 
  + make setup-lib
  `You must specify a region. You can also configure your region by running "aws configure".
  make: *** [Makefile:43: login-setup] Error 253
  `
  + export AWS_PROFILE=btcy-sso
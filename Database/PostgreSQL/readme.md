# Setup 
+ sudo apt install postgresql postgresql-client
+ sudo systemctl status/start/stop postgresql
# Create user DB
+ Method 1: Using createuser Client Utility
  + sudo -u postgres createuser [name]
  + sudo -u postgres createuser -e [name] To show the server message, add the -e tag:
  + Chia lam 2 phan:
    + Switch to the postgres user: sudo su - postgres
    + Run the createuser command: createuser [name]
+ Method 2: Using psql
  + Switch to the postgres user and start the interactive terminal with: sudo -u postgres psql
    + CREATE USER [name] (CREATE USER mary)
# Create a Password for a User
+ Method 1: The createuser Command
    + Use the createuser command and add the --pwprompt option to invoke a password creation prompt automatically:
      + sudo -u postgres createuser [name] --pwprompt
      + sudo -u postgres createuser [name] -P (shorthand)

+ Method 2: The psql Interactive Shell
    + CREATE USER [name] WITH PASSWORD '[password]';

=> sudo -u postgres createuser -s vuong_postgre2 -P
=> sudo -u postgres psql 
  \du 

  
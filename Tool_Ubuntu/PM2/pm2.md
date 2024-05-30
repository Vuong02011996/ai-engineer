# Mange python process by pm2
## Install
```commandline
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs
```
+ If not npm:
+ NPM viết tắt của từ Node Package Manager là một công cụ tạo và quản lý các thư viện javascript cho Nodejs
```commandline
sudo apt-get install npm
sudo npm install pm2 -g
```

## Command often using
```commandline
pm2 status
pm2 ls
pm2 start
pm2 stop
pm2 logs 
```

# Reference
+ [pm2.io Manage-Python-Processes](https://pm2.io/blog/2018/09/19/Manage-Python-Processes)
Inference in [here](https://pm2.io/blog/2018/09/19/Manage-Python-Processes)
# Config
Create file ecosystem.config.yml:
```
    apps:
      - script : ./server.py
        name   : 'clover_dev_5555'
        interpreter: /mnt/storage/anaconda3/envs/flask-app/bin/python
        args: ".env_test"
    
      - script : ./server.py
        name   : 'clover_dev_11033'
        interpreter: /mnt/storage/anaconda3/envs/flask-app/bin/python
        args: ".env_demo"
    
      - script : ./server.py
        name   : 'clover_dev_5556'
        interpreter: /mnt/storage/anaconda3/envs/flask-app/bin/python
        args: ".env_staging"
```
    
pm2 restart ecosystem.test.config.yaml

# Auto start when reboot
+ [Auto start when reboot](https://stackoverflow.com/questions/60095316/does-pm2-auto-restart-application-after-reboot-by-default)
pm2 start ecosystem.test.config.yaml
pm2 startup
  + sudo su -c "env PATH=$PATH:/home/unitech/.nvm/versions/node/v14.3/bin pm2 startup <distribution> -u <user> --hp <home-path>
pm2 save 

# Command
```
pm2 resurrect
pm2 status
pm2 restart 0
pm2 stop 0
pm2 show run_model
pm2 start python.py
```
# Monitor 
    ```commandline
        pm2 monit
    ```
# View log file
+ `/home/oryza/.pm2/logs`
+ view 20 line before and after grep : `grep -C  20 "Camera can't read frame" loitering-production-30001-out.log`
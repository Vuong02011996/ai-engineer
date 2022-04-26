see details at https://github.com/Vuong02011996/mongo_db

# Install with one command from docker-compose
+ Create folder save data: mongodb
+ Create file docker-compose.yaml
+ ```commandline
    version: '3'
    services:
      mongodb:
        image: 'mongo:latest'
        environment:
          MONGO_INITDB_ROOT_USERNAME: root
          MONGO_INITDB_ROOT_PASSWORD: example
        ports:
          - 11037:27017
        restart: always
        volumes:
          - /storages/data/Database/NewMongoDB/mongodb:/data/db
    
    ```
  
+ Run: sudo docker-compose up

# Mongo compass
```commandline
+ wget https://downloads.mongodb.com/compass/mongodb-compass_1.28.1_amd64.deb
+ sudo apt install ./mongodb-compass_1.28.1_amd64.deb
```

# Connect with mongo compass
+ mongodb://root:example@localhost:11037
# Usually using
## Docker
+ `docker stop $(docker ps -a -q)`
+ `docker rm $(docker ps -a -q)`
+ docker logs id/name_container -f
+ docker stats - view cpu/memory using

+ docker build --tag <Docker Image name> --file <specific Dockerfile> . - `docker build -t registry.oryza.vn/vehicle-detection:latest .`
+ docker tag - `docker tag registry.oryza.vn/vehicle-detection:latest registry.oryza.vn/vehicle-detection:v1.1.0`
+ docker push - `docker push registry.oryza.vn/head_person_v2:latest`

+ Run container: `docker run -it --name test_loitering_image registry.oryza.vn/loitering_detection`

## Docker compose
+ docker compose -f file_docker-compose.yml up -d
+ docker compose -f file_docker-compose.yml down



# Task
+ Run docker face in local
  + B1: Stop all docker, service port is running
    + `docker stop $(docker ps -a -q)`
    + `docker rm $(docker ps -a -q)`
  + B2: 
+ Run BE/FE oryza AI
  + Framework
  + Flow code
  + Key logic/library
  + Copilot
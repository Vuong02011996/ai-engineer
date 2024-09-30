# Run full 
oryza-ai.db
oryza-ai.prod
insightface.trt
head_person
milvus.2.4.....
face_recognition

## oryza-ai.db
+ mongo : 0.0.0.0:27017 - image: mongo
+ rabbitmq : 0.0.0.0:5672 - image: rabbitmq:management
## cam-ai-prod.yml
+ camera_ai_service: 0.0.0.0:8000 - image registry.oryza.vn/camera-ai-service:latest
## oryza-ai.prod
+ BE oryza-ai: 0.0.0.0:8001 - image:registry.oryza.vn/oryza-ai:latest
+ FE oryza-ai: 0.0.0.0:3000 - registry.oryza.vn/oryza-ai-frontend:v1.0.0-local


# Error
+ error from daemon in stream: Error grabbing logs: invalid character 'l' after object key:value pair
+ Khong login create duoc user to login in localhost
  + `docker exec -it id_container_BE bash`
  + in folder app: `python -m app.db.init_db --email admin@gmail.com --username admin --password 1`
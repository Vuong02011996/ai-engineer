# Step to run service using grpc

+ Define Protobuf messages: Define Protobuf messages for the request and response payloads.
+ Define gRPC service: Define a gRPC service that specifies the methods (RPCs) that the server can handle.
  + Compile the api.proto file to generate Python code for gRPC
  + python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. api.proto
  + This will generate api_pb2.py and api_pb2_grpc.py files.
+ Implement the gRPC server: Implement the server logic for handling the gRPC methods defined in the service.
+ Implement the gRPC client: Implement the client code to call the gRPC methods exposed by the server.

# Install 
+ pip install grpcio
+ pip install grpcio-tools

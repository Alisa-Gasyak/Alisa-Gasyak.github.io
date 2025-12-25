@echo off

mkdir protos 2>nul
mkdir server\grpc_generated 2>nul
mkdir client\grpc_generated 2>nul

python -m grpc_tools.protoc ^
  -I./protos ^
  --python_out=./server/grpc_generated ^
  --grpc_python_out=./server/grpc_generated ^
  --python_out=./client/grpc_generated ^
  --grpc_python_out=./client/grpc_generated ^
  ./protos/glossary.proto

echo Protobuf код сгенерирован
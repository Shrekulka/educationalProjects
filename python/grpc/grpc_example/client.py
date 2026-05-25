# grpc_example/client.py

import grpc

from config import settings
from protos import todo_pb2_grpc


async def grpc_todo_client():
    # Объединяем хост и порт в одну строку
    target = f"{settings.host}:{settings.port}"

    # Создаем gRPC канал
    channel = grpc.insecure_channel(target)

    # Создаем клиента
    client = todo_pb2_grpc.TodoServiceStub(channel)

    return client

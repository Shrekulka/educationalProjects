import typing as t

import grpc
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from google.protobuf.json_format import MessageToDict
from grpc.aio import AioRpcError
from starlette import status

from starlette.responses import FileResponse, JSONResponse

from client import grpc_todo_client
from config import settings
from logger_config import logger
from protos import todo_pb2


def create_app() -> FastAPI:
    """
        Создает и настраивает экземпляр приложения FastAPI.

        Returns:
            FastAPI: Настроенный экземпляр приложения FastAPI.
    """
    # Создаем экземпляр FastAPI с заголовком "gRPC example"
    app: FastAPI = FastAPI(title="gRPC example")

    @app.get("/")
    def get_ping() -> FileResponse:
        return {"ping": True}

    @app.post("/", status_code=status.HTTP_201_CREATED)
    async def create_todo(name: str, completed: bool, day: int, client: t.Any = Depends(grpc_todo_client)):
        try:
            todo = await client.CreateTodo(
                todo_pb2.CreateTodoRequest(
                    name=name,
                    completed=completed,
                    day=day
                ), timeout=30
            )
            return JSONResponse(MessageToDict(todo))
        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")

    @app.get("/todo")
    async def list_todo(client: t.Any = Depends(grpc_todo_client)) -> JSONResponse:
        try:
            todo = await client.ListTodo(todo_pb2.ListTodoRequest())
            return JSONResponse(MessageToDict(todo))
        except AioRpcError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.details())

    # Возвращаем созданный экземпляр FastAPI
    return app


# Если этот файл запускается напрямую (не импортируется как модуль), запускаем приложение с помощью uvicorn
if __name__ == '__main__':
    try:
        # Запускаем приложение с помощью `uvicorn`, указывая путь к функции create_app(), а также хост и порт
        uvicorn.run("api:create_app", host=settings.host, port=settings.port)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

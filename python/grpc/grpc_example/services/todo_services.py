# grpc_example/services/todo_services.py
from grpc import aio
from grpc_reflection.v1alpha import reflection

from config import settings
from model.todo_model import Todo
from protos import todo_pb2
from protos import todo_pb2_grpc


class TodoServiceServicer(todo_pb2_grpc.TodoServiceServicer):
    async def CreateTodo(self, request, content):
        todo = await Todo.insert(
            Todo(
                name=request.name,
                completed=request.completed,
                day=request.day))
        print("CreateTodo")
        return todo_pb2.CreateTodoResponse(todo=todo[0])

    async def ReadTodo(self, request, content):
        todo = await Todo.select().where(Todo.id == request.id).first()
        print("ReadTodo")
        return todo_pb2.ReadTodoResponse(todo=todo)

    async def UpdateTodo(self, request, content):
        await Todo.update({
            Todo.name: request.name,
            Todo.completed: request.completed,
            Todo.day: request.day}).where(Todo.id == request.id)
        todo = await Todo.select().where(Todo.id == request.id).first()
        print("UpdateTodo")
        return todo_pb2.UpdateTodoResponse(todo=todo)

    async def DeleteTodo(self, request, content):
        await Todo.delete().where(Todo.id == request.id)
        print("DeleteTodo")
        return todo_pb2.DeleteTodoResponse(success=True)

    async def ListTodo(self, request, context):
        todo = await Todo.select()
        print("ListTodo")
        return todo_pb2.ListTodoResponse(todo=todo)


async def serve():
    await Todo.create_table(if_not_exists=True)
    server = aio.server()

    # Регистрация сервиса TodoServiceServicer на сервере.
    # Это связывает реализацию сервиса с сервером, чтобы он мог обрабатывать запросы к этому сервису.
    todo_pb2_grpc.add_TodoServiceServicer_to_server(
        TodoServiceServicer(), server
    )

    # Определение списка имен сервисов, которые будут поддерживать рефлексию.
    # Включает имя зарегистрированного сервиса и имя встроенного сервиса рефлексии.
    SERVICE_NAMES = (
        # Имя зарегистрированного сервиса
        todo_pb2.DESCRIPTOR.services_by_name['TodoService'].full_name,
        reflection.SERVICE_NAME,
    )

    # Включение поддержки рефлексии на сервере.
    # Это позволяет клиентам запрашивать информацию о сервисах и методах на сервере.
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    # Настройка сервера на прослушивание входящих соединений на порту 5080.
    # '[::]:5080' означает, что сервер будет слушать на всех сетевых интерфейсах на этом порту.
    server.add_insecure_port(f'[::]:{settings.port}')
    print(f'[::]:{settings.port}')

    # Запуск сервера. После запуска сервер начнет принимать и обрабатывать входящ ие запросы.
    await server.start()

    print("Сервер клиентского потокового RPC запущен на порту 5080")

    # Ожидание завершения работы сервера
    await server.wait_for_termination()

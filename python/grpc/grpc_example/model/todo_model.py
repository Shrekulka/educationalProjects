# grpc_example/model/todo.py

from piccolo.columns import Boolean, Varchar, Integer
from piccolo.engine.sqlite import SQLiteEngine
from piccolo.table import Table

DB = SQLiteEngine("db.sqlite")


class Todo(Table, db=DB):
    name = Varchar(length=50)
    completed = Boolean(default=False)
    day = Integer(default=0)

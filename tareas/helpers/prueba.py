from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine.base import Connection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import os


def changeTaskState(task_id):
    engine = create_engine('sqlite:///../data/test.db')
    connection = engine.connect()
    Base = automap_base()
    Base.prepare(engine,reflect=True)
    Tarea = Base.classes.tarea
    session = Session(engine)

    try:
        firstTask = session.query(Tarea).get(task_id)
        firstTask.estado = 'processed'
        session.commit()
        closeConnections(session,connection)
    except:
        print('hola')
        closeConnections(session,connection)


def closeConnections(session:Session,connection:Connection):
    session.close_all()
    connection.close()

changeTaskState(1)
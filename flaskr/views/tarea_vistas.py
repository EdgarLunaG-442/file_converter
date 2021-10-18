from typing import List
from flask_restful import Resource
from flask import request,send_file
from celery import Celery
from werkzeug.datastructures import FileStorage
from uuid import uuid1

from ..models import Tarea,db
from ..schemas import TareaSchema
import os

os.environ.setdefault("REDIS_HOST", "localhost")
UPLOAD_DIRECTORY = "../data/input"
OUTPUT_DIRECTORY= "../data/output"

def withoutPaths(tarea):
    inputpath,outputpath, rest = (lambda inputpath,outputpath,**rest: (inputpath,outputpath, rest))(**tarea)
    return rest

celery_app = Celery(
    "tareas",
    broker=f'redis://{os.environ["REDIS_HOST"]}:6379/0',
    backend=f'redis://{os.environ["REDIS_HOST"]}:6379/0',
)

tarea_schema = TareaSchema()


class TareasView(Resource):
    def post(self):
        lista = request.files.lists()
        files:List[FileStorage] = [elem[1] for elem in lista][0]
        outputFormat = request.form.get('output_format')
        inputFormat = request.form.get('input_format')
        tasks:List[Tarea] = []
        for file in files:
            uuid = uuid1()
            savePath = os.path.join(UPLOAD_DIRECTORY, '{}.{}'.format(uuid,inputFormat))
            outPath = os.path.join(OUTPUT_DIRECTORY, '{}.{}'.format(uuid,outputFormat))
            file.save(savePath)
            tarea=Tarea(nombre='{}'.format(uuid),inputpath=savePath,outputpath=outPath)
            db.session.add(tarea)
            tasks.append(tarea)
        db.session.commit()
        for task in tasks:
            celery_app.send_task('procesar_tarea',args=(task.id,),queue='prueba1')

        return {'mensaje':'La tarea fue creada con éxito'}

    def get(self):
        tareas = Tarea.query.all()
        tareasJson = [withoutPaths(tarea_schema.dump(tarea)) for tarea in tareas]

        return tareasJson

class TareaView(Resource):

    def get(self,id_task):
        tarea = Tarea.query.get_or_404(id_task)
        tareaJson = withoutPaths(tarea_schema.dump(tarea))
        return tareaJson

class FileView(Resource):

    def get(self,id_task):
        tarea = Tarea.query.get_or_404(id_task)
        if tarea.estado == 'processed':
            return send_file(tarea.outputpath)
        else:
            return {'mensaje':'El archivo aún no esta listo'},400



from flask import Flask
from flask_cors import CORS
from flask_restful import Api



from .views import TareasView,TareaView,FileView,db




def create_app(name):
    app = Flask(name)
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///../data/test.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = True
    return app

app = create_app('default')
app.app_context().push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api=Api(app)

api.add_resource(TareasView,'/api/tareas')
api.add_resource(TareaView,'/api/tareas/<int:id_task>')
api.add_resource(FileView,'/api/tareas/<int:id_task>/download')






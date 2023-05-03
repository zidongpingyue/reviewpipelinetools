from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import *
# from flask_pymongo import PyMongo,MongoClient

import traceback
import logging




app =Flask("model api server")
CORS(app,supports_credentials=True,max_age=36000,resources={r"*": {"origins": "*"}})



#配置sql地址



# SQLALCHEMY_DATABASE_URI = '''mysql://enteam:123456@1.15.184.52:3306/flasktest'''
# MONGODB_URI="mongodb://superuser:superadmin@1.15.184.52:27017/test?authSource=admin"


# app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_ENGINE_OPTIONS']={
    'pool_size' : 10,
    'pool_recycle':120,
    'pool_pre_ping': True
}
# app.config["MONGO_URI"] = MONGODB_URI
app.config["SECRET_KEY"] = "sdfsdfssefe"
app.config["JSON_AS_ASCII"] = False
# mongo = PyMongo(app)
# mongo=PyMongo(app,uri=MONGODB_URI)
# mongo=MongoClient(MONGODB_URI)
# db=SQLAlchemy(app)


#导入blueprint
# from template.template import appblueprint
from router.ImgUtils import imgutilsblueprint
from router.WorkPipeline import workpipelineblueprint
#--------------------------------------------
#加载blueprint
app.register_blueprint(imgutilsblueprint)
app.register_blueprint(workpipelineblueprint)
# app.register_blueprint(appblueprint)
# app.register_blueprint(fileblueprint)
# app.register_blueprint(llr)
# app.register_blueprint(alldirectorblueprint,url_prefix="/director")
# app.register_blueprint(allfrontprint,url_prefix="/front")



#___________________________________________

# #导入socket
# # from flask_socketio import Namespace
# from router.monitor.monitor import MonitorSocket
# from flask_socketio import SocketIO
# # from socketio import AsyncServer
# # from aiohttp import web
# socketio = SocketIO(app,ping_interval=25,cors_allowed_origins="*")
# socketio.on_namespace(MonitorSocket("/monsocket"))

# appsock = web.Application()
# socket_=AsyncServer()
# socket_.register_namespace(MonitorSocket("/monsocket"))
# socket_.attach(appsock)
# socket_.


#_______________________________________________



if __name__=="__main__":
    try:
        app.run(debug=True,port=8087,use_reloader=False)
        # app.run(debug=True,port=8086,use_reloader=True)
    except Exception :
        traceback.print_exc()
    finally:
        pass
        # db.session.close_all()
        # mongo.close()
        # print(get_trace)
        
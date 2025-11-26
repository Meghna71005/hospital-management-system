from flask import Flask;
from application.database import db
app= None

def create_app():
    app = Flask(__name__)
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///hospital.sqlite3'
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()  
from application import models
#from application.controllers import *        


    
if __name__=="__main__": # run ths app when invoked
    with app.app_context():
        db.create_all()  # create database tables
    
    app.run()

   
    

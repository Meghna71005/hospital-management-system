from flask import Flask;
from application.database import db
from dotenv import load_dotenv

import os
app= None

load_dotenv()
def create_app():
    app = Flask(__name__)
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///hospital.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'false').lower() == 'true'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()  
from application import models
from application.controllers import *        
from application.models import create_default_admin

    
if __name__=="__main__": # run ths app when invoked
    with app.app_context():
         db.create_all()  # create database tables
         create_default_admin() 
    app.run()

   
    

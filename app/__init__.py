from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

SECRET_KEY = os.urandom(24).hex()
app = Flask(__name__)
# Configurar SECRET KEY y La base de datos con MySQL
app.config['SECRET_KEY'] = SECRET_KEY
# La base de datos le llamé votation_db
# Modificar el Username y el password y el nombre de la base de datos que tu tengas configurado
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pwd12345@localhost/votation_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#SQLAlchemy es un Object-Relational Mapper (ORM) en Python que permite interactuar con
# bases de datos relacionales sin necesidad de usar SQL directamente. 
# Se utiliza para simplificar el acceso y manipulación de datos almacenados 
# en bases de datos desde aplicaciones Python

from app import routes
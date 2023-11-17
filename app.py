import os
import psycopg2
import requests

from flask import Flask, session,render_template , redirect, request , jsonify
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

#Cargo las Variables de Entorno
load_dotenv()



app = Flask(__name__)


#Validamos que haya una DB URL
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

#APP Config
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


Session(app)
# Conexion de la DB
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 
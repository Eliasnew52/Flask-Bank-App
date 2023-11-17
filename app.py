import os
import psycopg2
import requests

from flask import Flask, session,render_template , redirect, request , jsonify
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from tempfile import mkdtemp


#Hash Pass for more security
from werkzeug.security import generate_password_hash , check_password_hash

#Virtual Enviroment VARS Setup
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")



# Configure session to use filesystem

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
    #Este limpia los datos de Sesion
    session.clear()
    return render_template('login.html')




# LOGIN ROUTE
@app.route('/login',methods = ['GET','POST'])
def login():
    #Login - Capto los Datos del Formulario
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    #Si falta algun dato del Form, Redireccionar
        if not request.form.get('username') or not request.form.get('password'):
            return redirect('/')
        
        #Pruebo ejecutar la busqueda dentro de la db
        try:
            User_Query = text("SELECT * FROM users WHERE username =:username AND password =:password")
            Query_Result = db.execute(User_Query,{'username':username,'password':password})
            User = Query_Result.fetchone()
            print(User)
            if User:  
                session["user_id"] = User[0]
                session["username"] = User[1]
                print(session["username"])
                print(session["user_id"])
                return redirect('/index')
            else:
                return "Incorrect Username or Password"
        except Exception as e:
            print(e)
    else:
       session.clear()
       return render_template('login.html')


        
@app.route('/register',methods = ['GET','POST'])
def register():
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

    
    
        if not request.form.get('username') or not request.form.get('password'):
            return "Please Add all the Data Requiered Dude omg"
        
        #Efectuamos una busqueda para los posibles usernames y mail ya registrados
        try:
            Search_Query = text("SELECT * from users WHERE username =:username")
            Query_Result = db.execute(Search_Query,{'username':username})
            User = Query_Result.fetchone()
            print(User)
            if User:
                if(User[1] == username):
                    return"Username Already Exists"
            else:
                try:
                    Register_Query = text("INSERT INTO users (username,password) VALUES (:username,:password)")
                    Query_Result = db.execute(Register_Query,{'username':username,'password':password})
                    db.commit()
                    return redirect('/login')
                except:
                    db.rollback()
                    return "Submit Error"                     
        except Exception as e:
            print(e)
    else:
        return render_template('register.html')



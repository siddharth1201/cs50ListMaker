import smtplib
from turtle import radians


from flask import Flask,redirect,render_template,request,session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from validate_email import validate_email 

from threading import Lock


#configuring sqlite3
import sqlite3
conn = sqlite3.connect("data.db", check_same_thread=False)
db = conn.cursor()

#configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#ensure are autoreloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Define the lock globally
lock = Lock()

@app.route("/")
def index():
    id = session.get("user_id")
    
    if check_login(id) == True:
        data=db.execute("SELECT * FROM users WHERE id = ?",(id,))
        for row in data:
            name = row[1]
            email = row[3]
            phone_number= row[4]
            

        return render_template("index.html",name=name,email=email,phone_number=phone_number)
        
    else:
        return redirect ("/login")
    

@app.route("/register", methods=["GET","POST"])
def register():
    #loading data from form into variables 
    if request.method=="GET":
        return render_template("register.html")

    if request.method=="POST":
        if not request.form.get("name"):
            return("Name is compulsory")

        if not request.form.get("user_password"):
            return ("Password is Compulsory.")

        if not request.form.get("phone_number"):
            return ("Phone number required")
            
        name = request.form.get("name")
        password = request.form.get("user_password")
        conf_password = request.form.get("confirm_user_password")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")

        hash= generate_password_hash(password)            
        db.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER NOT NULL,Name TEXT,Hash TEXT,Email TEXT, PhoneNumber TEXT, PRIMARY KEY(id))")
        user_list = []
        user_list = db.execute("SELECT * FROM users")
        #check if name is unique
        valid= False
        for row in user_list:
            print(row[1])
            if name not in row[1]:
                valid = True
            else:
                return ("Username already exists")

        print(email)
        #check if password is valid
        valid=False
        if len(password)>=8:
            valid=True
        else:
            return("Password must be 8 Character long")

        #checking confirm password
        valid=False
        if password == conf_password:
            valid=True
        else:
            return("Confirm Password does not match")


        #check if email is valid
        valid= False
        is_valid=validate_email(email)
        if is_valid == True:
            valid = True
        else:
            return ("email does not exist")

        print(is_valid)
        if valid == True:
            db.execute("INSERT INTO users(name,hash,email,PhoneNumber) VALUES(?,?,?,?)",(name,hash,email,phone_number))
            conn.commit()

            return redirect("/login")
            
        
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    
    if request.method=="POST":
        user_name = request.form.get("name")
        registered_list = []
        registered_list = db.execute("SELECT id,Name,hash FROM users WHERE name = ?",(user_name,))
        conn.commit()
        for row in registered_list:
            if user_name in row[1]:
                entered_password = request.form.get("password")
                hash_check=check_password_hash(row[2],entered_password)
                if hash_check == True:
                    session["user_id"] = row[0]
                else:
                    return ("Incorrect pasword")
            else:
                return ("Invalid username/password")

        return redirect("/")


@app.route("/note",methods=["GET","POST"])
def note():
    if check_login(session.get("user_id"))==True:
        #lock the cursor
        lock.acquire(True)

        id=session.get("user_id")
        if request.method=="GET":
            saved_notes = db.execute("SELECT note_no,note,note_title FROM Notes WHERE id = ?",(id,))
            note_list=[]
            for row in saved_notes:
                note_dict={}
                note_dict["note_no"]=row[0]
                note_dict["note"]=row[1]
                note_dict["note_title"]=row[2]
                note_list.append(note_dict)
            
            #release the cursor
            lock.release()
            return render_template("notes.html",note_list=note_list)

        if request.method=="POST":
            note_title = request.form.get("note_title").strip()
            note = request.form.get("note").strip()
            db.execute("INSERT INTO Notes(id,note_title,note) VALUES(?,?,?)",(id,note_title,note,))
            conn.commit()
            #release the cursor
            lock.release()
            return redirect("/")


    else:
        return redirect("/login")

@app.route("/email",methods=["POST"])
def email():
    #lock the cursor
    lock.acquire(True)
    id = session.get("user_id")

    server = smtplib.SMTP('smtp.gmail.com',587)

    server.starttls()

    server.login('titlemaker4@gmail.com','akllucitxtvmklbf')
    notes_table_data = []
    notes_table = db.execute("SELECT note_no,note,note_title FROM Notes WHERE id=?",(id,))
    for row in notes_table:
        notes_table_data.append(row)

    email_string = "\n"
    for row in notes_table_data:
        data_string = '=>' + str(row[2]) + '\n||=>' + row[1]
        email_string = email_string + data_string + "\n\n\n"

    
    user_email = db.execute("SELECT Email from users WHERE id=?",(id,))
    for row in user_email:
        u_email = row[0]
    server.sendmail("titlemaker4@gmail.com",u_email,email_string)
    #release the cursor
    lock.release()
    return redirect("/")

@app.route("/clear_table", methods=["POST"])
def clear_table():
    id = session.get("user_id")
    db.execute("DELETE FROM notes WHERE id=?",(id,))
    conn.commit()
    return redirect("/")

@app.route("/logout", methods=["GET","POST"])
def logout():
    session.clear()

    return redirect("/")


def check_login(session_id):
    if session_id == None:
        return False
    else:
        return True


    
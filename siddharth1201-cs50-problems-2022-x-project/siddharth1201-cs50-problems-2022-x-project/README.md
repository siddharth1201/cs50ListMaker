# Listmaker
#### Video Demo: https://youtu.be/bPyxCLKk2-E
#### Description:
Listmaker is a website that allow us to make a list of tasks and email them to ouselves. The advantage of using an email is that as soon as we email something it is easily accessible across various devices.
### layout.html
layout page contains building tags of html. It also contains the navigation bar which contains four buttons Register, Login, Home, and Logout.
The register button takes us to register page. The login button takes us to the login page , The Home button takes us to the home page and logout button is used to logout of the website so new user can login.
### Register page
Register page contains five forms Name, Password, Confirm Password, Email, Phone Number.The username must be unique, the password must be atleat 8 characters long. It should also match with the confirm password entry. The email address should be valid. We fill the details and click on the register button then we are directed to the login page.
### login page
Login page contains name and password form. Fill the details and click on the login button. The name and password will be checked to see if the user is registered or not and the passsword is correct.
### Home page
- The home page of the website contains details of the user at the top. A note form to enter the note, and title form to enter the title of the note. When we click on the save note button the note is saved to the table and also in the database with the unique user id.
- The send as email button sends the whole table as email to the registered email address.
- The clear all button clears the table so we can create a new table.
### style.css
I used class identifiers to edit different part of the pages in similar way. I also tried to keep the design as minimalistic as possible so it is easy to understand by the user.
### data.db
- The database contain all the lists the the user saves and the title given to them. It also contains additional information like note id and id of the uer the note is written by.
- It also contains all the users who are registered in the website. User info is stored in the users table.
- data.db database contains two tables, users and notes. The user table have ID as primary key and foreign key. Other columns in user table are Name, hash(hash value of the password), email, phonenumber. The notes table contain note_no as prmimary key and id as foreign key. Other columns in notes table are note_text and note_title.
### Programming language and framework
- Python(Flask) is used for writing the backend of the website.
- HTML, CSS, Bootstrap is used for frontend of the website.
- SQLite is used for managing databases.
### How to launch an application
- Open `app.py` file.
- Type `flask run` the terminal window will run a server
- Click on the local address that shows up.
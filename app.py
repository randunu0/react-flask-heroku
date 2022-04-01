from email import message
from flask import Flask, render_template,request,redirect,url_for, flash, session
from bson import ObjectId     
from pymongo import MongoClient     
from flask_wtf import FlaskForm
from matplotlib.style import available
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from dotenv import load_dotenv
import certifi
import os

class InputForm(FlaskForm):
    first = StringField(label='first_name', validators=[DataRequired()])
    submit = SubmitField(label='Get')

class RegisterForm(FlaskForm):
    fname = StringField(label='First name', validators=[DataRequired()])
    lname = StringField(label='Last name', validators=[DataRequired()])
    submit = SubmitField(label='Sign up')

app = Flask(__name__)    
app.config['SECRET_KEY'] = 'any secret string'

title = "Flask MongoDB Heroku EE461L HW6"   
heading = "Hello there! Try entering YOUR first name below."  
    
cert = certifi.where()

load_dotenv() # use dotenv to hide sensitive credential as environment variables
DATABASE_URL=f'mongodb+srv://randunu0:{os.environ.get("password")}'\
              '@cluster0.pywnt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority' # get connection url from environment

client = MongoClient(DATABASE_URL, tlsCAFile=cert)
db = client.hw6DB
names = db.names 

#vWmkW6UoHUsCHxnb 


def redirect_url():    
    return url_for('index')    
  
@app.route("/users", methods=["GET", "POST"])    
def users ():    
    form = RegisterForm()
    error = ""
    names_l = names.find()    

    if form.validate_on_submit():
        if request.method == "POST":
            fname = form.fname.data    # stores first name entered by user
            lname = form.lname.data    # stores last name entered by user

            post = {'first_name':fname,
                    'last_name':lname,} # array that contains projectIDs, initially empty
            
            form.fname.data = ""
            form.lname.data = ""
            names.insert_one(post)
            return render_template('users.html', form=form, names=names_l, message=error, t=title, h=heading)    
    
    form.fname.data = ""
    form.lname.data = ""

    return render_template('users.html', form=form, names=names_l, t=title, h=heading, message=error)    
    

@app.route("/", methods=["GET", "POST"])    
def home ():   
    form = InputForm()
    error = ""

    if request.method == "POST":
        first_name = form.first.data           # stores userID entered by user

        user = names.find_one({"first_name": first_name})
        # user does not exist or password entered is incorrect
        if not user:
            error = "User Not Found"
            flash(error)
            return render_template('index.html', form=form, message=error, t=title, h=heading)    

        # user exists --> login user
        else:
            error = "Welcome back, " + first_name + " " + user['last_name']
            flash(error)
            return render_template('index.html', form=form, message=error, t=title, h=heading)    

    return render_template('index.html', form=form, message=error, t=title, h=heading)    
  

if __name__ == "__main__":    
    app.run(debug=True)   
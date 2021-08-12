from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import pymongo
import json


try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port= 27017,
        serverSelectionTimeoutMS = 1000
    )
    db =  mongo.company

    #trigger exception
    mongo.server_info()
except:
    print("ERROR - Cannot connect to db")


app = Flask(__name__)

Articles = Articles()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles= Articles )

@app.route('/article/<string:id>')
def article(id):
    return render_template('article.html', id=id)


class RegisterForm(Form):
    name= StringField('Name', [validators.Length(min=1, max=50)])
    username= StringField('Username', [validators.Length(min=4, max=25)])
    email= StringField('Email', [validators.Length(min=6, max=50)])
    password= PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm= PasswordField('Confirm Password')

@app.route('/register', methods= ['GET', 'POST'])
def register():
    form= RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name= form.name.data
        email= form.email.data
        username= form.username.data
        password= form.password.data
        user={
            "name": name,
            "email": email,
            "username": username,
            "password":password
        }
        print(user)
        dbResponse= db.users.insert_one(user)

        flash('Yopu are now registered and can login', 'success')

        redirect(url_for('index'))
    return render_template('register.html', form= form)
    
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
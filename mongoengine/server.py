from flask import Flask,render_template
from mongoengine import *
import datetime

connect('company')
app= Flask(__name__)


#Mongoengine document define
class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)
    tags = ListField(StringField(max_length=30))

    meta = {'allow_inheritance': True}

class TextPost(Post):
    content = StringField()

class LinkPost(Post):
    link_url = StringField()



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
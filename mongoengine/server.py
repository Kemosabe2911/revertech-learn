from flask import Flask, render_template, request
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


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user_email = request.form['email']
        user_fname = request.form['fname']
        user_lname = request.form['lname']
        user = User(email = user_email, first_name = user_fname, last_name= user_lname)
        print(user.email, user.first_name, user.last_name)
        user.save()
        print(user.id)

        for user in User.objects:
            print (user.email)

        user_list= User.objects()
        return render_template('post.html', users= user_list)
    else:
        return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        post_title = request.form['title']
        post = Post(title= post_title)
        post.tags = ['mongodb','mongoengine']
        post.save()
        print(post.title, post.tags,post.id)

        for post in Post.objects:
            print(post.title)
        
        #post_list= Post.objects()
        return render_template('edit_post.html')

    else:
        render_template('post.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        title_from = request.form['title1']
        title_to = request.form['title2']
        Post.objects(title=title_from).update(title= title_to)
        return render_template('delete_post.html')
    else:
        return render_template('edit_post.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        delete_title= request.form['title']
        print(delete_title)
        delete_post=Post.objects(title= delete_title)
        print(delete_post[0].title)
        delete_post_id= delete_post[0].id
        print(delete_post_id)
        Post.objects(id= delete_post_id).delete()
        print('success')
        return render_template('index.html')
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
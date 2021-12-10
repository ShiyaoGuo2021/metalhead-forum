from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from MetalWeb import MetalWeb,db, api
from MetalWeb.forms import LoginForm, RegistrationForm, TopicForm, PostForm, CommentForm, ResetPasswordForm, ResetPasswordRequestForm
from MetalWeb.models import User, load_user, Topic, Post, Comment
from datetime import datetime
from flask_restful import Resource
from requests import put, get
import json
from MetalWeb.email import send_reset_email
import requests


@MetalWeb.route('/')
def home():
	return render_template('home.html')

#home page
@MetalWeb.route('/index',methods=['GET', 'POST'])
@login_required

def index():
    form = TopicForm()
    user = load_user(current_user.get_id())
    username = user.username
    topics = Topic.query.all()
    if form.validate_on_submit():
        topic = Topic(topic_name = form.topicname.data)
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('index.html',username=username, topics = topics, form = form)


#login page
@MetalWeb.route('/login',methods=['GET','POST'])

def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html',form=form)

# for user to logout
@MetalWeb.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



@MetalWeb.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


#this page shows all the posts in the subforum
@MetalWeb.route('/index/subforum/<string:topicname>', methods = ['GET', 'POST'])
def subforum(topicname):
    topic = Topic.query.filter_by(topic_name = topicname).first()
    posts = topic.posts

    dicti = get('http://127.0.0.1:5000/users').json()
    dicti = {int(key): value for key,value in dicti.items()}
    
    
    print(dicti)
    

    
    return render_template('subforum.html', topicname = topicname, posts = posts, dicti = dicti)


# this page is for adding a post
@MetalWeb.route('/index/subforum/<string:topicname>/addPost', methods = ['GET', 'POST'])

def addPost(topicname):
    form = PostForm()
    topic = Topic.query.filter_by(topic_name = topicname).first()
    user = load_user(current_user.get_id())
    if form.validate_on_submit():
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        post = Post(title = form.title.data, content = form.content.data, topic_id = topic.id, posted_by = user.id, date = dt_string)
        db.session.add(post)
        db.session.commit()
        form.title.data=''
        form.content.data=''
        return redirect(url_for('subforum',topicname = topicname))

    return render_template('addPost.html', topicname = topicname, form = form)


#this page is for showing a specific post
@MetalWeb.route('/index/subforum/<string:topicname>/<string:title>/<int:post_id>', methods = ['GET', 'POST'])

def showPost(topicname, title, post_id):

    form = CommentForm()
    post = Post.query.filter_by(id = post_id).first()
    content  = post.content
    comments = post.comments
    dicti = {}
    users = User.query.all()
    for user in users:
        dicti[user.id] = user.username
    print(dicti)
    if form.validate_on_submit():
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        comment = Comment(content = form.comment.data, post_id = post.id, commented_by =current_user.get_id(), date = dt_string)
        db.session.add(comment)
        db.session.commit()
        form.comment.data=''
        return redirect(url_for('showPost', topicname=topicname, title=title, post_id=post_id))
    return render_template('Post.html', topicname=topicname, title=title, content=content, form=form, comments = comments, dicti=dicti)





@MetalWeb.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        u = User.query.all()[0]
        user = u.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@MetalWeb.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    u = User.query.all()[0]
    user = u.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


# get the response from a REST API 
@MetalWeb.route('/random', methods=['GET'])
def ramdom():
    r = requests.get("http://metallizer.dk/api/json/0")
    
    rr = r.text[20:]
    rrr = rr[:-2]
    responce = json.loads(rrr)
    return responce






# an API for match all user ids with their username
class User_Api(Resource):
    dicti = {}
    users = User.query.all()
    for user in users:
        dicti[user.id] = user.username

    def get(self):
        return self.dicti



api.add_resource(User_Api, '/users')










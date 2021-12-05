from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from MetalWeb import MetalWeb,db
from MetalWeb.forms import LoginForm, RegistrationForm, TopicForm, PostForm, CommentForm
from MetalWeb.models import User, load_user, Topic, Post, Comment
from datetime import datetime

@MetalWeb.route('/')
def home():
	return render_template('home.html')


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

    return render_template('index.html',username=username, topics = topics, form = form)


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


@MetalWeb.route('/index/subforum/<string:topicname>')
def subforum(topicname):
    topic = Topic.query.filter_by(topic_name = topicname).first()
    posts = topic.posts
    dicti = {}
    users = User.query.all()
    for user in users:
        dicti[user.id] = user.username

    
    return render_template('subforum.html', topicname = topicname, posts = posts, dicti = dicti)


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
        return redirect(url_for('subforum',topicname = topicname))

    return render_template('addPost.html', topicname = topicname, form = form)


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
    if form.validate_on_submit():
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        comment = Comment(content = form.comment.data, post_id = post.id, commented_by =current_user.get_id(), date = dt_string)
        db.session.add(comment)
        db.session.commit()
    return render_template('Post.html', topicname=topicname, title=title, content=content, form=form, comments = comments, dicti=dicti)














from MetalWeb import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt
from MetalWeb import MetalWeb


class User(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), unique = True, nullable=False)
	email = db.Column(db.String(120), unique = True, nullable=False)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref = 'user')
	comments = db.relationship('Comment' , backref = 'user')

	



	def __repr__(self):
		return '<User {} id {} >'.format(self.username,self.id)


	
	def set_password(self,password):
		self.password_hash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password_hash,password)


	def get_reset_password_token(self, expires_in=600):
        	return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            MetalWeb.config['SECRET_KEY'], algorithm='HS256')
	
	def verify_reset_password_token(self,token):
		try:
			id = jwt.decode(token, MetalWeb.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Topic(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	topic_name = db.Column(db.String(64), unique = True, nullable=False)
	posts = db.relationship('Post', backref = 'topic')
	def __repr__(self):
		return '<Topic {} id {}  posts {}' .format(self.topic_name,self.id, self.posts)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(30) ,nullable=False)
	content = db.Column(db.Text(),nullable=False)
	topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'),nullable=False)
	posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date = db.Column(db.String(30))
	comments = db.relationship('Comment', backref = 'post')


	def __repr__(self):
		return 'title {}  content {}  topic_id {} posted_by {} date{} comments{}  '.format(self.title,self.content,self.topic_id, self.posted_by, self.date, self.comments)

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	content = db.Column(db.Text(), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
	commented_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date = db.Column(db.String(30))

	def __repr__(self):
		return 'content {}  post_id {} commented_by {} date{}'.format(self.content, self.post_id, self.commented_by, self.date)










 

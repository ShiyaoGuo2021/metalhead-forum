from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from MetalWeb.models import User
from MetalWeb.models import Topic

class RegistrationForm(FlaskForm):
	username = StringField("Username",validators=[DataRequired()])
	email = StringField("Email",validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	passwordre = PasswordField("Repeat Password", validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField("Welcome to METAL WORLD")

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
	username = StringField("Username",validators=[DataRequired()])
	email = StringField('Email',validators=[DataRequired()])
	password = PasswordField("Password",validators=[DataRequired()])
	submit = SubmitField("Welcome back!")


class TopicForm(FlaskForm):
	topicname = StringField("Topic",validators=[DataRequired()])
	submit = SubmitField("Add this subforum!")

	def validate_topicname(self,topicname):
		topic = Topic.query.filter_by(topic_name = topicname.data).first()
		if topic is not None:
			raise ValidationError("The topic is already extant")


class PostForm(FlaskForm):
	title = StringField("Title",validators=[DataRequired()])
	content = StringField("Content", validators = [DataRequired()])
	submit = SubmitField("Add new Post")
	

class CommentForm(FlaskForm):
	comment = StringField("Comment" , validators = [DataRequired()])
	submit = SubmitField("Add new Comment")








		
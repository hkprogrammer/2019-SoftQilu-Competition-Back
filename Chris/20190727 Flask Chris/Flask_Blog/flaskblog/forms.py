from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, DecimalField, SubmitField, BooleanField, TextAreaField
from wtforms.fields import RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
	username = StringField("Username",
		validators=[DataRequired(), Length(min=3, max=15)])
	email = StringField("Email", 
		validators=[DataRequired(), Email()])
	password = PasswordField("Password", 
		validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password", 
		validators=[DataRequired(), EqualTo("password")])
	level = RadioField('I am a', choices=[('Student','student'),
		('Staff','staff'), 
		('Repairman','repairman'),
		('Administrator','adminstrator')], 
		validators=[DataRequired()])
	submit = SubmitField("Sign Up")

	def validate_username(self, username):
		
		user = User.query.filter_by(username=username.data).first()

		if user:
			raise ValidationError("Username taken.")

	def validate_email(self, email):
		
		user = User.query.filter_by(email=email.data).first()

		if user:
			raise ValidationError("Email taken.")

class LoginForm(FlaskForm):
	email = StringField("Email", 
		validators=[DataRequired(), Email()])
	password = PasswordField("Password", 
		validators=[DataRequired()])
	remember = BooleanField("Remember Me")
	submit = SubmitField("Log In")


class UpdateAccountForm(FlaskForm):
	username = StringField("Username",
		validators=[DataRequired(), Length(min=3, max=15)])
	email = StringField("Email", 
		validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField("Update")

	def validate_username(self, username):
		
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError("Username taken.")

	def validate_email(self, email):
		
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("Email taken.")

class ReportIssueForm(FlaskForm):
	title = RadioField('Type of Problem', choices=[('furniture issue','furniture issue'),('electronic issue','electronic issue'), ('Wifi issue','Wifi issue')])
	content = TextAreaField("Problem Description", validators=[DataRequired()])
	picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField("Send")


class GradeForm(FlaskForm):
	assignment = TextAreaField("Assignment", validators=[DataRequired()])
	student = TextAreaField("Student Username", validators=[DataRequired(), ])
	grade = DecimalField("Grade(on a scale of 1 to 100)", validators=[DataRequired()])
	total_points = DecimalField("Total Points for this assignment", validators=[DataRequired()])
	submit = SubmitField("Update")

	def validate_student(self, student):
		ifstudent = User.query.filter_by(username=student.data, level='Student').first()
		ifadmin = User.query.filter_by(username=student.data, level='Administrator').first()
		if (not ifstudent) and (not ifadmin):
			raise ValidationError("the username is not a student or does not exist")



class QuestionForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	content = TextAreaField("Content", validators=[DataRequired()])
	picture = FileField('Update Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField("Send")

class AnswerForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	content = TextAreaField("Content", validators=[DataRequired()])
	submit = SubmitField("Publish")

class MypueoForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	destination = RadioField('Type of Problem', choices=[('Club News','Club News'),('Athletic News','Athletic News'), ('Activities','Activities'), ('School Lunch', 'School Lunch')])
	targetclub = RadioField('Type of Problem', choices=[('Chess Club','Chess Club'),('Food Club','Food Club'), ('Magic Club','Magic Club'), ('Not a Club News', 'Not a Club News')])
	content = TextAreaField("Content", validators=[DataRequired()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField("Publish")

class RequestResetForm(FlaskForm):
	email = StringField("Email", 
		validators=[DataRequired(), Email()])
	submit = SubmitField("Request for Password Reset")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError("There is no account associated with this address.")

class ResetPasswordForm(FlaskForm):
	password = PasswordField("Password", 
		validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password", 
		validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Reset Password")







 

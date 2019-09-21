from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.fields import RadioField, DateField, SelectField
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

class PostForm(FlaskForm):
	title = SelectField('Type of Problem', choices=[('furniture issue','furniture issue'),('electronic issue','electronic issue'), ('Wifi issue','Wifi issue')])
	content = TextAreaField("Content", validators=[DataRequired()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField("Publish")

class QuestionForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	content = TextAreaField("Content", validators=[DataRequired()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField("Publish")

class AnswerForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	content = TextAreaField("Content", validators=[DataRequired()])
	submit = SubmitField("Publish")

class MypueoForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	destination = SelectField('Type of Problem', choices=[('Club News','Club News'),('Athletic News','Athletic News'), ('Activities','Activities'), ('School Lunch', 'School Lunch')])
	targetclub = SelectField('Type of Problem', choices=[('Chess Club','Chess Club'),('Food Club','Food Club'), ('Magic Club','Magic Club'), ('Not a Club News', 'Not a Club News')])
	content = TextAreaField("Content", validators=[DataRequired()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField("Publish")

class InjuryForm(FlaskForm):
	location = SelectField('Location', choices=[('Atherten','Atherten'),('Kawai Hall','Kawai Hall')])
	injury = SelectField('Type of Injury', choices=[('Sickness','Sickness'),('Cuts','Cuts')])
	note = TextAreaField("Content")
	submit = SubmitField("Publish")

class AbsenceForm(FlaskForm):
	student = StringField("Student", validators=[DataRequired()])
	reason = TextAreaField("Reason", validators=[DataRequired()])
	date = DateField('Absent Date', format='%Y-%m-%d')
	time1 = SelectField("From", choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12')])
	timestate1 = RadioField(' ', choices=[('am','am'),('pm','pm')])
	time2 = SelectField("From", choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12')])
	timestate2 = RadioField(' ', choices=[('am','am'),('pm','pm')])
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







 

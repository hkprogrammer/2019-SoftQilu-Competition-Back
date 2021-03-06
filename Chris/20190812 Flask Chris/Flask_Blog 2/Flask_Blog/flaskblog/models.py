from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	level = db.Column(db.String(20), nullable=False)
	tutor = db.Boolean()
	course1 = db.Column(db.String(50))
	course3 = db.Column(db.String(50))
	course4 = db.Column(db.String(50))
	course5 = db.Column(db.String(50))
	course6 = db.Column(db.String(50))
	course7 = db.Column(db.String(50))
	course2 = db.Column(db.String(50))
	barcode = db.Column(db.String(500))

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"('{self.id}','{self.username}')"



class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title =db.Column(db.String(20), default = "New Question")
	content = db.Column(db.String(300))
	reviewedornot = db.Column(db.Boolean, default=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	attached_image = db.Column(db.String(20))
	user = db.Column(db.String(50), nullable=False)
	quirk = db.Column(db.String(20), nullable=False)
	user_id = db.Column(db.Integer, nullable=False)
	

	def __repr__(self):
		return "Question({}, {})".format(self.title, self.date_posted)

class IssueReport(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(300))
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	attached_image = db.Column(db.String(20))
	issuetype = db.Column(db.String(20), nullable=False)
	user = db.Column(db.String(50), nullable=False)
	user_id = db.Column(db.Integer, nullable=False)
	
	def __repr__(self):
		return "Report({}, {}, {})".format(self.issuetype, self.user_id, self.date_posted)

class Grade(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	assignment = db.Column(db.String(20), nullable=False)
	course = db.Column(db.String(20), nullable = False)
	user = db.Column(db.String(20), nullable=False)#student for whom the grade is posted
	grade = db.Column(db.Integer(), nullable=False)
	points = db.Column(db.Integer(), nullable=False)
	total_points = db.Column(db.Integer(), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	teacher = db.Column(db.String(20), nullable=False)#grader
	user_id = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return "Grade({}, {})".format(self.assignment, self.grade)
	
	def __repr__(self):
		#return "News({}, {})".format(self.title, self.content)


		d = {
			"Assignment": str(self.assignment),
			"Course": str(self.course),
			"Id": str(self.id),
			"Grade": str(self.grade)



		}
		#print("sending format")
		return "{}".format(d)



class Memory(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value1=db.Column(db.String(50))
	value2=db.Column(db.String(50))

	def __repr__(self):
		return "Memory({}, {})".format(self.value1, self.value2)

class News(db.Model):### for mypueo
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20), nullable=False, default="m")###title
	content = db.Column(db.String(20), nullable=False)###content
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	attached_image = db.Column(db.String(20))
	newstype = db.Column(db.String(20), nullable=False)
	clubname = db.Column(db.String(20))
	user = db.Column(db.String(50))
	user_id = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		#return "News({}, {})".format(self.title, self.content)


		d = {
			"Title": str(self.title),
			"Id": str(self.id),
			"Content": str(self.content)
		}
		#print("sending format")
		return "{}".format(d)

		#return [self.id,self.title,self.content]

		#return {self.title,self.id,self.content}
class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	commenter = db.Column(db.String(20), nullable=False)
	commenttitle = db.Column(db.String(20))
	comment = db.Column(db.String(500), nullable=False)
	reference = db.Column(db.String(20), nullable=False)

	def __repr__(self):	
		return "Comment({}, {})".format(self.commenter, self.comment)

class Club(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	clubname = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return "({}, {})".format(self.clubname, self.clubname)

class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	coursename = db.Column(db.String(20), nullable=False, unique=True)
	teacher = db.Column(db.String(20), nullable=False)
	students = db.Column(db.String(500), nullable=False)
	period = db.Column(db.String(10), nullable=False)


	def __repr__(self):
		return "({}, {})".format(self.id, self.coursename)




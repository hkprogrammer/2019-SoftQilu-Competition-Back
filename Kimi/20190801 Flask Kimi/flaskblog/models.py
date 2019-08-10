from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

membership = db.Table('membership',
	db.Column('member_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('club_id', db.Integer, db.ForeignKey('clubs.id'))
	)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	level = db.Column(db.String(20), nullable=False)
	posts = db.relationship('Post', backref='student', lazy=True )
	memberof = db.relationship('Clubs', secondary=membership, backref=db.backref('members', lazy='dynamic'))

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
		return "User({}, {}, {})".format(self.username, self.email, self.image_file)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	assignment = db.Column(db.String(20), nullable=False, default="m")
	grade = db.Column(db.String(20), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	attached_image = db.Column(db.String(20))
	posttype = db.Column(db.String(20), nullable=False)
	newstype = db.Column(db.String(20))
	clubtype = db.Column(db.String(20))
	reviewedornot = db.Column(db.Boolean, default=False)
	quirk = db.Column(db.String(20), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return "Post({}, {})".format(self.assignment, self.grade)

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	commenter = db.Column(db.String(20), nullable=False)
	commenttitle = db.Column(db.String(20))
	comment = db.Column(db.String(500), nullable=False)
	reference = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return "Comment({}, {})".format(self.commenter, self.comment)

class Clubs(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	club = db.Column(db.String(20), nullable=False)


import secrets
import os
from PIL import Image
#from flask import render_template, url_for, flash, redirect, request, abort
from flask import *
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm, QuestionForm, AnswerForm, MypueoForm, InjuryForm, AbsenceForm
from flaskblog.models import User, Post, Comment, Clubs, membership
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/")
@app.route("/home")
@login_required
def home():
	return "Home"

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static','profile_pics', picture_fn)
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn

def save_picture_for_attachments(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static','attachment_pics', picture_fn)
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn

##Later
@app.route("/report")
@login_required
def report():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(posttype="Report").paginate(page=page, per_page=5)
	return render_template('reports.html', posts=posts, title="Pending Reports")

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		else:
			current_user.image_file = ""
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		return redirect(url_for('account'))
	image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
	return render_template('account.html', title="Student Account", image_file=image_file, form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		if form.email.data.endswith('midpac.edu'):
			user = User(username=form.username.data, email=form.email.data, password=hashed_password, level="Faculty")
		else:
			user = User(username=form.username.data, email=form.email.data, password=hashed_password, level="Student")
		db.session.add(user)
		db.session.commit()
		flash("Account created for {}.".format(form.username.data), 'success')
		return redirect(url_for('login'))
	return render_template("register.html", title="Register", form=form)


### Modified by Hitoki 7/24/2019
@app.route("/login", methods=['GET', 'POST'])
def login():
	# if current_user.is_authenticated:
	# 	return redirect(url_for('home'))
	# form = LoginForm()

	## I'm using processing and im inputing email, password, and remember as parameters in my http post request
	

	data = request.form or request.args
	dataemail = str(data["email"]) or None
	datapassword = str(data["password"]) or None
	dataremember = bool(data["remember"]) or None

	msg = {
		"email": None,
		"password" : None,
		"remember" : None,
		"login" : False
	}


	#user = User.query.filter_by(email=form.email.data).first()
	user = User.query.filter_by(email=dataemail).first()
	#if user and bcrypt.check_password_hash(user.password, form.password.data):
	if user and bcrypt.check_password_hash(user.password, datapassword):
		#login_user(user, remember=form.remember.data)
		login_user(user, remember=dataremember)
		#return redirect(url_for('home'))
		p = ""
		for i in datapassword:
			p += "*"
			
		msg = {
			"email": dataemail,
			"password" : p,
			"remember" : dataremember,
			"login" : True 
		}

		
	else:
		msg = {
			"email": dataemail,
			"password" : p,
			"remember" : dataremember,
			"login" : False
		}
	js = json.dumps(msg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp
	# return render_template("login.html", title="Login", form=form)
###Modify Finish
@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('register'))

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture_for_attachments(form.picture.data)
			post = Post(assignment=form.title.data, grade=form.content.data, student=current_user, attached_image=picture_file, posttype="Report", quirk=secrets.token_hex(8))
		else:
			post = Post(assignment=form.title.data, grade=form.content.data, student=current_user, posttype="Report", quirk=secrets.token_hex(8))
		db.session.add(post)
		db.session.commit()
		flash("your post has been created", "success")
		return redirect(url_for("report"))
	return render_template("create_post.html", title="Issue Reporting", form=form, legend="File a Report")

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id):
	post = Post.query.get_or_404(post_id)
	page = request.args.get('page', 1, type=int)
	comments = Comment.query.filter_by(reference=post.quirk).paginate(page=page, per_page=5)
	form = AnswerForm()
	
	###Modified by Hitoki 7/24/2019
	post.posttype = str(post.posttype)
	if post.posttype == "Report" or post.posttype == "Announcement":
	###Modified finish
		return render_template("post.html", title=post.assignment, post=post)
	elif post.posttype == "Injury":
		return render_template("injurypost.html", title=post.assignment, post=post)
	elif post.posttype == "Question":
		if form.validate_on_submit():
			comment = Comment(commenter=current_user.username, comment=form.content.data, commenttitle=form.title.data, reference=post.quirk)
			db.session.add(comment)
			db.session.commit()
			post.reviewedornot = True
			db.session.commit()
			return redirect(url_for("post", post_id=post.id))
		return render_template("studypost.html", title=post.assignment, post=post, comments=comments, legend="Add your comment here", form=form)
	###Modified by Hitoki 7/24/2019
	
	msg = {
		"Message" : "Not Valid Response",
		"posttype" : post.posttype,
		"post overall" : post
	}

	js = json.dumps(msg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp
	###Modify End

###Modify by Hitoki 7/24/2019
@app.route('/post/getNum' , methods=['GET','POST'])
def getpostnum():

	basenum = 0
	try:
		while True:
			basenum +=1
			post = Post.query.get_or_404(basenum)

	except:
		print("database overflow, current basenum value is ", basenum)

	finally:	
		basenum -= 1
		print("basenum is", basenum)
		return str(basenum)


###Modify Finish

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.student != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		if form.picture.data:
			attachment = save_picture_for_attachments(form.picture.data)
			post.attached_image = attachment
		post.assignment = form.title.data
		post.grade = form.content.data
		db.session.commit()
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.assignment
		form.content.data = post.grade
	return render_template("create_post.html", title="Update Report", form=form, legend="Update Report")

@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if current_user.level != "Faculty":
		abort(403)
	db.session.delete(post)
	db.session.commit()
	if post.posttype == "Report":
		return redirect(url_for("report"))
	elif post.posttype == "Announcement":
		return redirect(url_for("mypueo"))
	elif post.posttype == "Injury":
		return redirect(url_for("injury"))
	elif post.posttype == "Question":
		return redirect(url_for("studybuddieshome"))

@app.route("/user/<string:username>")
@login_required
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(student=user).paginate(page=page, per_page=5)
	return render_template('user_posts.html', posts=posts, user=user)

@app.route("/studybuddies/post", methods=['GET', 'POST'])
@login_required
def study_post():
	form = QuestionForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture_for_attachments(form.picture.data)
			post = Post(assignment=form.title.data, grade=form.content.data, student=current_user, attached_image=picture_file, posttype="Question", quirk=secrets.token_hex(8))
		else:
			post = Post(assignment=form.title.data, grade=form.content.data, student=current_user, posttype="Question", quirk=secrets.token_hex(8))
		db.session.add(post)
		db.session.commit()
		return redirect(url_for("studybuddieshome"))
	return render_template("file_question.html", title="Study Buddies", form=form, legend="Ask a Question")

@app.route("/studybuddies")
@login_required
def studybuddieshome():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(posttype="Question").paginate(page=page, per_page=5)
	return render_template('studybuddieshome.html', posts=posts, title="Student Questions")

@app.route("/mypueo/post", methods=['GET', 'POST'])
@login_required
def mypeo_post():
	form = MypueoForm()
	if form.validate_on_submit():
		if form.targetclub.data != 'Not a Club':	
			if form.picture.data:
				picture_file = save_picture_for_attachments(form.picture.data)
				post = Post(assignment=form.title.data, grade=form.content.data, student=current_user, attached_image=picture_file, posttype="Announcement", quirk=secrets.token_hex(8), newstype=form.destination.data, clubtype=form.targetclub.data)
			else:
				post = Post(assignment=form.title.data, grade=form.content.data, student=current_user, posttype="Announcement", quirk=secrets.token_hex(8), newstype=form.destination.data, clubtype=form.targetclub.data)
		else:
			if form.picture.data:
				picture_file = save_picture_for_attachments(form.picture.data)
				post = Post(assignment=form.title.data, grade=form.content.data, student=current_user, attached_image=picture_file, posttype="Announcement", quirk=secrets.token_hex(8), newstype=form.destination.data)
			else:
				post = Post(assignment=form.title.data, grade=form.content.data, student=current_user, posttype="Announcement", quirk=secrets.token_hex(8), newstype=form.destination.data)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for("mypueo"))
	return render_template("mypueopost.html", title="Post Accouncement", form=form, legend="Post Announcement")

@app.route("/mypueo", methods=['GET', 'POST'])
@login_required
def mypueo():
	return render_template("mypueo.html", title="Mypueo")

@app.route("/mypueo/clubnews", methods=['GET', 'POST'])
@login_required
def clubnews():
	if current_user.level == "Student":
		clubs = []
		for x in current_user.memberof:
			clubs.append(x.club)
		page = request.args.get('page', 1, type=int)
		posts = Post.query.filter_by(newstype='Club News').paginate(page=page, per_page=5)
		return render_template('clubnews.html', posts=posts, title="Club News", clubs=clubs)
	elif current_user.level == "Faculty":
		page = request.args.get('page', 1, type=int)
		posts = Post.query.filter_by(newstype='Club News').paginate(page=page, per_page=5)
		return render_template('clubnews.html', posts=posts, title="Club News")

@app.route("/mypueo/athleticnews", methods=['GET', 'POST'])
@login_required
def athleticnews():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(newstype='Athletic News').paginate(page=page, per_page=5)
	return render_template('athleticnews.html', posts=posts, title="Athletic News")

@app.route("/mypueo/Activities", methods=['GET', 'POST'])
@login_required
def actvities():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(newstype='Athletics').paginate(page=page, per_page=5)
	return render_template('activities.html', posts=posts, title="Club News")

@app.route("/mypueo/schoollunch", methods=['GET', 'POST'])
@login_required
def schoollunch():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(newstype='School Lunch').paginate(page=page, per_page=5)
	return render_template('schoollunch.html', posts=posts, title="Club News")

@app.route("/injury/post", methods=['GET', 'POST'])
@login_required
def injurypost():
	form = InjuryForm()
	if form.validate_on_submit():
		if form.note.data:
			post = Post(assignment=form.location.data, grade=form.injury.data, attached_image=form.note.data, student=current_user, posttype="Injury", quirk=secrets.token_hex(8))
		else:
			post = Post(assignment=form.location.data, grade=form.injury.data, student=current_user, posttype="Injury", quirk=secrets.token_hex(8))
		db.session.add(post)
		db.session.commit()
		return redirect(url_for("injury"))
	return render_template('injuryform.html', title="Injury Submission", legend="Injury Submission", form=form)

@app.route("/injury", methods=['GET', 'POST'])
@login_required
def injury():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(posttype="Injury").paginate(page=page, per_page=5)
	return render_template('injury.html', posts=posts, title="Injury Reports")

@app.route("/absence", methods=['GET', 'POST'])
@login_required
def absence():
	form = AbsenceForm()
	if form.validate_on_submit():
		msg = Message('Your child, ' + str(form.student.data) + ', will be permitted with absence between ' + str(form.time1.data) + str(form.timestate1.data) + ' and ' + str(form.time2.data) + str(form.timestate2.data) + ' on ' + str(form.date.data) + ' due to ' + str(form.reason.data) + '.', sender='testingnowpls@gmail.com', recipients=['kimiweng@student.midpac.edu'])
		mail.send(msg)
		return redirect(url_for("home"))
	return render_template('absenceform.html', form=form, legend='Absence Request', title='Absence Request')

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
	msg.body = url_for('reset_token', token=token, _external=True)
	mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		return redirect(url_for('login'))
	return render_template('reset_request.html', title="Reset Password", form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash("Invalid token", "warning")
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('reset_token.html', title="Reset Password", form = form)



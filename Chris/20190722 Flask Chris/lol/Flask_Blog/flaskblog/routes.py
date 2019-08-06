import secrets
import os
from PIL import Image
from flask import *
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, GradeForm, QuestionForm, ReportIssueForm, RequestResetForm, ResetPasswordForm, QuestionForm, AnswerForm, MypueoForm
from flaskblog.models import User, Question, Grade, Course, IssueReport, Comment
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/")
@app.route("/home")
@login_required
def home():
	page = request.args.get('page', 1, type=int)
	posts = Question.query.paginate(page=page, per_page=5)
	return render_template('home.html', posts=posts, title="Home Page")

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
		user = User(username=form.username.data, email=form.email.data, password=hashed_password, level=form.level.data)
		db.session.add(user)
		db.session.commit()
		flash("Account created for {}.".format(form.username.data), 'success')
		return redirect(url_for('login'))
	return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):

			login_user(user, remember=form.remember.data)

			next_page = request.args.get('next')  

			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('register'))


@app.route("/user/<string:username>")
@login_required
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(student=user).paginate(page=page, per_page=5)
	return render_template('user_posts.html', posts=posts, user=user)



@app.route("/studybuddies")
@login_required
def studybuddieshome():
	page = request.args.get('page', 1, type=int)
	posts = Question.query.paginate(page=page, per_page=5)
	#return type(posts)
	return render_template('studybuddieshome.html', posts=posts, title="Student Questions")

@app.route("/mypueo/post", methods=['GET', 'POST'])
@login_required
def mypeo_post():
	form = MypueoForm()
	if form.validate_on_submit():
		if form.targetclub.data != 'Not a Club':	
			if form.picture.data:
				picture_file = save_picture_for_attachments(form.picture.data)
				post = Post(assignment=form.title.data, grade=form.content.data, student=current_user, attached_image=picture_file, posttype="Announcement", newstype=form.destination.data, clubtype=form.targetclub.data)
			else:
				post = Post(assignment=form.title.data, grade=form.content.data, student=current_user, posttype="Announcement", newstype=form.destination.data, clubtype=form.targetclub.data)
		else:
			if form.picture.data:
				picture_file = save_picture_for_attachments(form.picture.data)
				post = Post(assignment=form.title.data, grade=form.content.data, student=current_user, attached_image=picture_file, posttype="Announcement", newstype=form.destination.data)
			else:
				post = Post(assignment=form.title.data, grade=form.content.data, student=current_user, posttype="Announcement", newstype=form.destination.data)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for("mypueo"))
	return render_template("mypueopost.html", title="Post Accouncement", form=form, post=post, legend="Post Announcement")

@app.route("/mypueo", methods=['GET', 'POST'])
@login_required
def mypueo():
	return render_template("mypueo.html", title="Mypueo")

@app.route("/mypueo/clubnews", methods=['GET', 'POST'])
@login_required
def clubnews():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(newstype='Club News').paginate(page=page, per_page=5)
	return render_template('clubnews.html', posts=posts, title="Club News")

@app.route("/mypueo/athleticnews", methods=['GET', 'POST'])
@login_required
def athleticnews():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter_by(newstype='Athletic News').paginate(page=page, per_page=5)
	return render_template('athleticnews.html', posts=posts, title="Athletic News")

@app.route("/mypueo/activities", methods=['GET', 'POST'])
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

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
	msg.body = url_for('reset_token', token=token, _external=True)
	mail.send(msg)

@app.route("/class/create", methods=['GET', 'POST'])
@login_required
def new_class():
	if current_user.level != 'Teacher':
		abort(403)
	form = CourseForm()
	if form.validate_on_submit():
		post = Course(course_name=form.title.data, teacher=form.teacher.data, students=form.students.data)
		db.session.add(post)
		db.session.commit()
		flash("The class has been created", "success")
		return redirect(url_for("home"))
	return render_template("create_post.html", title="Issue Reporting", form=form, legend="File a Report")

@app.route("/report_issue/new", methods=['GET', 'POST'])
@login_required
def report_issue():
	if current_user.level == 'Repairman':
		abort(403)
	form =ReportIssueForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture_for_attachments(form.picture.data)
			post = IssueReport(issuetype=form.title.data, content=form.content.data, user=current_user, user_id=current_user.id, attached_image=form.picture.data)
		else:
			post = IssueReport(issuetype=form.title.data, content=form.content.data, user=current_user, user_id=current_user.id)
		db.session.add(post)
		db.session.commit()
		flash("The issue has been reported. Thank you for your coorperation. ", "success")
		return redirect(url_for("home"))
	return render_template("create_post.html", title="Issue Reporting", form=form, legend="File a Report")

@app.route("/view_report/<int:post_id>", methods=['GET', 'POST'])
@login_required
def view_issue(post_id):
	post = IssueReport.query.get_or_404(post_id)
	page = request.args.get('page', 1, type=int)
	return render_template("studypost.html", title=post.title, post=post.content)


@app.route("/post_question", methods=['GET', 'POST'])
@login_required
def post_question():
	if current_user.level != 'Student':
		abort(403)
	form = QuestionForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture_for_attachments(form.picture.data)
			#post = Question(title=form.title.data, content=form.content.data, student=current_user, user_id=current_user.id, attached_image=picture_file, quirk=secrets.token_hex(8))
			post = Question(title=form.title.data, content=form.content.data, student=current_user.id, user_id=current_user.id, quirk=secrets.token_hex(8))
		
		else:
			#post = Question(title=form.title.data, content=form.content.data, student=current_user, user_id=current_user.id, quirk=secrets.token_hex(8))
			post = Question(title=form.title.data, content=form.content.data, student=current_user.id, user_id=current_user.id, quirk=secrets.token_hex(8))
		


		db.session.add(post)
		db.session.commit()


		#flash("your question has been posted", "success")

		returnfile = {
			"Title" : form.title.data,
			"Content" : form.content.data,
			"ttached Images" : form.picture.data,
			"Message" : "Success"
		}
		js = json.dumps(returnfile)
		print(form.title.data, form.content.data, form.picture.data)
		print(str(type(form)))
		resp = Response(js, status=200, mimetype='application/json')
		return resp
		#return str(post)
	return render_template("file_question.html", title="Study Buddies", form=form, legend="Ask a Question")

@app.route("/view_question/<int:post_id>", methods=['GET', 'POST'])
@login_required
def view_question(post_id):
	post = Question.query.get_or_404(post_id)
	page = request.args.get('page', 1, type=int)
	comments = Comment.query.filter_by(reference=post.quirk).paginate(page=page, per_page=5)
	if current_user.level != 'student':
		return render_template("studypost.html", title=post.assignment, post=post, comments=comments)
	else:
		form = AnswerForm()
		if form.validate_on_submit():
			comment = Comment(commenter=current_user.username, comment=form.content.data, commenttitle=form.title.data, reference=post.quirk)
			db.session.add(comment)
			db.session.commit()
			post.reviewedornot = True
			db.session.commit()
			return redirect(url_for("post", post_id=post.id))
		return render_template("studypost.html", title=post.assignment, post=post, comments=comments, legend="Add your comment here", form=form)

@app.route("/post_grade", methods=['GET', 'POST'])
@login_required
def post_grade():
	if current_user.level != 'staff':
		abort(403)
	form = GradeForm()
	if form.validate_on_submit():
		post = Grade(assignment=form.title.data, grade=form.grade.data, points=string(float(form.grade.data)*float(form.total_points.data)/100), student=form.student.data)
		db.session.add(post)
		db.session.commit()
		flash("The grade has been posted. ", "success")
		return redirect(url_for("home"))
	return render_template("create_post.html", title="Grade Updating", form=form, legend="Update a Grade")

@app.route("/view_grade/<int:post_id>", methods=['GET', 'POST'])
@login_required
def view_grade(post_id):
	post = Grade.query.get_or_404(post_id)
	if post.student != current_user:
		abort(403)
	page = request.args.get('page', 1, type=int)
	return render_template("studypost.html", title=post.student, post=post, comments=comments)


@app.route("/view_grade/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_grade(post_id):
	post = Grade.query.get_or_404(post_id)
	if post.student != current_user:
		abort(403)
	form = GradeForm()
	if form.validate_on_submit():
		post.assignment = form.title.data
		post.grade = form.content.data
		db.session.commit()
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.assignment
		form.content.data = post.grade
	return render_template("create_post.html", title="Update Grade", form=form, legend="Update Report")

@app.route("/view_report/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_report(post_id):
	post = Grade.query.get_or_404(post_id)
	if current_user.level == student:
		abort(403)
	form = IssueReportForm()
	if form.validate_on_submit():
		post.issuetype = form.title.data
		post.content = form.content.data
		db.session.commit()
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.issuetype
		form.content.data = post.content
	return render_template("create_post.html", title="Update Report", form=form, legend="Update Report")


@app.route("/view_report/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_report(post_id):
	post = IssueReport.query.get_or_404(post_id)
	if current_user.level != post.user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for("home"))

@app.route("/view_question/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_question(post_id):
	post = Question.query.get_or_404(post_id)
	if current_user.level != post.user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for("home"))

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



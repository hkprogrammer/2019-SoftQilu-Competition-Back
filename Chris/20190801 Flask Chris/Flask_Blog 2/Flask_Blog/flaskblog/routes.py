import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, ClubForm, GradeForm, QuestionForm, ReportIssueForm, RequestResetForm, ResetPasswordForm, QuestionForm, AnswerForm, NewsForm
from flaskblog.models import User, Question, Grade, IssueReport, Comment, News, Memory
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

admin = User.query.filter_by(username='admin').first()
if not admin: 
	admin = User(username= 'admin', email='admin@gmail.com', password = bcrypt.generate_password_hash('admin').decode('utf-8'), level='Administrator')
	db.session.add(admin)
	db.session.commit()

@app.route("/")
@app.route("/home")
@login_required
def home():
	if current_user.level == 'Repairman':
		page = request.args.get('page', 1, type=int)
		reports = IssueReport.query.paginate(page=page, per_page=5)
		return render_template('home.html', reports=reports, title="Home Page")
	elif current_user.level == 'Administrator':
		page = request.args.get('page', 1, type=int)
		reports = IssueReport.query.paginate(page=page, per_page=5)
		questions = Question.query.paginate(page=page, per_page=5)
		newss = News.query.paginate(page=page, per_page=5)
		return render_template('home.html', questions=questions, newss=newss, reports=reports, title="Home Page")
	else:
		page = request.args.get('page', 1, type=int)
		questions = Question.query.paginate(page=page, per_page=5)
		newss = News.query.paginate(page=page, per_page=5)
		return render_template('home.html', questions=questions, newss=newss, title="Home Page")

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



@app.route("/account/update", methods=['GET', 'POST'])
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
	return render_template('account.html', title="Student Account", form=form)

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
	else:
		flash('that username or email is already taken', 'danger')
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
	attached_image=user.image_file
	questions = Question.query.filter_by(user=username).paginate(page=page, per_page=5)
	grades = Grade.query.filter_by(user=username).paginate(page=page, per_page=5)
	return render_template('user_posts.html', questions=questions, grades=grades, user=user, attached_image=attached_image)


@app.route("/news/post/<int:num>", methods=['GET', 'POST'])
@login_required
def news_post(num=0): #num = 0 is a default
	if current_user.level != ('Staff2' and 'Administrator'):
		abort(403)
	form1 = NewsForm() ## Form page 1
	form2 = ClubForm() ## Form page 2
	###
	# num have three variants, 0, 1, 2.
	# 0 represents first entry
	# 1 represents second entry from post_news.html
	# 2 represents third entry from post_news_clubname.html
	# each number are being called at the action attributes in each html file
	###
	if num == 1: ## Second entry
		if form1.validate_on_submit():
			if form1.picture.data:
				picture_file = save_picture_for_attachments(form1.picture.data)
				post = News(title=form1.title.data, content=form1.content.data, user=current_user.username, attached_image=picture_file, newstype=form1.destination.data, user_id= current_user.id)
			else:
				post = News(title=form1.title.data, content=form1.content.data, user=current_user.username, newstype=form1.destination.data, user_id= current_user.id)
				db.session.add(post)
				db.session.commit()
			if form1.destination.data == 'Club News':
				memory = Memory(value1=post.id, value2=post.user)
				db.session.add(memory)
				db.session.commit()
				return render_template("post_news_clubname.html", title="Choose Club Name", form=form2, legend="Choose Club Name")
			else:
				return redirect(url_for("home"))
	elif num == 2: ## Third Entry
		if form2.validate_on_submit():
				memory = Memory.query.filter_by(value2=current_user.username).first()
				post = News.query.filter_by(id=memory.value1).first()
				post.clubname = form2.club.data
				db.session.delete(memory)
				db.session.commit()

				return redirect(url_for("home"))

	elif num == 0: ## First Entry

		return render_template("post_news.html", title="Post Accouncement", form=form1, legend="Post Announcement")
	
	else: ## First/Error Entry
		print("Error at news posting input num:", str(num))
		return render_template("post_news.html", title="Post Accouncement", form=form1, legend="Post Announcement")
	
@app.route("/view_news/<int:post_id>", methods=['GET', 'POST'])
@login_required
def view_news(post_id):
	post = News.query.get_or_404(post_id)
	page = request.args.get('page', 1, type=int)
	
	return render_template("view_news.html", title=post.title, post=post)


@app.route("/view_news/clubs", methods=['GET', 'POST'])
@login_required
def clubnews():
	page = request.args.get('page', 1, type=int)
	posts = News.query.filter_by(newstype='Club News').paginate(page=page, per_page=5)
	return render_template('mypueo.html', posts=posts, title="Club News")

@app.route("/view_news/athletic", methods=['GET', 'POST'])
@login_required
def athleticnews():
	page = request.args.get('page', 1, type=int)
	posts = News.query.filter_by(newstype='Athletic News').paginate(page=page, per_page=5)
	return render_template('mypueo.html', posts=posts, title="Athletic News")

@app.route("/view_news/activities", methods=['GET', 'POST'])
@login_required
def actvities():
	page = request.args.get('page', 1, type=int)
	posts = News.query.filter_by(newstype='Athletics').paginate(page=page, per_page=5)
	return render_template('mypueo.html', posts=posts, title="School News")

@app.route("/view_news/schoollunch", methods=['GET', 'POST'])
@login_required
def schoollunch():
	page = request.args.get('page', 1, type=int)
	posts = News.query.filter_by(newstype='School Lunch').paginate(page=page, per_page=5)
	return render_template('mypueo.html', posts=posts, title="Club News")

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
	msg.body = url_for('reset_token', token=token, _external=True)
	mail.send(msg)


@app.route("/report_issue/new", methods=['GET', 'POST'])
@login_required
def report_issue():
	if current_user.level == 'Repairman':
		abort(403)
	form =ReportIssueForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture_for_attachments(form.picture.data)
			post = IssueReport(issuetype=form.title.data, content=form.content.data, user=current_user.username, user_id=current_user.id, attached_image=form.picture.data)
		else:
			post = IssueReport(issuetype=form.title.data, content=form.content.data, user=current_user.username, user_id=current_user.id)
		db.session.add(post)
		db.session.commit()
		flash("The issue has been reported. Thank you for your coorperation. ", "success")
		return redirect(url_for("home"))
	return render_template("report_issue.html", title="Issue Reporting", form=form, legend="File a Report")

@app.route("/view_report/<int:post_id>", methods=['GET', 'POST'])
@login_required
def view_report(post_id):
	post = IssueReport.query.get_or_404(post_id)
	page = request.args.get('page', 1, type=int)
	
	return render_template("view_report.html", title=post.issuetype, post=post)


@app.route("/post_question", methods=['GET', 'POST'])
@login_required
def post_question():
	if current_user.level != ('Student' and 'Administrator'):
		abort(403)
	form = QuestionForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture_for_attachments(form.picture.data)
			post = Question(title=form.title.data, content=form.content.data, user=current_user.username, user_id=current_user.id, attached_image=picture_file, quirk=secrets.token_hex(8))
		else:
			post = Question(title=form.title.data, content=form.content.data, user=current_user.username, user_id=current_user.id, quirk=secrets.token_hex(8))
		db.session.add(post)
		db.session.commit()
		flash("your question has been posted", "success")
		return redirect(url_for("home"))
	return render_template("post_question.html", title="Study Buddies", form=form, legend="Ask a Question")

@app.route("/view_question/<int:post_id>", methods=['GET', 'POST'])
@login_required
def view_question(post_id):
	post = Question.query.get_or_404(post_id)
	page = request.args.get('page', 1, type=int)
	comments = Comment.query.filter_by(reference=post.quirk).paginate(page=page, per_page=5)
	
	user_level = current_user.level
	form = AnswerForm()
	if current_user.level == ('Repairman' or 'Administrator'):
		return render_template("studypost.html", title=post.title, user_level=user_level, post=post, comments=comments)
	else:
		if form.validate_on_submit():
			comment = Comment(commenter=current_user.username, comment=form.content.data, commenttitle=form.title.data, reference=post.quirk)
			db.session.add(comment)
			db.session.commit()
			post.reviewedornot = True
			db.session.commit()
			return redirect(url_for("home", post_id=post.id))
		return render_template("view_question.html", title=post.title, form = form, user_level=user_level, post=post, comments=comments, legend="Add your comment here")

@app.route("/post_grade", methods=['GET', 'POST'])
@login_required
def post_grade():
	if current_user.level != ('Staff' and 'Administrator'):
		abort(403)
	form = GradeForm()
	if form.validate_on_submit():
		post = Grade(assignment=form.assignment.data, grade=float(form.grade.data), points=(float(form.grade.data)*float(form.total_points.data)/100), total_points=float(form.total_points.data), user=form.student.data, teacher=current_user.username, user_id=current_user.id)
		db.session.add(post)
		db.session.commit()
		flash("The grade has been posted. ", "success")
		return redirect(url_for("home"))
	else:
		flash('the username you entered is not a student or does not exist', 'danger')
	return render_template("post_grade.html", title="Grade Posting", form=form, legend="Post a Grade")

@app.route("/view_grade/<int:post_id>", methods=['GET', 'POST'])
@login_required
def view_grade(post_id):
	post = Grade.query.get_or_404(post_id)
	if (post.user != (current_user)) and (current_user.level !='Administrator'):
		abort(403)
	page = request.args.get('page', 1, type=int)
	attached_image=current_user.image_file
	return render_template("view_grade.html", title=post.user, post=post, attached_image=attached_image)


@app.route("/view_grade/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_grade(post_id):
	post = Grade.query.get_or_404(post_id)
	
	if (post.user != (current_user)) and (current_user.level !='Administrator'):
		abort(403)
	form = GradeForm()
	if form.validate_on_submit():
		post.assignment = form.assignment.data
		post.user = form.student.data
		post.grade = form.grade.data
		post.total_points = form.total_points.data
		db.session.commit()
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.assignment.data = post.assignment
		form.student.data = post.user
		form.grade.data = post.grade
		form.total_points.data = post.total_points
	return render_template("update_grade.html", title="Update Grade", form=form, legend="Update Grade")

@app.route("/view_report/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_report(post_id):
	post = IssueReport.query.get_or_404(post_id)
	if current_user.level == 'Student':
		abort(403)
	form = IssueReportForm()
	if form.validate_on_submit():
		post.issuetype = form.title.data
		post.content = form.content.data
		post.attached_image=form.picture.data
		db.session.commit()
		return redirect(url_for('view_report', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.issuetype
		form.content.data = post.content
		form.picture.data = post.attached_image
	return render_template("update_report.html", image_file = image_file, title="Update Report", form=form, legend="Update Report")


@app.route("/view_report/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_report(post_id):
	post = IssueReport.query.get_or_404(post_id)
	if (post.user != (current_user)) and (current_user.level !='Administrator'):
		abort(403)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for("home"))

@app.route("/view_question/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_question(post_id):
	post = Question.query.get_or_404(post_id)
	if (post.user != (current_user)) and (current_user.level !='Administrator'):
		abort(403)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for("home"))

@app.route("/view_grade/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_grade(post_id):
	post = Grade.query.get_or_404(post_id)
	if (post.user != (current_user)) and (current_user.level !='Administrator'):
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



import secrets
import os
from PIL import Image
#from flask import render_template, url_for, flash, redirect, request, abort, json
import flask
from flask import *
from flaskblog import app, db, bcrypt, mail
from flaskblog.models import User, Question, Course, Grade, IssueReport, Comment, News, Memory, Club
from flaskblog.forms import RegistrationForm, GradeCourseForm, ClubForm, CourseForm, LoginForm, UpdateAccountForm, NewsClubForm, GradeForm, QuestionForm, ReportIssueForm, RequestResetForm, ResetPasswordForm, QuestionForm, AnswerForm, NewsForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
###levels: 1=student; 2=student tutor; 3=teacher; 4=repairman; 5=administrator

admin = User.query.filter_by(username='admin').first()
if not admin: 
	admin = User(username= 'admin', email='admin@gmail.com', password = bcrypt.generate_password_hash('admin').decode('utf-8'), level='5')
	db.session.add(admin)
	db.session.commit()

@app.route("/")
@app.route("/home")
#@login_required
def home():
	page = request.args.get('page', 1, type=int)
	reports = IssueReport.query.paginate(page=page,per_page=1000)
	questions = Question.query.paginate(page=page, per_page=1000)
	#newss = News.query.paginate(page=page, per_page=1000)
	newss = News.query.paginate(page=page, per_page=1000)

	R = reports.__dict__
	Q = questions.__dict__

	N = newss.__dict__
	#print(type(N))

	#print(N["items"])

	
	bigmsg = {"News":[], "Reports": [], "Questions":[]}
	for x in N["items"]:
		x = x.__dict__
		#print("How many items: ", x)
		detailedmsg = {
			"title" : str(x["title"]) or " ",
			"user" : str(x["user"]),
			"content" : str(x["content"]),
			"date_posted" : str(x["date_posted"]),
			"attached_image" : str(x["attached_image"]) or "",
			"newstype" : str(x["newstype"]),
			"clubname" : str(x["clubname"]) or "",
			"user_id" : str(x["user_id"])
		
		}
		bigmsg["News"].append(detailedmsg)


	for x in Q["items"]:
		x = x.__dict__
		#print("How many items: ", x)
		detailedmsg = {
			"id" : str(x["id"]) or "",
			"title" : str(x["title"]) or " ",
			"user" : str(x["user"]),
			"content" : str(x["content"]),
			"reviewedornot" : str(x["reviewedornot"]) or "",
			"date_posted" : str(x["date_posted"]),
			"attached_image" : str(x["attached_image"]) or "",
			"user_id" : str(x["user_id"])
		
		}
		bigmsg["Questions"].append(detailedmsg)

	
	for x in R["items"]:
		x = x.__dict__
		#print("How many items: ", x)
		detailedmsg = {
			"id" : str(x["id"]) or "",
			"title" : str(x["issuetype"]) or " ",
			"user" : str(x["user"]),
			"content" : str(x["content"]),
			"date_posted" : str(x["date_posted"]),
			"attached_image" : str(x["attached_image"]) or "",
			"issuetype" : str(x["issuetype"]),
			
			"user_id" : str(x["user_id"])
		
		}
		bigmsg["Reports"].append(detailedmsg)

	


		
	
	#str(JsonNews[""]),
	

	#JsonNews = N["items"][0].__dict__
	
	#print(bigmsg)


	#if current_user.level == '4':
		

		#return render_template('home.html', reports=reports, title="Home Page")

	#elif current_user.level == '5':

		#return render_template('home.html', questions=questions, newss=newss, reports=reports, title="Home Page")

	#else:

		#return render_template('home.html', questions=questions, newss=newss, title="Home Page")




	#print(JsonNews['items'])
	#print(JsonNews['user'])
			# if current_user.level == '4':
			# 	return render_template('home.html', reports=reports, title="Home Page")
			# elif current_user.level == '5':
			# 	return render_template('home.html', questions=questions, newss=newss, reports=reports, title="Home Page")
			# else:
			# 	return render_template('home.html', questions=questions, newss=newss, title="Home Page")
	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp
	#return flask.jsonify(N)	

	#return JsonNews
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

@app.route("/account/profile_pic", methods=['GET', 'POST'])
@login_required
def account():
	image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
	return redirect(image_file)


#Ignore for right now
@app.route("/account/update", methods=['GET', 'POST'])
@login_required
def account_update():
	#form = UpdateAccountForm()
	data = request.form or request.args
	username = str(data["username"]) or ""
	email = str(data["email"]) or ""

	current_user.username = username
	current_user.email = email
	db.session.commit()
	#image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
	
	return str({"username": username, "email" : email})


	#return render_template('account.html', title="1 Account", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
	
	#form = RegistrationForm()


	try:
		data = request.form or request.args
		username = str(data["username"]) 
		email = str(data["email"]) 
		password = str(data["password"])
		confirmpass = str(data["confirmpass"])
		level = int(data["level"])

	except Exception as e:
		print(e)

		msg = {"staus": "Not enough arguments", "error" : e}
		js = json.dumps(msg)
		resp = Response(js, status=200, mimetype='application/json')
		return resp

		
	# 1) student
	# 2) student tutor
	# 3) staff
	# 4) repairman
	# 5) administrator
	#print({data})
	hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
	user = User(username=username, email=email, password=hashed_password, level=level)
	if user.level == '2':
		user.level = '1'
		user.tutor = True
	else:
		user.tutor = False


		encryptpassword = ""

		for i in password:
			encryptpassword = encryptpassword + "*"

	try:
		db.session.add(user)
		db.session.commit()

		msg = {
			"username" : username,
			"email": email,
			"password": encryptpassword,
			"level": level,
			"status" : "success"
		}


		js = json.dumps(msg)
		resp = Response(js, status=200, mimetype='application/json')
		return resp
		
	except Exception as e:
		print("database error")
		return e
	
	#flash("Account created for {}.".format(form.username.data), 'success')
	
	
		
	
## Do Last
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
	return "logout"


@app.route("/user/<string:username>")
@login_required
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	attached_image = user.image_file
	questions = Question.query.filter_by(user=username).paginate(page=page, per_page=5)
	grades = Grade.query.filter_by(user=username).paginate(page=page, per_page=5)
	#return render_template('user_posts.html', questions=questions, grades=grades, user=user, attached_image=attached_image)
	
	G = grades.__dict__
	


	# print(grade["items"][0].__dict__["assignment"])
	
	bigmsg = {"grades":[], "questions":[], "user": []}
	for x in G["items"]:
		x = x.__dict__
		#print("How many items: ", x)
		detailedmsg = {
			"assignment" : str(x["assignment"]) or " ",
			"course" : str(x["course"]),
			"id" : str(x["id"]),
			"grade" : int(x["grade"]),
			"id" : str(x["id"]) or "",
			"points" : int(x["points"]),
			"total_points" : int(x["total_points"]) or "",
			"date_posted" : str(x["date_posted"]),
			"teacher" : str(x["teacher"]),
			"user_id" : int(x["user_id"])
		
		}
		bigmsg["grades"].append(detailedmsg)

	Q = questions.__dict__

	for x in Q["items"]:
		x = x.__dict__
		#print("How many items: ", x)
		detailedmsg = {
			"id" : str(x["id"]) or "",
			"title" : str(x["title"]) or " ",
			"user" : str(x["user"]),
			"content" : str(x["content"]),
			"reviewedornot" : str(x["reviewedornot"]) or "",
			"date_posted" : str(x["date_posted"]),
			"attached_image" : str(x["attached_image"]) or "",
			"user_id" : str(x["user_id"])
		
		}
		bigmsg["questions"].append(detailedmsg)


	U = user.__dict__

	
	x = U
	#print("How many items: ", x)

	encryptpass = ""
	for i in str(x["password"]):
		encryptpass = encryptpass + "*"

	detailedmsg = {
		"id" : str(x["id"]) or "",
		"username" : str(x["username"]) or " ",
		"email" : str(x["email"]),
		"image_file" : str(x["image_file"]),
		"password" : encryptpass or "",
		"level" : str(x["level"]),
		#"tutor" : str(x["tutor"]) or "",
		"course1" : str(x["course1"]),
		"course2" : str(x["course2"]),
		"course3" : str(x["course3"]),
		"course4" : str(x["course4"]),
		"course5" : str(x["course5"]),
		"course6" : str(x["course6"]),
		"course7" : str(x["course7"]),
		"barcode" : str(x["barcode"])
	
	}
	bigmsg["user"].append(detailedmsg)


	

	# msg = {
	# 	"grades": grades
	# }


	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/news/post", methods=['GET', 'POST'])
@login_required
def news_post(): #num = 0 is a default
	if current_user.level != '5':
		abort(403)
	# form1 = NewsForm() ## Form page 1
	# form2 = NewsClubForm() ## Form page 2


	data = request.form or request.args
	title = str(data["title"])
	destination = str(data["destination"])
	content = str(data["content"])


	try:
		picture = str(data["picture"]) or ""
	except:
		picture = ""

	listofdest = ["Club", "Athletic", "Activity", "Lunch"]
	for i in listofdest:
		if(destination == i):
			break
		

	else:
		destination = "Activity"




	
	if(destination == "Club"):



		clubdict = Club.query.all()
		for c in clubdict:
			x = c.__dict__
			
			if(x == club):
				club = str(data["club"]) or ""
				break
			else:
				club = ""

		
	elif(destination != "Club"):
		club = ""
	
		
	#print(club)	
	#form2.club.choices = [(c.clubname, c.clubname) for c in Club.query.all()]
	###
	# num have three variants, 0, 1, 2.
	# 0 represents first entry
	# 1 represents second entry from post_news.html
	# 2 represents third entry from post_news_clubname.html
	# each number are being called at the action attributes in each html file
	###
	

	if picture != "":
		picture_file = save_picture_for_attachments(picture)
		post = News(title=title, content=content, user=current_user.username, attached_image=picture, newstype= destination, user_id= current_user.id)
		db.session.add(post)
		db.session.commit()


	else:
		post = News(title=title, content=content, user=current_user.username, newstype= destination, user_id= current_user.id)
		db.session.add(post)
		db.session.commit()


	if destination == 'Club':
		memory = Memory(value1=post.id, value2=post.user)
		db.session.add(memory)
		db.session.commit()
		

		memory = Memory.query.filter_by(value2=current_user.username).first()
		post = News.query.filter_by(id=memory.value1).first()
		post.clubname = club
		db.session.delete(memory)
		db.session.commit()

		#return redirect(url_for("home"))

	msg = {

		"title": title,
		"destination": destination,
		"content" : content,
		"picture" : picture or "",
		"club" : club or ""


	}


	js = json.dumps(msg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp


	# elif num == 0: ## First Entry

	# 	return render_template("post_news.html", title="Post Accouncement", form=form1, legend="Post Announcement")
	
	# else: ## First/Error Entry
	# 	print("Error at news posting input num:", str(num))
	# 	return render_template("post_news.html", title="Post Accouncement", form=form1, legend="Post Announcement")
	
@app.route("/view_news", methods=['GET', 'POST'])
@login_required
def view_news():
	page = request.args.get('page', 1, type=int)
	news = News.query.paginate(page=page, per_page=1000)
	
	
	P = news.__dict__
	


	bigmsg = {"News": []}
	for x in P["items"]:
		x = x.__dict__
		#print("How many items: ", x)
		detailedmsg = {
			"title" : str(x["title"]) or " ",
			"user" : str(x["user"]),
			"content" : str(x["content"]),
			"date_posted" : str(x["date_posted"]),
			"attached_image" : str(x["attached_image"]) or "",
			"newstype" : str(x["newstype"]),
			"clubname" : str(x["clubname"]) or "",
			"user_id" : str(x["user_id"])
		
		}
		bigmsg["News"].append(detailedmsg)


	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

	#return render_template("view_news.html", title=post.title, post=post)


@app.route("/view_news/clubs", methods=['GET', 'POST'])
@login_required
def clubnews():
	page = request.args.get('page', 1, type=int)
	news = News.query.filter_by(newstype='Club').paginate(page=page, per_page=5)
	
	P = news.__dict__
	


	bigmsg = {"News": []}
	for x in P["items"]:
		x = x.__dict__
		#print("How many items: ", x)
		detailedmsg = {
			"title" : str(x["title"]) or " ",
			"user" : str(x["user"]),
			"content" : str(x["content"]),
			"date_posted" : str(x["date_posted"]),
			"attached_image" : str(x["attached_image"]) or "",
			"newstype" : str(x["newstype"]),
			"clubname" : str(x["clubname"]) or "",
			"user_id" : str(x["user_id"])
		
		}
		bigmsg["News"].append(detailedmsg)


	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp



	#return render_template('mypueo.html', posts=posts, title="Club News")

@app.route("/view_news/athletic", methods=['GET', 'POST'])
@login_required
def athleticnews():
	page = request.args.get('page', 1, type=int)
	news = News.query.filter_by(newstype='Athletic').paginate(page=page, per_page=5)
	
	P = news.__dict__
	


	bigmsg = {"News": []}
	for x in P["items"]:
		x = x.__dict__
		#print("How many items: ", x)
		detailedmsg = {
			"title" : str(x["title"]) or " ",
			"user" : str(x["user"]),
			"content" : str(x["content"]),
			"date_posted" : str(x["date_posted"]),
			"attached_image" : str(x["attached_image"]) or "",
			"newstype" : str(x["newstype"]),
			"clubname" : str(x["clubname"]) or "",
			"user_id" : str(x["user_id"])
		
		}
		bigmsg["News"].append(detailedmsg)


	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp






	#return render_template('mypueo.html', posts=posts, title="Athletic News")

@app.route("/view_news/activities", methods=['GET', 'POST'])
@login_required
def actvities():
	page = request.args.get('page', 1, type=int)
	news = News.query.filter_by(newstype='Activity').paginate(page=page, per_page=5)
	
	P = news.__dict__
	


	bigmsg = {"News": []}
	for x in P["items"]:
		x = x.__dict__
		#print("How many items: ", x)
		detailedmsg = {
			"title" : str(x["title"]) or " ",
			"user" : str(x["user"]),
			"content" : str(x["content"]),
			"date_posted" : str(x["date_posted"]),
			"attached_image" : str(x["attached_image"]) or "",
			"newstype" : str(x["newstype"]),
			"clubname" : str(x["clubname"]) or "",
			"user_id" : str(x["user_id"])
		
		}
		bigmsg["News"].append(detailedmsg)


	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp


	#return render_template('mypueo.html', posts=posts, title="School News")

@app.route("/view_news/schoollunch", methods=['GET', 'POST'])
@login_required
def schoollunch():
	page = request.args.get('page', 1, type=int)
	news = News.query.filter_by(newstype='Lunch').paginate(page=page, per_page=5)
	
	P = news.__dict__
	


	bigmsg = {"News": []}
	for x in P["items"]:
		x = x.__dict__
		#print("How many items: ", x)
		detailedmsg = {
			"title" : str(x["title"]) or " ",
			"user" : str(x["user"]),
			"content" : str(x["content"]),
			"date_posted" : str(x["date_posted"]),
			"attached_image" : str(x["attached_image"]) or "",
			"newstype" : str(x["newstype"]),
			"clubname" : str(x["clubname"]) or "",
			"user_id" : str(x["user_id"])
		
		}
		bigmsg["News"].append(detailedmsg)


	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp



	#return render_template('mypueo.html', posts=posts, title="Club News")

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
	msg.body = url_for('reset_token', token=token, _external=True)
	mail.send(msg)


@app.route("/report_issue/new", methods=['GET', 'POST'])
@login_required
def report_issue():
	# if current_user.level == '4':
	# 	abort(403)
	#form =ReportIssueForm()
	#if form.validate_on_submit():

	data = request.form or request.args

	destination = str(data["destination"])
	description = str(data["description"])
	picture = str(data["picture"]) or ""





	d = ["furniture","electronic","wifi"]
	for c in d:
		
		print(c)
		if(destination == c):
			destination = str(data["destination"]) + " issue"
			break
	
	else:
		destination = "furniture"
		



	try:
		if picture:
			picture_file = save_picture_for_attachments(picture)
			post = IssueReport(issuetype=destination, content=description, user=current_user.username, user_id=current_user.id, attached_image=picture)
		else:
			post = IssueReport(issuetype=destination, content=description, user=current_user.username, user_id=current_user.id)

		bigmsg = {
			"status": "success",
			"destination" : destination,
			"description" : description,
			"picture" : picture or ""
		}	

		db.session.add(post)
		db.session.commit()
	except Exception as e:
		
		print(e)
		bigmsg = {
			"status": "error",
			"destination" : destination,
			"description" : description,
			"picture" : picture or "",
			"err" : e or ""
		}	
		
	

		
	print("bigmsg",bigmsg)

	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp




	#flash("The issue has been reported. Thank you for your coorperation. ", "success")
	#return redirect(url_for("home"))
	#return render_template("report_issue.html", title="Issue Reporting", form=form, legend="File a Report")

@app.route("/view_report/<int:post_id>", methods=['GET', 'POST'])
@login_required
def view_report(post_id):
	post = IssueReport.query.get_or_404(post_id)
	page = request.args.get('page', 1, type=int)
	
	P = post.__dict__
		
	# print(type(P))
	# return str(P["issuetype"])

	bigmsg = {"Report": []}
	# for x in P:
	# 	x = x.__dict__
	# 	#print("How many items: ", x)

	x = P

	detailedmsg = {
		"issuetype" : str(x["issuetype"]) or " ",
		"user" : str(x["user"]),
		"content" : str(x["content"]),
		"date_posted" : str(x["date_posted"]),
		"attached_image" : str(x["attached_image"]) or "",
		"id" : str(x["id"]),
		"user_id" : str(x["user_id"])
	
	}
	bigmsg["Report"].append(detailedmsg)


	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp




	return render_template("view_report.html", title=post.issuetype, post=post)

@app.route("/view_report/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_report(post_id):
	post = IssueReport.query.get_or_404(post_id)
	if (current_user.level != '5') and (current_user.username != post.user):
		bigmsg = {"status" : "denied", "user_level" : current_user.level}

		js = json.dumps(bigmsg)
		resp = Response(js, status=403, mimetype='application/json')
		return resp
	
	#form = IssueReportForm()
	data = request.form or request.args
	try:
		destination = str(data["destination"]) or ""
	except:
		destination = ""
	try: 
		description = str(data["description"]) or ""
	except:
		description = ""
	try:
		picture = str(data["picture"]) or ""
	except:
		picture = ""

	d = ["furniture","electronic","wifi"]
	for c in d:
		print(c)
		if(destination == c):
			destination = str(data["destination"]) + " issue"
			break
	else:
		destination = "furniture"

	#if form.validate_on_submit():
	try:
		if(destination != ""):
			post.issuetype = destination
		
		if(description != ""):
			post.content = description
		
		if(picture != ""):
			post.attached_image= picture or ""
		

		db.session.commit()

		#return redirect(url_for('view_report', post_id=post.id))
		# elif request.method == 'GET':
		# 	form.title.data = post.issuetype
		# 	form.content.data = post.content
		# 	form.picture.data = post.attached_image


		bigmsg = {
			"status" : "success",
			"destination" : destination,
			"description" : description,
			"picture" : picture or ""
		}

	except Exception as e:
		print(e)
		bigmsg = {
			"status" : "error",
			"error" : str(e),
			"destination" : destination,
			"description" : description,
			"picture" : picture or ""

		}		


	js = json.dumps(bigmsg)
	resp = Response(js, status=403, mimetype='application/json')
	return resp
	#return render_template("update_report.html", image_file = image_file, title="Update Report", form=form, legend="Update Report")

@app.route("/view_report/delete", methods=['GET', 'POST'])
@login_required
def delete_report():
	
	

	data = request.args or request.form or post_id
	post_id = int(data["post_id"]) or ""
	if(post_id == ""):
		bigmsg = {"status" : "error", "details" : "empty id"}

		js = json.dumps(bigmsg)
		resp = Response(js, status=403, mimetype='application/json')
		return resp
	post = IssueReport.query.get_or_404(post_id)
	if (post.user != (current_user)) and (current_user.level !='5'):
		bigmsg = {"status" : "denied", "user_level" : current_user.level}

		js = json.dumps(bigmsg)
		resp = Response(js, status=403, mimetype='application/json')
		return resp
	db.session.delete(post)
	db.session.commit()
	bigmsg = {"status" : "success", "post_id" : post_id}

	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/post_question", methods=['GET', 'POST'])
@login_required
def post_question():
	if current_user.level != ('1' and '5'):
		if(current_user.username != "admin"):
			bigmsg = {"status" : "denied", "user_level" : current_user.level}

			js = json.dumps(bigmsg)
			resp = Response(js, status=403, mimetype='application/json')
			return resp

	#form = QuestionForm()
	data = request.args or request.form
	title = str(data["title"])
	content = str(data["content"])
	picture = str(data["picture"]) or ""



	#if form.validate_on_submit():
	try:

		if picture:
			picture_file = save_picture_for_attachments(picture)
			post = Question(title=title, content=content, user=current_user.username, user_id=current_user.id, attached_image=picture_file, quirk=secrets.token_hex(8))
		else:
			post = Question(title=title, content=content, user=current_user.username, user_id=current_user.id, quirk=secrets.token_hex(8))
		
		db.session.add(post)
		db.session.commit()
		bigmsg = {
			"title": title,
			"content" : content,
			"picture" : picture or "",
			"status" : "success"
		}
	except Exception as e:
		print(e)
		bigmsg = {
			"title": title,
			"content" : content,
			"picture" : picture or "",
			"status" : "error"
		}


	js = json.dumps(bigmsg)
	resp = Response(js, status=403, mimetype='application/json')
	return resp
	#flash("your question has been posted", "success")
		##return redirect(url_for("home"))
	#return render_template("post_question.html", title="Study Buddies", form=form, legend="Ask a Question")

@app.route("/view_question", methods=['GET', 'POST'])
@login_required
def view_question():

	data = request.args or request.form
	post_id = str(data["post_id"])
	# title = str(data["title"])
	# content = str(data["content"]) or ""


	post = Question.query.get_or_404(post_id)
	page = request.args.get('page', 1, type=int)
	comments = Comment.query.filter_by(reference=post.quirk).paginate(page=page, per_page=5)
	
	user_level = current_user.level
	#form = AnswerForm()
	bigmsg = {
		"post_id": post_id,
		"status" : "success"
	}
	if (current_user.level == ('4' or '5')) or current_user.tutor == True:
		
		bigmsg["permission"] = bool(True)

		#return render_template("studypost.html", title=post.title, user_level=user_level, post=post, comments=comments)
	#else:
		#if form.validate_on_submit():
		#comment = Comment(commenter=current_user.username, comment=content, commenttitle=title, reference=post.quirk)
		#db.session.add(comment)
		#db.session.commit()
		#post.reviewedornot = True
		#db.session.commit()
	print(post.__dict__)
	x = post.__dict__

	
	
	#print("How many items: ", x)
	detailedmsg = {
		"id" : str(x["id"]) or "",
		"title" : str(x["title"]) or " ",
		"user" : str(x["user"]),
		"content" : str(x["content"]),
		"reviewedornot" : str(x["reviewedornot"]) or "",
		"date_posted" : str(x["date_posted"]),
		"attached_image" : str(x["attached_image"]) or "",
		"user_id" : str(x["user_id"])
	
	}
	
	bigmsg = detailedmsg


	

	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp
		#return redirect(url_for("home", post_id=post.id))
	#return render_template("view_question.html", title=post.title, form = form, user_level=user_level, post=post, comments=comments, legend="Add your comment here")

@app.route("/view_question/delete", methods=['GET', 'POST'])
@login_required
def delete_question():
	data = request.args or request.form 
	post_id = int(data["post_id"]) or ""

	if(post_id == ""):

		bigmsg = {
		"post_id": post_id,
		"status" : "error"
		}

		js = json.dumps(bigmsg)
		resp = Response(js, status=403, mimetype='application/json')
		return resp

	post = Question.query.get_or_404(post_id)
	if (post.user != (current_user.username)) and (current_user.level !='5'):
		bigmsg = {
		"current_level": current_user.level,
		"current_user" : current_user.username,
		"status" : "denied"
		}

		js = json.dumps(bigmsg)
		resp = Response(js, status=403, mimetype='application/json')
		return resp
		#abort(403)
	db.session.delete(post)
	db.session.commit()
	bigmsg = {
		"post_id": post_id,
		"details": "deleted",
		"status" : "success"
	}

	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp
	#return redirect(url_for("home"))

@app.route("/post_grade/getCourses", methods=['GET', 'POST'])
@login_required
def getCourses():
	choices = [(c.coursename) for c in Course.query.filter_by(teacher=current_user.username).all()]
	
	js = json.dumps(choices)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/post_grade", methods=['GET', 'POST'])
@login_required
def post_grade():
	if current_user.level != ('3' and '5'):
		if(current_user.username != "admin"):
			bigmsg = {"status" : "denied", "user_level" : current_user.level}

			js = json.dumps(bigmsg)
			resp = Response(js, status=403, mimetype='application/json')
			return resp
	#form1 = GradeForm()
	#form2 = GradeCourseForm()

	data = request.args or request.form
	assignment = str(data["assignment"])
	student = str(data["student"])
	grade = float(data["grade"])
	total_points = float(data["total_points"])
	course = str(data["course"])




	choices = [(c.coursename) for c in Course.query.filter_by(teacher=current_user.username).all()]
	
	if(course not in choices):
		print(choices[0].coursename)
		print(course)
		return "Not Listed"
	else:
		course = str(course)

	try:	
		#if num == 1:
		memory = Memory(value1 = course, value2=current_user.username)
		db.session.add(memory)
		db.session.commit()
		students = User.query.filter_by(course1 = course).all()+User.query.filter_by(course2 = course).all()+User.query.filter_by(course3 = course).all()+User.query.filter_by(course4 = course).all() + User.query.filter_by(course5 = course).all() + User.query.filter_by(course6 = course).all() + User.query.filter_by(course7 = course).all()
		student_choices=[(c.username, c.username) for c in students]
		#return render_template("post_grade.html", title="Grade Posting", form=form1, legend="Post a Grade")

		memory = Memory.query.filter_by(value2=current_user.username).first()
		students = User.query.filter_by(course1 = memory.value1).all()+User.query.filter_by(course2 = memory.value1).all()+User.query.filter_by(course3 = memory.value1).all()+User.query.filter_by(course4 = memory.value1).all() + User.query.filter_by(course5 = memory.value1).all() + User.query.filter_by(course6 = memory.value1).all() + User.query.filter_by(course7 = memory.value1).all()
		#student_choices =[(c.username, c.username) for c in students]
		
		#if form1.validate_on_submit:
		post = Grade(assignment=assignment, grade=float(grade), points=(float(grade)*float(total_points)/100), total_points=float(total_points), user=student, teacher=current_user.username, course = memory.value1, user_id=current_user.id)
		db.session.add(post)
		db.session.delete(memory)
		db.session.commit()
		bigmsg = {
			
			"student" : student,
			"grade" : grade,
			"total_points" : total_points,
			"course" : course,
			"status" : "success"
		}


	except Exception as e:
		print(e)
		bigmsg = {
		 "status" : "error",
		 "error" : str(e)
		}

	

	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp	



	#flash("The grade has been posted. ", "success")
	#return redirect(url_for("home"))
	
	#elif num == 0:
		#return render_template("post_grade_course.html", title="Grade Posting", form=form2, legend="Post a Grade")
	#else: ## First/Error Entry
		#print("Error at news posting input num:", str(num))
		#return render_template("post_grade_course.html", title="Post Accouncement", form=form2, legend="Post a Grade")


# @app.route("/view_grade/<int:post_id>", methods=['GET', 'POST'])
# @login_required
# def view_grade(post_id):
# 	post = Grade.query.get_or_404(post_id)
# 	if ((post.user != current_user.username)) or (current_user.level != "5" and current_user.level != "3"):
		
# 		abort(403)

# 	page = request.args.get('page', 1, type=int)
# 	attached_image = current_user.image_file

# 	#return render_template("view_grade.html", title=post.user, post=post, attached_image=attached_image)
# 	msg = {
# 		"user" : post.user,
# 		"grade_post" : post,
# 		"attached_image" : attached_image
# 	}
# 	js = json.dumps(msg)
# 	resp = Response(js, status=200, mimetype='application/json')
# 	return resp


@app.route('/view_grade/<int:post_id>',methods=['GET', 'POST'])
@login_required
def view_grade(post_id):
	post = Grade.query.get_or_404(post_id)
	if ((post.user != current_user.username)) or (current_user.level != "5" and current_user.level != "3" and current_user.level != "6"):
		bigmsg = {"status" : "denied", "user_level" : current_user.level ,"reason" : "user " + current_user.username+" is not posted user"}
		print(post.user)
		js = json.dumps(bigmsg)
		resp = Response(js, status=403, mimetype='application/json')
		return resp		
		
	assignment = post.assignment
	student = post.user
	grade = post.grade
	total_points = post.total_points

	bigmsg = {
		"assignment" : assignment,
		"student" : student,
		"grade" : grade,
		"total_points" : total_points
	}
	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/view_grade/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_grade(post_id):
	post = Grade.query.get_or_404(post_id)
	if (post.user != (current_user.username)) and (current_user.level !='5' or current_user.level != '6'):

		if(current_user.username == "admin"):

			print("admin access")
		
		else:

			bigmsg = {"status" : "denied", "user_level" : current_user.level ,"reason" : "user " + current_user.username+" is not posted user"}

			js = json.dumps(bigmsg)
			resp = Response(js, status=403, mimetype='application/json')
			return resp
	

	#print(current_user)
	#form = GradeForm()
		
	data = request.args or request.form
	assignment = str(data["assignment"]) or post.assignment
	student = str(data["student"]) or post.user
	grade = int(data["grade"]) or post.grade
	total_points = int(data["total_points"]) or post.total_points



	students = User.query.filter_by(course1 = post.course).all()+User.query.filter_by(course2 = post.course).all()+User.query.filter_by(course3 = post.course).all()+User.query.filter_by(course4 = post.course).all() + User.query.filter_by(course5 = post.course).all() + User.query.filter_by(course6 = post.course).all() + User.query.filter_by(course7 = post.course).all()
	print(post)

	for i in students:
		#print(i)
		if(i.username == student):
			print("user found: ",i)
			student = str(student)
			break
		


	else:

		bigmsg = {"status" : "denied", "user" : current_user.username ,"reason" : "user " + current_user.username+" not found"}

		js = json.dumps(bigmsg)
		resp = Response(js, status=403, mimetype='application/json')
		return resp
		#return "no user found"

		
	#form.student.choices = [(c.username, c.username) for c in students]
	#if form.validate_on_submit():
	post.assignment = assignment
	post.user = student
	post.grade = grade
	post.total_points = total_points

	print(post)

	#return ""
	db.session.commit()
	#return redirect(url_for('view_grade', post_id=post.id))
	#elif request.method == 'GET':
		# form.assignment.data = post.assignment
		# form.student.data = post.user
		# form.grade.data = post.grade
		# form.total_points.data = post.total_points
	
	bigmsg = {
		"assignment" : assignment,
		"student" : student,
		"grade" : grade,
		"total_points" : total_points,
		"status" : "success"
	}

	js = json.dumps(bigmsg)
	resp = Response(js, status=200, mimetype='application/json')
	return resp


	#return render_template("update_grade.html", title="Update Grade", form=form, legend="Update Grade")

@app.route("/view_grade/delete", methods=['GET', 'POST'])
@login_required
def delete_grade():
	data = request.args or request.form
	post_id = str(data["post_id"]) or ""
	if(post_id == ""):
		bigmsg = {"status" : "error", "details" : "invalid post_id"}
		js = json.dumps(bigmsg)
		resp = Response(js, status=403, mimetype='application/json')
		return resp

	post = Grade.query.get_or_404(post_id)
	if (post.user != (current_user.username)) and (current_user.level !='5'):
		
		if (current_user.username != "admin"):
			bigmsg = {"status" : "error", "details" : "not admin"}
			js = json.dumps(bigmsg)
			resp = Response(js, status=403, mimetype='application/json')
			return resp

	db.session.delete(post)
	db.session.commit()
	bigmsg = {"status" : "success", "post_id" : post_id}
	js = json.dumps(bigmsg)
	resp = Response(js, status=202, mimetype='application/json')
	return resp
	#return redirect(url_for("home"))

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

@app.route("/create_club", methods=['GET', 'POST'])
@login_required
def create_club():
	if current_user.level != '5':
		if(current_user.username != "admin"):
			bigmsg = {"status" : "error", "details" : "not admin"}
			js = json.dumps(bigmsg)
			resp = Response(js, status=403, mimetype='application/json')
			return resp
	
	#form = ClubForm()
	#if form.validate_on_submit():

	data = request.args or request.form
	clubname = str(data["clubname"]) or ""
	if(clubname == ""):
		bigmsg = {"status" : "error", "details" : "invalid clubname"}
		js = json.dumps(bigmsg)
		resp = Response(js, status=403, mimetype='application/json')
		return resp


	post = Club(clubname=clubname)
	db.session.add(post)
	db.session.commit()

	bigmsg = {"status" : "success", "clubname" : clubname}
	js = json.dumps(bigmsg)
	resp = Response(js, status=202, mimetype='application/json')
	return resp
		#flash("your club has been posted", "success")
		#return redirect(url_for("home"))
	#return render_template("create_club.html", title="Create Club", form=form, legend="Create a Club")

@app.route("/create_course", methods=['GET', 'POST'])
@login_required
def create_course():
	if current_user.level != '5' and '3':
		if(current_user.username != "admin"):
			bigmsg = {"status" : "error", "details" : "not admin"}
			js = json.dumps(bigmsg)
			resp = Response(js, status=403, mimetype='application/json')
			return resp

	#form = CourseForm()
	data = request.args or request.form
	coursename = str(data["coursename"])
	
	period = int(data["period"])
	

	if(period > 7 and period < 1):
		bigmsg = {"status" : "error", "details" : "period invalid"}
		js = json.dumps(bigmsg)
		resp = Response(js, status=403, mimetype='application/json')
		return resp


	choices = [(c.username) for c in User.query.filter_by(level='1').all()]
	students = choices
	print(students)
	# if(students not in choices):
	# 	bigmsg = {"status" : "error", "details" : "student invalid"}
	# 	js = json.dumps(bigmsg)
	# 	resp = Response(js, status=403, mimetype='application/json')
	# 	return resp

	#if form.validate_on_submit():
	post = Course(coursename=coursename, students=repr(students), teacher = current_user.username, period = period)
	db.session.add(post)

	for i in students:
		s = User.query.filter_by(username = i).first()
		period = str(period)
		if period == '1':
			s.course1=post.id
		elif period == '2':
			s.course2=post.id
		elif period == '3':
			s.course3=post.id
		elif period == '4':
			s.course4=post.id
		elif period == '5':
			s.course5=post.id
		elif period == '6':
			s.course6=post.id
		elif period == '7':
			s.course7=post.id
		else:
			s.course1 = post.id
		db.session.commit()

	bigmsg = {"status" : "success", "coursename" : coursename, "students" : students, "period" : period}
	js = json.dumps(bigmsg)
	resp = Response(js, status=202, mimetype='application/json')
	return resp 
		#flash("your club has been posted", "success")
		#return redirect(url_for("home"))
	#return render_template("create_course.html", title="Create Club", form=form, legend="Create a Club")

@app.route("/user/schedule", methods=["GET","POST"])
@login_required
def user_schedule():
	data = request.args or request.form
	username = str(data["username"])
	#print(username)
	user = User.query.filter_by(username = str(username)).first()
	#print(user.__dict__)
	#print(current_user.course1)
	
	courses = Course.query.all()
	print(courses)
	course = {"period_1": "Free", "period_2" : "Free", "period_3" : "Free", "period_4" : "Free", "period_5" : "Free", "period_6" : "Free", "period_7": "Free"}
	for i in courses:
		if(user.course1 == i.id):
			course["period_1"] = i.coursename

		elif(user.course2 == i.id):
			course["period_2"] = i.coursename

		elif(user.course3 == i.id):
			course["period_3"] = i.coursename

		elif(user.course4 == i.id):
			course["period_4"] = i.coursename

		elif(user.course5 == i.id):
			course["period_5"] = i.coursename

		elif(user.course6 == i.id):
			course["period_6"] = i.coursename

		elif(user.course7 == i.id):
			course["period_7"] = i.coursename
	



	print(course)


	bigmsg = course
	js = json.dumps(bigmsg)
	resp = Response(js, status=202, mimetype='application/json')
	return resp 
######BACK-END SESSION REPORT#######

###Overall:
	*Need more documentations of every single route and functions, also include package/module used
	and global range variables(indicate their specific type)
	*Please indicate specific instructions for installing needed applications or modules in your documentations too.
	*Remember to comment on tangled lines that involves with specific module syntaxes for easier imports in the future and easier for connections front~back.
	*Currently we are not making a website, but an web based server sided scripts for data transfer between front-end(swift) and database(in this case SQLAchemy/SQLite), so please do not include render template in your code.
	*I like the idea of hashing your password before putting in to database.
	*Delete weird pictures to save space.




#Important prioritized bugs/issues:
	*Page does not load sometimes and you would need to press enter key in the command prompt in order to allow it run. This can cause some serious issues in the AWS server CLI, check if there is a better way to resolve this than pressing enter key.
	*Please include sessions for user logins. Check Flask official documentations for details.
	*Page number does not work for posts.
	*[routes.py Line 140]: Delete posts bugs, typing /post/1/delete will cause 403 forbidden errors and typing /post/0/delete will cause 404 error. make an validator that cannot allow users to type 0 in the post_id variable. Even if I changed my level to 5 it still displays a 403 no permission error.
	*HTTP 500 Internal server error occurs when updating posts: 
		- sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) database is locked
		- See report.png for detailed screenshot.
	*Some SQL errors please see report.sql file



##Detailed each individual page reports:
======================================================
#Run.py:
	*Does not include debug mode on sometimes?
	*App.run() can also indicate your ports, set your port to 8000(default)


#__init__.py:
	*[Line 1]: Command Prompt import os error until installed SQLAchemy, please check why needed os here and specify it in your documentations.
	*[Line 2 ~ 6]: Please specify which extentions of flask you have used in your documentation.
	*[Line 9]: Please do not set a fixed secret key, check this for more details: [Official Page](http://flask.pocoo.org/docs/1.0/quickstart/#sessions) 
	*[Line 12 ~ 13]: Please specify useage of these two objects/variables.
	*[Line 21]: mail = Mail(app)?

#models.py:
	*[Line 6]: Login Manager user loader functions within the cookies section, with more XSS you can change the cookies in one logged in computer to another not logged in computer and get access through the login system without actually typing username or password. Also as well as this does not correspond to the future swift front-end patch. see #Overall for more details.
	*[Line 15]: Image_file default.jpg not found in your directory.
	*[Line 21 ~ 22]: Please explain in documentations, if useless then please delete, it might cause memory corruptions.
	*In most of your codes you have db.something, since you are using SQLAchemy/SQLite them please specify each lines' functionality in SQL language or human readable language.
	*[Line 33]: def __repr__ ?

#forms.py:
	*Please write documentations for each class and their properties.
	

#routes.py:
	*[Line 11 ~ 13]: Please specify usage
	*[Line 19 ~ 28]: Why would you need a random generated name for a picture? Using user's name plus a number would work better in this case, such as Hitoki_Image_001 and Hitoki_Image_002
	*[Line 30 ~ 39]: Same description as above.
	*[Line 50]: Default user image is nothing? How about change it to a default picture like this: (https://banner2.kisspng.com/20180410/bbw/kisspng-avatar-user-medicine-surgery-patient-avatar-5acc9f7a7cb983.0104600115233596105109.jpg)
	*[Line 74]: Samething, do not use any webpage syntaxes such as render_template or flash, just use return datas since we are not making a webstite but a mobile application using SWIFT
	*[Line 122 ~ 123]: why if post.student not equals to current user ends up in abort 403? If you are going to abort it for whatever reason then add a break or reuturn "" there, even with abort 403 the script will still continue to execute, but with a break or return "" then the script will actually stop continue running on that function.
	*[Line 134 ~ 135]: I do not see any grades or assignments on the home.html page, but instead I only see descriptions and titles. Change your variable name according to what its role here.
	*[Line 140]: Delete posts bugs, typing /post/1/delete will cause 403 forbidden errors and typing /post/0/delete will cause 404 error. make an validator that cannot allow users to type 0 in the post_id variable. Even if I changed my level to 5 it still displays a 403 no permission error.
	*[Line 156 ~ 160]: send reset email is a void function that doesn't return any variable, please check if thats intended.


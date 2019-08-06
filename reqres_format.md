###Back/Front I/O Formats

##Output:
Json formatted 

Sucess HTTP response 200
{
	"Inputed variable name 1” : "Inputed variable 1 value",
	"Inputed variable name 2" : "Inputed variable 2 value",
	"Message" : True
}

Rejected HTTP response 200
{
	"Inputed variable name 1” : "Inputed variable 1 value",
	"Inputed variable name 2" : "Inputed variable 2 value",
	"Message": False
}

Failed HTTP response 400 or any other error
{
	"Error" : Error type & error message,
	"Message" : False

}


##Input
/.
/home
/report
/account
/register
/login
/logout
/post/new
/post/<int:post_id>
/post/<int:post_id>/update
/post/<int:post_id>/delete
/user/<string:username>
/studybuddies/post
/studybuddies
/mypueo/post
/mypueo
/mypueo/clubnews
/mypueo/athleticnews
/mypueo/Activities
/mypueo/schoollunch
/injury/post
/injury
/absense
/reset_password
/reset_password/<token>



/account/update

/user/<string:username>
/news/post/<int:num>
/view_news/<int:post_id>
/view_news/clubs
/view_news/athletics
/view_news/schoollunch
/report_issue/new
/view_report/<int:post_id>
/view_report/<int:post_id>/update
/view_report/<int:post_id>/delete
/post_question
/view_question/<int:post_id>
/view_question/<int:post_id>/delete
/post_grade
/view_grade/<int:post_id>
/view_grade/<int:post_id>/delete
/view_grade/<int:post_id>/update


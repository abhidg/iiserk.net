#	Copyright (C) 2008 Sambit Bikas Pal, IISERK
#	Author: Sambit Bikas Pal , Email: sam@botcyb.org , sambit@iiserkol.ac.in
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
__author__ = 'Sambit Bikas Pal'

import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import images
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app


class User(db.Model):						# Class to store details of individuals in the DB
	username = db.StringProperty()				# Currently saved details alongwith datatypes:
	userhtml = db.TextProperty()				# String username,fullname
	usercss = db.TextProperty()				# Text page-html, css
	userfullname = db.StringProperty()			# String major, year, batch
	usermajor = db.StringProperty()				# Email email
	userbatch = db.StringProperty()				# Link orkut, web, blog
	useryear = db.StringProperty()				# Text about
	userabout = db.TextProperty()				# PhNo. PhNo.
	useremail = db.EmailProperty()				# Blob Image
	userblog = db.LinkProperty()
	userweb = db.LinkProperty()
	userorkut = db.LinkProperty()
	userphone = db.PhoneNumberProperty()
	useravatar = db.BlobProperty()

	
class StudentsList(webapp.RequestHandler):
	def get(self):
		allusers = db.GqlQuery("SELECT * FROM User ORDER BY username")
		self.response.out.write("""
					<html>
					<head>
					<link rel="stylesheet" href="/static/iiser1.css" type="text/css" />
					</head>
					<body>
						<h2>Welcome</h2>
						<p>Currently we have the following users' profiles:</p>
					""")
		self.response.out.write("<ul>")
		for user in allusers:
			self.response.out.write("""<li>
						<a href='/~""" + user.username + """'>""" + user.userfullname + "</a>" + """ (<span class="nick">""" + user.username + """</span>)</li>
						""")
		self.response.out.write("""</ul>
					<p>You can email any of the users by adding @iiserk.net after the username or by mailing
					the user at his/her preferred email ID on the profile page.</p>
					<p><a href='"""+users.create_login_url("/adduser0")+"""'>Add</a> user's page.</p>
					<p><a href='"""+users.create_login_url("/useredit")+"""'>Edit</a> user's page.</p>
					<p><a href='"""+users.create_login_url("/adminedit0")+"""'>Admins'</a>page.</p>
					</body></html>
					""")

class UserPage(webapp.RequestHandler):				#Serves out cuser homepage, $cuser is fetched from the requested url
	def get(self,cuser):
		flag = 0					#flag is made 1 if requested user is in the DB
		users = db.GqlQuery("SELECT * FROM User")	#GQL query is made to fetch user list, this has to be improved
								#to access entries by keys
		for user in users:
			if user.username == cuser:		#if the requested user is found in the DB, take out the users page and
				cuserhtml=user.userhtml		#							mark flag 1
				cusercss =user.usercss
				flag = 1
 		if flag == 0:					#if user doesn't exist, spew an error else serve the requested page
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write("The user is not in the DBase, try searching hell.")

		else:
			self.response.headers['Content-Type'] = 'text/html'
			self.response.out.write(cuserhtml)



class ImageSpew(webapp.RequestHandler):
	def get(self,cuser):
		users = db.GqlQuery("SELECT * FROM User")	#GQL query is made to fetch user list, this has to be improved
								#to access entries by keys
		for user in users:
			if user.username == cuser:		#if the requested user is found in the DB, spew out the user's image
				if user.useravatar != None:
					self.response.headers['Content-Type'] = 'image/png'
					self.response.out.write(user.useravatar)
				else :
					self.redirect("/static/none.png")

class CssSpew(webapp.RequestHandler):
	def get(self,cuser):
		users = db.GqlQuery("SELECT * FROM User")	#GQL query is made to fetch user list, this has to be improved
								#to access entries by keys
		for user in users:
			if user.username == cuser:		#if the requested user is found in the DB, spew out the user's image
				self.response.headers['Content-Type'] = 'text/css'
				self.response.out.write(user.usercss)


class UserAddStep0(webapp.RequestHandler):			#
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write("""
					<html>
					<head>
					<link rel="stylesheet" href="/static/iiser1.css" type="text/css" />
					</head>
					<body>
						<div><h1>Webpage creator for new user</h1></div>
						<div><h3>If you are not a student of IISER Kolkata, then no need to proceed further</h3></div>
						<div>
						<h3>If you are a student of IISERK</h3>
						<p>Welcome, this page will guide you through the process of creating you own webpage in
						a few minutes</p>
						<div>
							<p> Kindly select the correct choice :</p>	
							<form name="userac" action="/adduser1" method="post">
								iiserk.net account:
								<select name="account">
								<option>Select the correct one</option>
								<option>I have an iiserk.net account</option>
								<option>I do not have one</option>
								</select>
								<input type="submit" value="Submit">
							</form>
						</div>
						</div>
					</body>
					</html>
					""")

class UserAddStep1(webapp.RequestHandler):
	def post(self):
		acstatus = self.request.get('account')
		if acstatus == "I have an iiserk.net account":
					self.response.headers['Content-Type'] = 'text/html'
					self.response.out.write("""
								<html>
								<head>
					<link rel="stylesheet" href="/static/iiser1.css" type="text/css" />
								</head>
								<body>
									<div><h3>Great, so you already have a iiserk.net account.</h3></div>
									<div><p>You can now proceed to the Login page for your iiserk.net account</p>
										<p>Click <a href='""" + users.create_login_url("/adduser2") + """'>here</a>.
									</div>
								</body>
								<html>
								""")
		if acstatus == "I do not have one":
					self.response.headers['Content-Type'] = 'text/html'
					self.response.out.write("""
								<html>
								<head>
					<link rel="stylesheet" href="/static/iiser1.css" type="text/css" />
								</head>
								<body>
									<div><h3>Sorry, but you need to have a iiserk.net account.</h3></div>
									<div><p>Sorry for the inconvenience, but this step is to ensure that non-iisereans don't create their webpages here.</p>
										<p>Click <a href="/adduser3">here to request the admin to create an account for you.</a>.
									</div>
								</body>
								<html>
								""")


class UserAddStep2(webapp.RequestHandler):			# Login required for this
	def get(self):
		flag = 0;
		loggedin = users.get_current_user()
		allusers = db.GqlQuery("SELECT * FROM User ORDER BY username")
		self.response.out.write("""
					<html>
					<head>
					<link rel="stylesheet" href="/static/iiser1.css" type="text/css" />
					</head>
					<body>
						<h2>Welcome """ + loggedin.nickname() + """</h2>
						<h3>Let's get started.</h3>
						<p>Currently we have the following users in the DBase:</p>
					""")
		for user in allusers:
			if loggedin.nickname() == user.username:
				flag=1
			self.response.out.write('<b>%s</b><br/>' % user.username)

		if flag ==0:
			self.response.out.write("""
							<p>Kindly fill out the following form, if you want the html to be generated automatically for you.</p>
							<p>
							<form name="userinput" action="/adduser5" enctype="multipart/form-data" method="post">
							<div>Fullname:<input type="text" name="formuserfullname"></div>
							<div>Email:<input type="text" name="formuseremail"></div>
							<div>
							Major:
							<select name="formusermajor">
							<option>Biology</option>
							<option>Chemistry</option>
							<option>Mathematics</option>
							<option>Physics</option>
							</select>
							</div>
							<div>
							Year:
							<select name="formuseryear">
							<option>1st</option>
							<option>2nd</option>
							<option>3rd</option>
							<option>4th</option>
							<option>5th</option>
							</select>
							</div>
							<div>Batch:
							<select name="formuserbatch">
							<option>2006-2011</option>
							<option>2007-2012</option>
							<option>2008-2013</option>
							<option>2009-2014</option>
							<option>2010-2015</option>
							</select>
							</div>
							<div>AboutMe:<br/><textarea name="formuserabout" rows="10" cols="70" wrap="off"/></textarea></div>
							<div>Image:<input type="file" name="formuserimg"/><i>Upload a png image.</i></div>
							<div><i>Kindly provide full link (including http://) for the following, e.g. http://www.example.com</i></div>
							<div>Blog:<input type="text" name="formuserblog"/></div>
							<div>Personal Website:<input type="text" name="formuserweb"/></div>
							<div>Orkut Profile:<input type="text" name="formuserorkut"/></div>
							<div>Phone:<input type="text" name="formuserphn"/></div>
							<div>HTML:<i>Either fill this properly or leave it blank, don't botch it up unnecessarily.</i><br/>
							<textarea name="formuserhtml" rows="10" cols="70" wrap="off"/></textarea></div>
							<div>CSS:<i>Either fill this properly or leave it blank, don't botch it up unnecessarily.</i><br/>
							<textarea name="formusercss" rows="10" cols="70" wrap="off"/></textarea></div>
							<div><input type="submit" value="Submit"/></div>
							</form>
							
						</body>
						</html>
						""")
		else:
			self.response.out.write("""
						<p>Your name seems to be there in the DBase.</p>
						<p>If you want to edit your page then click this <a href="/useredit">link</a>.</p>
						""")
	
class UserAddStep3(webapp.RequestHandler):			#No login needed, a/c creation, passwd reset request
	def get(self):
		self.response.headers['Content-type'] = 'text/plain'
		self.response.out.write("Not yet implemented.")

class UserAddStep5(webapp.RequestHandler):			#Login needed, HTML generation from submitted form
	def post(self):
		loggedin = users.get_current_user()
		htmlhead="""
			<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
			<html xmlns="http://www.w3.org/1999/xhtml">
			<head>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
			<meta name="generator" content="HTML Tidy for Linux (vers 1 September 2005), see www.w3.org" />
			<meta content='Personal website of """ + self.request.get('formuserfullname') + """.' name='description'/>
			<meta content='"""+ self.request.get('formuserfullname') +""","""+ loggedin.nickname() +""",iiser,
			iiserk, iiserkol, iiserkolkata, """+ self.request.get('formusermajor') +"""' name='keywords'/>
			<title>"""+self.request.get('formuserfullname')+"""</title>
			<link rel="stylesheet" href='/css/"""+ loggedin.nickname() +"""' type="text/css" />
			</head>"""
			
		htmlbody1="""
			<body>
			<h1>"""+ self.request.get('formuserfullname') +"""</h1>
			<div id="designation">
			<h3>iiser kolkata</h3>

			<p>student &raquo; """+ self.request.get('formusermajor') +""" major, MS """+ self.request.get('formuseryear') +""" Year<br />
			batch &raquo; """+self.request.get('formuserbatch')+"""<br /></p>
			</div>
			<div id="sidephoto"><img src='/img/"""+ loggedin.nickname() +"""' alt='"""+ self.request.get('formuserfullname') +"""' width="250" /></div>
			"""
			
		about="""
			<div id="about">
			<ul><pre>""" + self.request.get('formuserabout') + """</pre></ul>
			</div>
			"""
		contact_top="""
			<div id="contact">
			<h3>contact</h3>
			<p>
			"""
		contact_lines =""
		if (self.request.get('formuseremail')) != "":
			contact_lines += """email: <a href='mailto:""" +(self.request.get('formuseremail'))+ """'>"""+ (self.request.get('formuseremail')) +"""</a><br />"""
		if (self.request.get('formuserweb')) != "":
			contact_lines += """website: <a href='""" +(self.request.get('formuserweb'))+ """'>"""+ (self.request.get('formuserweb')) +"""</a><br />"""
		if (self.request.get('formuserblog')) != "":
			contact_lines += """blog: <a href='""" +self.request.get('formuserblog')+ """'>"""+ self.request.get('formuserblog') +"""</a><br />"""
		if (self.request.get('formuserorkut')) != "":
			contact_lines += """orkut: <a href='""" +(self.request.get('formuserorkut'))+ """'>Profile</a><br />"""
		contact_bottom="""
			</p>
			</div>
			"""
		contact = contact_top + contact_lines + contact_bottom	
			
		htmlbody2="""
			</body>
			</html>
			"""
		if self.request.get('formuserhtml') != "":
			htmlcode = self.request.get('formuserhtml')
		else:
			htmlcode = htmlhead + htmlbody1 + about + contact + htmlbody2
		if self.request.get('formusercss') !="":
			csscode = self.request.get('formusercss')
		else:
			csscode="""
				body {
				width: 720px; margin:auto;
				background-color:transparent; padding: 10px;
				font-family : Arial, Helvetica, sans-serif;
				color : #333333;
				}

				#designation {
				width : auto;
				font : 85% "Trebuchet MS", Arial, Helvetica, sans-serif;
				color : grey;
				}

				#designation h3 {
				font : 170% arial;
				color : gold;
				text-transform : lowercase;
				margin : 0;
				padding : 0 0 0 0px;
				}

				#sidephoto {
				float : left;
				width : 300px;
				padding : 5px;
				}

				#about {
				font : 90% Arial, Helvetica, sans-serif;
				float : right;
				width : 400px;
				height : 500px;
				padding : 5px;
				}

				#contact {
				float : left;
				width : auto;
				padding : 5px;
				font : 85% "Trebuchet MS", Arial, Helvetica, sans-serif;
				color : grey;
				}
				"""
		checkflag = 0	
		allusers = db.GqlQuery("SELECT * FROM User ORDER BY username")
		for user in allusers:
			if loggedin.nickname() == user.username:
				checkflag=1
		if checkflag==0:
			newuser = User()
			newuser.username = loggedin.nickname()
			newuser.userhtml = htmlcode
			newuser.usercss = csscode
			newuser.userfullname = (self.request.get('formuserfullname'))
			newuser.usermajor = (self.request.get('formusermajor'))
			newuser.userbatch = (self.request.get('formuserbatch'))
			newuser.useryear = (self.request.get('formuseryear'))
			newuser.userabout = (self.request.get('formuserabout'))
			if (self.request.get('formuseremail')) != "":
				newuser.useremail = (self.request.get('formuseremail'))
			if (self.request.get('formuserblog')) != "":
				newuser.userblog = (self.request.get('formuserblog'))
			if (self.request.get('formuserweb')) != "":
				newuser.userweb = (self.request.get('formuserweb'))
			if (self.request.get('formuserorkut')) != "":
				newuser.userorkut = (self.request.get('formuserorkut'))
			if (self.request.get('formuserphn')) != "":
				newuser.userphone = self.request.get('formuserphn')
			if (self.request.get('formuserimg')) != "":
				avatar = images.im_feeling_lucky(self.request.get("formuserimg"))
				newuser.useravatar = db.Blob(avatar)
			newuser.put()

		self.redirect("""/~""" + loggedin.nickname())


class UserEditing(webapp.RequestHandler):			# Login required for this
	def get(self):
		loggedin = users.get_current_user()
		flag =0
		if loggedin:
			greeting = ("Welcome, %s! Not %s? (<a href=\"%s\">sign out</a> and login back.)" %(loggedin.nickname(), loggedin.nickname(), users.create_logout_url("/useredit")))
		else:
			greeting = ("<a href=\"%s\">Sign in</a>." % users.create_login_url("/useredit"))

		allusers = db.GqlQuery("SELECT * FROM User ORDER BY username")
		for user in allusers:
			if loggedin.nickname() == user.username:
				flag =1
				if user.userfullname != None:
					fullname = user.userfullname
				else:
					fullname =""
				if user.useremail != None:
					email = user.useremail
				else:
					email =""
				if user.usermajor != None:
					major = user.usermajor
				else:
					major =""
				if user.useryear != None:
					year = user.useryear
				else:
					year =""
				if user.userbatch != None:
					batch = user.userbatch
				else:
					batch =""
				if user.userabout != None:
					about = user.userabout
				else:
					about =""
				if user.userblog != None:
					blog = user.userblog
				else:
					blog =""
				if user.userweb != None:
					web = user.userweb
				else:
					web =""
				if user.userorkut != None:
					orkut = user.userorkut
				else:
					orkut =""
				if user.userphone != None:
					phone = user.userphone
				else:
					phone =""
					
				#Dropdown generator
				majordrop = """
								<div>
								Major:
								<select name="formusermajor">
								<option>Biology</option>
								<option>Chemistry</option>
								<option>Mathematics</option>
								<option>Physics</option>
								</select>
								</div>
							"""
				if major == "Biology" :
					majordrop = """
								<div>
								Major:
								<select name="formusermajor">
								<option selected>Biology</option>
								<option>Chemistry</option>
								<option>Mathematics</option>
								<option>Physics</option>
								</select>
								</div>
							"""
				if major == "Physics" :
					majordrop = """
								<div>
								Major:
								<select name="formusermajor">
								<option>Biology</option>
								<option>Chemistry</option>
								<option>Mathematics</option>
								<option selected>Physics</option>
								</select>
								</div>
							"""
				if major == "Mathematics" :
					majordrop = """
								<div>
								Major:
								<select name="formusermajor">
								<option>Biology</option>
								<option>Chemistry</option>
								<option selected>Mathematics</option>
								<option>Physics</option>
								</select>
								</div>
							"""
				if major == "Chemisty" :
					majordrop = """
								<div>
								Major:
								<select name="formusermajor">
								<option>Biology</option>
								<option selected>Chemistry</option>
								<option>Mathematics</option>
								<option>Physics</option>
								</select>
								</div>
							"""


				########################
				yeardrop = """
								<div>
								Year:
								<select name="formuseryear">
								<option>1st</option>
								<option>2nd</option>
								<option>3rd</option>
								<option>4th</option>
								<option>5th</option>
								</select>
								</div>
							"""

				
				if year == "1st" :
					yeardrop = """
								<div>
								Year:
								<select name="formuseryear">
								<option selected>1st</option>
								<option>2nd</option>
								<option>3rd</option>
								<option>4th</option>
								<option>5th</option>
								</select>
								</div>
							"""
				if year == "2nd" :
					yeardrop = """
								<div>
								Year:
								<select name="formuseryear">
								<option>1st</option>
								<option selected>2nd</option>
								<option>3rd</option>
								<option>4th</option>
								<option>5th</option>
								</select>
								</div>
							"""
				if year == "3rd" :
					yeardrop = """
								<div>
								Year:
								<select name="formuseryear">
								<option>1st</option>
								<option>2nd</option>
								<option selected>3rd</option>
								<option>4th</option>
								<option>5th</option>
								</select>
								</div>
							"""
				if year == "4th" :
					yeardrop = """
								<div>
								Year:
								<select name="formuseryear">
								<option>1st</option>
								<option>2nd</option>
								<option>3rd</option>
								<option>4th</option>
								<option selected>5th</option>
								</select>
								</div>
							"""
				if year == "5th" :
					yeardrop = """
								<div>
								Year:
								<select name="formuseryear">
								<option>1st</option>
								<option>2nd</option>
								<option>3rd</option>
								<option>4th</option>
								<option selected>5th</option>
								</select>
								</div>
							"""
				#######################
				batchdrop="""
								<div>Batch:
								<select name="formuserbatch">
								<option>2006-2011</option>
								<option>2007-2012</option>
								<option>2008-2013</option>
								<option>2009-2014</option>
								<option>2010-2015</option>
								</select>
								</div>

							"""			
				if batch == "2006-2011" :
					batchdrop="""
								<div>Batch:
								<select name="formuserbatch">
								<option selected>2006-2011</option>
								<option>2007-2012</option>
								<option>2008-2013</option>
								<option>2009-2014</option>
								<option>2010-2015</option>
								</select>
								</div>

							"""				
				if batch == "2007-2012" :
					batchdrop="""
								<div>Batch:
								<select name="formuserbatch">
								<option>2006-2011</option>
								<option selected>2007-2012</option>
								<option>2008-2013</option>
								<option>2009-2014</option>
								<option>2010-2015</option>
								</select>
								</div>

							"""				
				if batch == "2008-2013" :
					batchdrop="""
								<div>Batch:
								<select name="formuserbatch">
								<option>2006-2011</option>
								<option>2007-2012</option>
								<option selected>2008-2013</option>
								<option>2009-2014</option>
								<option>2010-2015</option>
								</select>
								</div>

							"""				
				if batch == "2009-2014" :
					batchdrop="""
								<div>Batch:
								<select name="formuserbatch">
								<option>2006-2011</option>
								<option>2007-2012</option>
								<option>2008-2013</option>
								<option selected>2009-2014</option>
								<option>2010-2015</option>
								</select>
								</div>

							"""				
				if batch == "2010-2015" :
					batchdrop="""
								<div>Batch:
								<select name="formuserbatch">
								<option>2006-2011</option>
								<option>2007-2012</option>
								<option>2008-2013</option>
								<option>2009-2014</option>
								<option selected>2010-2015</option>
								</select>
								</div>

							"""				

				######################
				self.response.out.write("""
							<html>
							<head>
					<link rel="stylesheet" href="/static/iiser1.css" type="text/css" />
							</head>
							<body>
								<h2> """ + greeting + """</h2>
								<p>Kindly fill out the following form, if you want the html to be generated automatically for you.</p>
								<p>Alternatively, you can upload your own html and css as well by clicking <a href="/adduser4">here</a>.</p>
								<p>
								<form name="userinput" action="/usereditsubmit" enctype="multipart/form-data" method="post">
								<div>Fullname:<input type="text" name="formuserfullname" value='"""+ fullname +"""'></div>
								<div>Email:<input type="text" name="formuseremail" value='"""+ email +"""'></div>
								""" + majordrop + yeardrop + batchdrop + """	
								<div>AboutMe:<br/><textarea name="formuserabout" rows="10" cols="70" wrap="off">"""+about+"""</textarea></div>
								<div>Image:<input type="file" name="formuserimg"/><i>Upload a png image.</i></div>
								<div><i>Kindly provide full link (including http://) for the following, e.g. http://www.example.com</i></div>
								<div>Blog:<input type="text" name="formuserblog" value='"""+ blog +"""'/></div>
								<div>Personal Website:<input type="text" name="formuserweb"value='"""+ web +"""'/></div>
								<div>Orkut Profile:<input type="text" name="formuserorkut"value='"""+ orkut +"""'/></div>
								<div>Phone:<input type="text" name="formuserphn"value='"""+ phone +"""'/></div>
								<div>HTML:<i>Either fill both the HTML or CSS properly or leave them blank, don't botch them up unnecessarily.</i><br/>
								<textarea name="formuserhtml" rows="10" cols="70" wrap="off"/></textarea></div>
								<div>CSS:<br/>
								<textarea name="formusercss" rows="10" cols="70" wrap="off"/></textarea></div>
								<div><input type="submit" value="Submit"/></div>
								</form>
							</body>
							</html>
							""")
		if flag == 0 :
			self.response.out.write("""
						<html>
						<head></head>
						<body>
							<h2> I couldn't find you in the DBase </h>
							<p> Click <a href='/adduser0'>here</a> to add yourself.</p>
						</body>
						</html>
						""")
								
class UserEditSubmit(webapp.RequestHandler):			#Login needed, HTML generation from submitted form
	def post(self):
		loggedin = users.get_current_user()
		htmlhead="""
			<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
			<html xmlns="http://www.w3.org/1999/xhtml">
			<head>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
			<meta name="generator" content="HTML Tidy for Linux (vers 1 September 2005), see www.w3.org" />
			<meta content='Personal website of """ + self.request.get('formuserfullname') + """.' name='description'/>
			<meta content='"""+ self.request.get('formuserfullname') +""","""+ loggedin.nickname() +""",iiser,
			iiserk, iiserkol, iiserkolkata, """+ self.request.get('formusermajor') +"""' name='keywords'/>
			<title>"""+self.request.get('formuserfullname')+"""</title>
			<link rel="stylesheet" href='/css/"""+ loggedin.nickname() +"""' type="text/css" />
			</head>"""
			
		htmlbody1="""
			<body>
			<h1>"""+ self.request.get('formuserfullname') +"""</h1>
			<div id="designation">
			<h3>iiser kolkata</h3>

			<p>student &raquo; """+ self.request.get('formusermajor') +""" major, MS """+ self.request.get('formuseryear') +""" Year<br />
			batch &raquo; """+self.request.get('formuserbatch')+"""<br /></p>
			</div>
			<div id="sidephoto"><img src='/img/"""+ loggedin.nickname() +"""' alt='"""+ self.request.get('formuserfullname') +"""' width="250" /></div>
			"""
			
		about="""
			<div id="about">
			<ul><pre>""" + self.request.get('formuserabout') + """</pre></ul>
			</div>
			"""
		contact_top="""
			<div id="contact">
			<h3>contact</h3>
			<p>
			"""
		contact_lines =""
		if (self.request.get('formuseremail')) != "":
			contact_lines += """email: <a href='mailto:""" +(self.request.get('formuseremail'))+ """'>"""+ (self.request.get('formuseremail')) +"""</a><br />"""
		if (self.request.get('formuserweb')) != "":
			contact_lines += """website: <a href='""" +(self.request.get('formuserweb'))+ """'>"""+ (self.request.get('formuserweb')) +"""</a><br />"""
		if (self.request.get('formuserblog')) != "":
			contact_lines += """blog: <a href='""" +self.request.get('formuserblog')+ """'>"""+ self.request.get('formuserblog') +"""</a><br />"""
		if (self.request.get('formuserorkut')) != "":
			contact_lines += """orkut: <a href='""" +(self.request.get('formuserorkut'))+ """'>Profile</a><br />"""
		contact_bottom="""
			</p>
			</div>
			"""
		contact = contact_top + contact_lines + contact_bottom	
			
		htmlbody2="""
			</body>
			</html>
			"""
			
		if self.request.get('formuserhtml') != "":
			htmlcode = self.request.get('formuserhtml')
		else:
			htmlcode = htmlhead + htmlbody1 + about + contact + htmlbody2
		if self.request.get('formusercss') !="":
			csscode = self.request.get('formusercss')
		else:
			csscode="""
				body {
				width: 720px; margin:auto;
				background-color:transparent; padding: 10px;
				font-family : Arial, Helvetica, sans-serif;
				color : #333333;
				}

				#designation {
				width : auto;
				font : 85% "Trebuchet MS", Arial, Helvetica, sans-serif;
				color : grey;
				}

				#designation h3 {
				font : 170% arial;
				color : gold;
				text-transform : lowercase;
				margin : 0;
				padding : 0 0 0 0px;
				}

				#sidephoto {
				float : left;
				width : 300px;
				padding : 5px;
				}

				#about {
				font : 90% Arial, Helvetica, sans-serif;
				float : right;
				width : 400px;
				height : 500px;
				padding : 5px;
				}

				#contact {
				float : left;
				width : auto;
				padding : 5px;
				font : 85% "Trebuchet MS", Arial, Helvetica, sans-serif;
				color : grey;
				}
				"""
		allusers = db.GqlQuery("SELECT * FROM User ORDER BY username")
		for user in allusers:
			if loggedin.nickname() == user.username:
				oldavatar = user.useravatar
				user.delete()
				newuser = User()
				newuser.username = loggedin.nickname()
				newuser.userhtml = htmlcode
				newuser.usercss = csscode
				newuser.userfullname = (self.request.get('formuserfullname'))
				newuser.usermajor = (self.request.get('formusermajor'))
				newuser.userbatch = (self.request.get('formuserbatch'))
				newuser.useryear = (self.request.get('formuseryear'))
				newuser.userabout = (self.request.get('formuserabout'))
				if (self.request.get('formuseremail')) != "":
					newuser.useremail = (self.request.get('formuseremail'))
				if (self.request.get('formuserblog')) != "":
					newuser.userblog = (self.request.get('formuserblog'))
				if (self.request.get('formuserweb')) != "":
					newuser.userweb = (self.request.get('formuserweb'))
				if (self.request.get('formuserorkut')) != "":
					newuser.userorkut = (self.request.get('formuserorkut'))
				if (self.request.get('formuserphn')) != "":
					newuser.userphone = self.request.get('formuserphn')
				if (self.request.get('formuserimg')) != "":
					avatar = images.im_feeling_lucky(self.request.get("formuserimg"))
					newuser.useravatar = db.Blob(avatar)
				else:
					newuser.useravatar = db.Blob(oldavatar)
				newuser.put()

		self.redirect("""/~""" + loggedin.nickname())
		
class AdminEditing0(webapp.RequestHandler):			# Admin Login required for this
	def get(self):
		allusers = db.GqlQuery("SELECT * FROM User ORDER BY username")
		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write("""
					<html>
					<head>
					<link rel="stylesheet" href="/static/iiser1.css" type="text/css" />
					</head>
					<body>
						<div><h1>Admin Page for Editing Users' pages</h1></div>
						<div>
							<p> Select the username to be edited :</p>	
							<form name="userac" action="/adminedit1" method="post">
								usernames:<br/>
					""")
		for users in allusers:
			self.response.out.write(users.username+"""<br/>""")
		self.response.out.write("""
								<input type="text" name="uname"/>
								<input type="submit" value="Submit">
							</form>
						</div>
						</div>
					</body>
					</html>
					""")

		
class AdminEditing1(webapp.RequestHandler):			# Admin Login required for this
	def post(self):
		userac = self.request.get('uname')
		flag =0

		fullname =""
		email=""
		major=""
		year=""
		batch=""
		about=""
		blog=""
		web=""
		orkut=""
		phone=""
		html=""
		css=""
		allusers = db.GqlQuery("SELECT * FROM User ORDER BY username")
		for user in allusers:
			if userac == user.username:
				flag =1
				if user.userfullname != None:
					fullname = user.userfullname
				if user.useremail != None:
					email = user.useremail
				if user.usermajor != None:
					major = user.usermajor
				if user.useryear != None:
					year = user.useryear
				if user.userbatch != None:
					batch = user.userbatch
				if user.userabout != None:
					about = user.userabout
				if user.userblog != None:
					blog = user.userblog
				if user.userweb != None:
					web = user.userweb
				if user.userorkut != None:
					orkut = user.userorkut
				if user.userphone != None:
					phone = user.userphone
				html = user.userhtml
				css = user.usercss
					
		#Dropdown generator
		majordrop = """
						<div>
						Major:
						<select name="formusermajor">
						<option>Biology</option>
						<option>Chemistry</option>
						<option>Mathematics</option>
						<option>Physics</option>
						</select>
						</div>
					"""
		if major == "Biology" :
			majordrop = """
						<div>
						Major:
						<select name="formusermajor">
						<option selected>Biology</option>
						<option>Chemistry</option>
						<option>Mathematics</option>
						<option>Physics</option>
						</select>
						</div>
					"""
		if major == "Physics" :
			majordrop = """
						<div>
						Major:
						<select name="formusermajor">
						<option>Biology</option>
						<option>Chemistry</option>
						<option>Mathematics</option>
						<option selected>Physics</option>
						</select>
						</div>
					"""
		if major == "Mathematics" :
			majordrop = """
						<div>
						Major:
						<select name="formusermajor">
						<option>Biology</option>
						<option>Chemistry</option>
						<option selected>Mathematics</option>
						<option>Physics</option>
						</select>
						</div>
					"""
		if major == "Chemisty" :
			majordrop = """
						<div>
						Major:
						<select name="formusermajor">
						<option>Biology</option>
						<option selected>Chemistry</option>
						<option>Mathematics</option>
						<option>Physics</option>
						</select>
						</div>
					"""


		########################
		yeardrop = """
						<div>
						Year:
						<select name="formuseryear">
						<option>1st</option>
						<option>2nd</option>
						<option>3rd</option>
						<option>4th</option>
						<option>5th</option>
						</select>
						</div>
					"""

		
		if year == "1st" :
			yeardrop = """
						<div>
						Year:
						<select name="formuseryear">
						<option selected>1st</option>
						<option>2nd</option>
						<option>3rd</option>
						<option>4th</option>
						<option>5th</option>
						</select>
						</div>
					"""
		if year == "2nd" :
			yeardrop = """
						<div>
						Year:
						<select name="formuseryear">
						<option>1st</option>
						<option selected>2nd</option>
						<option>3rd</option>
						<option>4th</option>
						<option>5th</option>
						</select>
						</div>
					"""
		if year == "3rd" :
			yeardrop = """
						<div>
						Year:
						<select name="formuseryear">
						<option>1st</option>
						<option>2nd</option>
						<option selected>3rd</option>
						<option>4th</option>
						<option>5th</option>
						</select>
						</div>
					"""
		if year == "4th" :
			yeardrop = """
						<div>
						Year:
						<select name="formuseryear">
						<option>1st</option>
						<option>2nd</option>
						<option>3rd</option>
						<option>4th</option>
						<option selected>5th</option>
						</select>
						</div>
					"""
		if year == "5th" :
			yeardrop = """
						<div>
						Year:
						<select name="formuseryear">
						<option>1st</option>
						<option>2nd</option>
						<option>3rd</option>
						<option>4th</option>
						<option selected>5th</option>
						</select>
						</div>
					"""
		#######################
		batchdrop="""
						<div>Batch:
						<select name="formuserbatch">
						<option>2006-2011</option>
						<option>2007-2012</option>
						<option>2008-2013</option>
						<option>2009-2014</option>
						<option>2010-2015</option>
						</select>
						</div>

					"""			
		if batch == "2006-2011" :
			batchdrop="""
						<div>Batch:
						<select name="formuserbatch">
						<option selected>2006-2011</option>
						<option>2007-2012</option>
						<option>2008-2013</option>
						<option>2009-2014</option>
						<option>2010-2015</option>
						</select>
						</div>

					"""				
		if batch == "2007-2012" :
			batchdrop="""
						<div>Batch:
						<select name="formuserbatch">
						<option>2006-2011</option>
						<option selected>2007-2012</option>
						<option>2008-2013</option>
						<option>2009-2014</option>
						<option>2010-2015</option>
						</select>
						</div>

					"""				
		if batch == "2008-2013" :
			batchdrop="""
						<div>Batch:
						<select name="formuserbatch">
						<option>2006-2011</option>
						<option>2007-2012</option>
						<option selected>2008-2013</option>
						<option>2009-2014</option>
						<option>2010-2015</option>
						</select>
						</div>

					"""				
		if batch == "2009-2014" :
			batchdrop="""
						<div>Batch:
						<select name="formuserbatch">
						<option>2006-2011</option>
						<option>2007-2012</option>
						<option>2008-2013</option>
						<option selected>2009-2014</option>
						<option>2010-2015</option>
						</select>
						</div>

					"""				
		if batch == "2010-2015" :
			batchdrop="""
						<div>Batch:
						<select name="formuserbatch">
						<option>2006-2011</option>
						<option>2007-2012</option>
						<option>2008-2013</option>
						<option>2009-2014</option>
						<option selected>2010-2015</option>
						</select>
						</div>

					"""				

		######################
		self.response.out.write("""
					<html>
					<head>
					</head>
					<body>
					""")
		if flag==1:
			self.response.out.write("""
						<h2> Edit existing user:""" + userac + """</h2>
						""")
		else:
			self.response.out.write("""
						<h2> Add new user: """ + userac + """</h2>
						""")
		self.response.out.write("""
						<p>Kindly fill out the following form, if you want the html to be generated automatically for you.</p>
						<p>Alternatively, you can upload your own html and css as well by clicking <a href="/adduser4">here</a>.</p>
						<p>
						<form name="userinput" action="/admineditsubmit" enctype="multipart/form-data" method="post">
						<div>Username:<input type="text" name="username" value='"""+ userac +"""'></div>
						<div>Fullname:<input type="text" name="formuserfullname" value='"""+ fullname +"""'></div>
						<div>Email:<input type="text" name="formuseremail" value='"""+ email +"""'></div>
						""" + majordrop + yeardrop + batchdrop + """	
						<div>AboutMe:<br/><textarea name="formuserabout" rows="10" cols="70" wrap="off">"""+about+"""</textarea></div>
						<div>Image:<input type="file" name="formuserimg"/><i>Upload a png image.</i></div>
						<div><i>Kindly provide full link (including http://) for the following, e.g. http://www.example.com</i></div>
						<div>Blog:<input type="text" name="formuserblog" value='"""+ blog +"""'/></div>
						<div>Personal Website:<input type="text" name="formuserweb"value='"""+ web +"""'/></div>
						<div>Orkut Profile:<input type="text" name="formuserorkut"value='"""+ orkut +"""'/></div>
						<div>Phone:<input type="text" name="formuserphn"value='"""+ phone +"""'/></div>
						<div>HTML:<i>Either fill both the HTML or CSS properly or leave them blank, don't botch them up unnecessarily.</i><br/>
						<textarea name="formuserhtml" rows="20" cols="110" wrap="off"/>"""+html+"""</textarea></div>
						<div>CSS:<br/>
						<textarea name="formusercss" rows="20" cols="110" wrap="off"/>"""+css+"""</textarea></div>
						<div><input type="submit" value="Submit"/></div>
						</form>
					</body>
					</html>
					""")
		

class AdminEditSubmit(webapp.RequestHandler):			#Admin Login needed, HTML generation from submitted form
	def post(self):
		userac = self.request.get('username')
		htmlhead="""
			<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
			<html xmlns="http://www.w3.org/1999/xhtml">
			<head>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
			<meta name="generator" content="HTML Tidy for Linux (vers 1 September 2005), see www.w3.org" />
			<meta content='Personal website of """ + self.request.get('formuserfullname') + """.' name='description'/>
			<meta content='"""+ self.request.get('formuserfullname') +""","""+ userac +""",iiser,
			iiserk, iiserkol, iiserkolkata, """+ self.request.get('formusermajor') +"""' name='keywords'/>
			<title>"""+self.request.get('formuserfullname')+"""</title>
			<link rel="stylesheet" href='/css/"""+ userac +"""' type="text/css" />
			</head>"""
			
		htmlbody1="""
			<body>
			<h1>"""+ self.request.get('formuserfullname') +"""</h1>
			<div id="designation">
			<h3>iiser kolkata</h3>

			<p>student &raquo; """+ self.request.get('formusermajor') +""" major, MS """+ self.request.get('formuseryear') +""" Year<br />
			batch &raquo; """+self.request.get('formuserbatch')+"""<br /></p>
			</div>
			<div id="sidephoto"><img src='/img/"""+ userac +"""' alt='"""+ self.request.get('formuserfullname') +"""' width="250" /></div>
			"""
			
		about="""
			<div id="about">
			<ul><pre>""" + self.request.get('formuserabout') + """</pre></ul>
			</div>
			"""
		contact_top="""
			<div id="contact">
			<h3>contact</h3>
			<p>
			"""
		contact_lines =""
		if (self.request.get('formuseremail')) != "":
			contact_lines += """email: <a href='mailto:""" +(self.request.get('formuseremail'))+ """'>"""+ (self.request.get('formuseremail')) +"""</a><br />"""
		if (self.request.get('formuserweb')) != "":
			contact_lines += """website: <a href='""" +(self.request.get('formuserweb'))+ """'>"""+ (self.request.get('formuserweb')) +"""</a><br />"""
		if (self.request.get('formuserblog')) != "":
			contact_lines += """blog: <a href='""" +self.request.get('formuserblog')+ """'>"""+ self.request.get('formuserblog') +"""</a><br />"""
		if (self.request.get('formuserorkut')) != "":
			contact_lines += """orkut: <a href='""" +(self.request.get('formuserorkut'))+ """'>Profile</a><br />"""
		contact_bottom="""
			</p>
			</div>
			"""
		contact = contact_top + contact_lines + contact_bottom	
			
		htmlbody2="""
			</body>
			</html>
			"""
		if self.request.get('formuserhtml') != "":
			htmlcode = self.request.get('formuserhtml')
		else:
			htmlcode = htmlhead + htmlbody1 + about + contact + htmlbody2
		if self.request.get('formusercss') !="":
			csscode = self.request.get('formusercss')
		else:
			csscode="""
				body {
				width: 720px; margin:auto;
				background-color:transparent; padding: 10px;
				font-family : Arial, Helvetica, sans-serif;
				color : #333333;
				}

				#designation {
				width : auto;
				font : 85% "Trebuchet MS", Arial, Helvetica, sans-serif;
				color : grey;
				}

				#designation h3 {
				font : 170% arial;
				color : gold;
				text-transform : lowercase;
				margin : 0;
				padding : 0 0 0 0px;
				}

				#sidephoto {
				float : left;
				width : 300px;
				padding : 5px;
				}

				#about {
				font : 90% Arial, Helvetica, sans-serif;
				float : right;
				width : 400px;
				height : 500px;
				padding : 5px;
				}

				#contact {
				float : left;
				width : auto;
				padding : 5px;
				font : 85% "Trebuchet MS", Arial, Helvetica, sans-serif;
				color : grey;
				}
				"""
		allusers = db.GqlQuery("SELECT * FROM User ORDER BY username")
		foundflag=0
		for user in allusers:
			if userac == user.username:
				foundflag=1
				oldavatar = user.useravatar
				user.delete()
				newuser = User()
				newuser.username = userac
				newuser.userhtml = htmlcode
				newuser.usercss = csscode
				newuser.userfullname = (self.request.get('formuserfullname'))
				newuser.usermajor = (self.request.get('formusermajor'))
				newuser.userbatch = (self.request.get('formuserbatch'))
				newuser.useryear = (self.request.get('formuseryear'))
				newuser.userabout = (self.request.get('formuserabout'))
				if (self.request.get('formuseremail')) != "":
					newuser.useremail = (self.request.get('formuseremail'))
				if (self.request.get('formuserblog')) != "":
					newuser.userblog = (self.request.get('formuserblog'))
				if (self.request.get('formuserweb')) != "":
					newuser.userweb = (self.request.get('formuserweb'))
				if (self.request.get('formuserorkut')) != "":
					newuser.userorkut = (self.request.get('formuserorkut'))
				if (self.request.get('formuserphn')) != "":
					newuser.userphone = self.request.get('formuserphn')
				if (self.request.get('formuserimg')) != "":
					avatar = images.im_feeling_lucky(self.request.get("formuserimg"))
					newuser.useravatar = db.Blob(avatar)
				else:
					newuser.useravatar = db.Blob(oldavatar)
				newuser.put()
		if foundflag == 0:
			newuser = User()
			newuser.username = userac
			newuser.userhtml = htmlcode
			newuser.usercss = csscode
			newuser.userfullname = (self.request.get('formuserfullname'))
			newuser.usermajor = (self.request.get('formusermajor'))
			newuser.userbatch = (self.request.get('formuserbatch'))
			newuser.useryear = (self.request.get('formuseryear'))
			newuser.userabout = (self.request.get('formuserabout'))
			if (self.request.get('formuseremail')) != "":
				newuser.useremail = (self.request.get('formuseremail'))
			if (self.request.get('formuserblog')) != "":
				newuser.userblog = (self.request.get('formuserblog'))
			if (self.request.get('formuserweb')) != "":
				newuser.userweb = (self.request.get('formuserweb'))
			if (self.request.get('formuserorkut')) != "":
				newuser.userorkut = (self.request.get('formuserorkut'))
			if (self.request.get('formuserphn')) != "":
				newuser.userphone = self.request.get('formuserphn')
			if (self.request.get('formuserimg')) != "":
				avatar = images.im_feeling_lucky(self.request.get("formuserimg"))
				newuser.useravatar = db.Blob(avatar)
			newuser.put()

		self.redirect("""/~""" + userac)
user = webapp.WSGIApplication([(r'/%7E(.*)', UserPage),
				('/img/(.*)', ImageSpew),
				('/css/(.*)', CssSpew),
				('/students.html', StudentsList),
				('/students',StudentsList),
				('/adduser0', UserAddStep0),
				('/adduser1', UserAddStep1),
				('/adduser2', UserAddStep2),			#Login required
				('/adduser3', UserAddStep3),
				('/adduser5', UserAddStep5),			#Login required
				('/useredit', UserEditing),			#Login required
				('/usereditsubmit', UserEditSubmit),		#Login required
				('/adminedit0', AdminEditing0),			#Admin Login required
				('/adminedit1', AdminEditing1),			#Admin Login required
				('/admineditsubmit', AdminEditSubmit)],		#Admin Login required
				debug=True)

def main():
	run_wsgi_app(user)

if __name__ == "__main__":
	main()

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


from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch


class HomePage(webapp.RequestHandler):
	def get(self):
		try:
#			feeds = urlfetch.fetch("http://feedproxy.google.com/Iiserk?format=sigpro")
			feeds = urlfetch.fetch("http://feeds.feedburner.com/iiserk-notices?format=sigpro")
			feedtext = feeds.content
			feedtext = feedtext.replace('document.write(\'','')
			feedtext = feedtext.replace('\');','')
			feedtext = """<div id="feed">""" + feedtext + """</div>"""
			
		except:
			feedtext = """<div id="feed"> Sorry could not fetch feeds.</div>"""

		page = """
			<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
			<html>
			<head>
			<meta name="generator" content="HTML Tidy for Linux (vers 1 September 2005), see www.w3.org">
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
			<meta name="verify-v1" content="UpHllLbRYQI9rBcZMnPc6Vnk7pmFZ7CtOMG8QYb3irI=">
			<link rel="stylesheet" href="/static/iiser1.css" type="text/css">
			<title>IISER Kolkata Students' Site</title>

			<style type="text/css">
			/*<![CDATA[*/
			 p.c2 {text-align: right}
			 img.c1 {border:0; width:60px;height:21px}
			/*]]>*/
			</style>
			</head>
			<body>
			<div id="content">
			<div id="header">
			<h1>iiser kolkata <span class="smaller">unofficial site</span></h1>
			</div>
			""" + feedtext + """
			<div id="text">
			<p>
			We're here to write about us. Bound by a common love
of science, this website is the showcase of what's
happening with those who <a href="/students">study</a> at this cool place,
a <a href="http://planet.iiserk.net">zeitgeist</a> of <a href="http://www.iiserkol.ac.in">IISER Kolkata</a>.</p>
			</div>
			<div id="linkbox">
			<ul>
			<li><a href="/students">students' homepages</a></li>
			<li>file archives<br/><a href="http://phy.iiserk.net">physics</a>,
			<a href="http://chem.iiserk.net">chemistry</a>,
			<a href="http://bio.iiserk.net">biology</a>,
			<a href="http://maths.iiserk.net">mathematics</a></li>

			<li><a href="http://lib.iiserkol.ac.in/cgi-bin/gw_48_0_3_3/chameleon/">institute library</a></li>
			<li>hostel server (currently down)</li>
			<li><a href="http://planet.iiserk.net">planet iiserk</a></li>
			</ul>
			</div>
			</div>
			<!--Tracker Code -->
			<script type="text/javascript">
			//<![CDATA[
			var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
			document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
			//]]>
			</script><script type="text/javascript">
			//<![CDATA[
			try {
			var pageTracker = _gat._getTracker("UA-3245579-6");
			pageTracker._trackPageview();
			} catch(err) {}
			//]]>
			</script><!--Tracker Code -->
			</body>
			</html>

		"""

		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write(page)

home = webapp.WSGIApplication([('/', HomePage)])

def main():
	run_wsgi_app(home)

if __name__ == "__main__":
	main()

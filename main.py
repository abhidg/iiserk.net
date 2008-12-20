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
			feeds = urlfetch.fetch("http://feedproxy.google.com/Iiserk?format=sigpro")
			feedtext = feeds.content
			feedtext = feedtext.replace('document.write(\'','')
			feedtext = feedtext.replace('\');','')
			feedtext = """<div id="feed">""" + feedtext + """</div>"""
			
		except:
			feedtext = """<div id="feed"> Sorry could not fetch feeds.</div>"""

		page = """
			<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
			<html xmlns="http://www.w3.org/1999/xhtml">
			<head>
			<meta name="generator" content="HTML Tidy for Linux (vers 1 September 2005), see www.w3.org" />
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
			<meta name="verify-v1" content="UpHllLbRYQI9rBcZMnPc6Vnk7pmFZ7CtOMG8QYb3irI=" />
			<link rel="stylesheet" href="/static/iiser.css" type="text/css" />
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
			<p>The Government of India, through the Ministry of Human Resource Development (MHRD), and based on the recommendation of Scientific Advisory Council to the Prime Minister, 
			decided to create a few undergraduate science universities. Named as the INDIAN INSTITUTE OF SCIENCE EDUCATION AND RESEARCH (IISER), these IISERs are designed to reach the
			prestigious position in the global setting that IISc, IIMs and IITs presently enjoy. Two of the IISERs located in Pune and Kolkata started their academic programme in 
			August 2006. The third in Mohali, Chandigarh has started its own activities in 2007.</p>
			<p>Each IISER is an autonomous institution awarding its own degrees. The central theme of the IISER is to integrate education with research so that undergraduate teaching 
			as well as doctoral and postdoctoral research work are carried out in symbiosis. Students are encouraged to carry out research projects during the vacation periods in the
			first four years of their Masters programme in various research institutes outside IISER. In the fifth year the students are required to participate in a research seminar
			and also carry out a research project on which a thesis will have to be written." -- 
			<a href="http://www.iiserkol.ac.in">http://www.iiserkol.ac.in</a></p>
			</div>
			<div id="linkbox">
			<ul>
			<li>Students' <a href="/students.html">homepages</a>.</li>
			<li>File Archives: <a href="http://phy.iiserk.net">Physics</a>, <a href="http://chem.iiserk.net">Chemistry</a>, <a href="http://bio.iiserk.net">Biology</a> and <a 
			href="http://maths.iiserk.net">Mathematics</a></li>
			<li><a href="http://lib.iiserkol.ac.in/cgi-bin/gw_48_0_3_3/chameleon/">Library</a></li>
			<li>See our hostel <a href="http://server.iiserk.net">server</a> web page.</li>
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

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

import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template

class HomePage(webapp.RequestHandler):
	def get(self):
		try:
#			feeds = urlfetch.fetch("http://feedproxy.google.com/Iiserk?format=sigpro")
			feeds = urlfetch.fetch("http://feeds.feedburner.com/iiserk-notices?format=sigpro")
			feedtext = feeds.content
			feedtext = feedtext.replace('document.write(\'','')
			feedtext = feedtext.replace('\');','')
			feedtext = """<div id="feed">""" + feedtext + """</div>"""
			feedtext = feedtext.replace("<br>","<br/>")
			feedtext = feedtext.replace("""target="_blank">"""," >")
			feedtext = feedtext.replace("""target="_blank">"""," >")
			feedtext = feedtext.replace("""<img border="0" src="http://www.feedburner.com/fb/i/icn/feed-icon-10x10.gif"/>""", \
				"""<img style="border: 0" src="http://www.feedburner.com/fb/i/icn/feed-icon-10x10.gif" alt="feedburner" />""" )
			
		except:
			feedtext = """<div id="feed"> Sorry could not fetch feeds.</div>"""

		template_values = { "feedtext": feedtext }

		path = os.path.join(os.path.dirname(__file__), 'templates','index.html')

		self.response.headers['Content-Type'] = 'text/html'
		self.response.out.write(template.render(path, template_values))

home = webapp.WSGIApplication([('/', HomePage)])

def main():
	run_wsgi_app(home)

if __name__ == "__main__":
	main()

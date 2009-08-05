from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class RedirectRequest(webapp.RequestHandler):
    def get(self, tail):
        self.redirect('/'+tail, permanent=True)
    def head(self, tail):
        self.redirect('/'+tail, permanent=True)

application = webapp.WSGIApplication([(r'^/static/(.*)\.html', RedirectRequest)])
def main(): run_wsgi_app(application)
if __name__ == "__main__": main()


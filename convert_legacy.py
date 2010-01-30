#!/opt/local/bin/python2.5

from models import Bet, Matchup, Unparsable
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from ladbrokes_parser import parse_date

class MainHandler(webapp.RequestHandler):
	def get(self):
		matches = Matchup.all().filter("date_match_formatted = ", None)
		for m in matches:
			self.response.out.write("converted %s vs %s @ %s (%s)" % (m.team_a_name, m.team_b_name, m.date_match_formatted, m.date_match))
			m.date_match_formatted = parse_date(m.date_match.split())
			m.put()
		self.response.out.write("done")

def main():
	application = webapp.WSGIApplication([('/convert', MainHandler)], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
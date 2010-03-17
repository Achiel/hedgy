#!/opt/local/bin/python2.5
from models import Bet, Matchup
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class MainHandler(webapp.RequestHandler):

	def get(self):
			w = self.response.out
			offset = self.request.get('offset')
			limit = self.request.get('limit')
			
			if limit is "":
			    limit = 100
			if offset is "":
			    offset = 0
			
			limit = int(limit)
			offset = int(offset)
			matches = Matchup.all()[offset:limit+offset]
			for m in matches:
				bets = Bet.all().filter("match = ", m)
				for b in bets:
					template = "%s;%s;%s;%s;%s;%s;%s" % (m.team_a_name, m.team_b_name, b.team_a_odds, b.team_b_odds,b.draw_odds,m.date_match_formatted, b.date_recorded)
					w.write(template)
					w.write("<br/>")

def main():
	application = webapp.WSGIApplication([('/csv', MainHandler)], debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()

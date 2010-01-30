#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import Matchup
from datetime import datetime, timedelta
from models import Bet

class MainHandler(webapp.RequestHandler):

	def get(self):
		w = self.response.out
		w.write("<a href='?till=24'>matches for the next 24h</a> ")
		w.write("<a href='?till=3'>matches for the next 3h</a> ")
		w.write("<a href='?till=3'>matches for the next hour</a> ")
		w.write("<a href='?till=all'>all matches</a>")
		w.write('<h1>matches:</h1>')

		matches = Matchup.all().order("date_match_formatted")

		span = self.request.get('till')
		if not span == "all":
			matches.filter("date_match_formatted > ", datetime.now())

		if not span == "" and not span == "all":
			span = int(span)
			matches.filter("date_match_formatted < ", datetime.now() + timedelta(hours=span))
			
		for m in matches:
			match_name = "%s vs %s" % (m.team_a_name, m.team_b_name)
			if  self.match_hot(m, w):
				style = "color: red"
			else:
				style = ""
			link = "<a style='%s' href='/match?team_a=%s&team_b=%s'>%s</a> at %s <br/>" % (style, m.team_a_name, m.team_b_name, match_name, m.date_match_formatted)
			w.write(link)

	def match_hot(self, m, w):
		
		bets = Bet.all().filter("match = ", m)
		odds_a = None
		odds_b = None
		odds_draw = None
		for b in bets:
			if odds_a == None:
				odds_a = b.team_a_odds
				odds_b = b.team_b_odds
				odds_draw = b.draw_odds
			
			if not odds_a == b.team_a_odds:
				return True
			if not odds_b == b.team_b_odds:
				return True
			if not odds_draw == b.draw_odds:
				return True
		return False

def main():
	application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()

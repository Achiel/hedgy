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
			matches.filter("date_match_formatted > ", datetime.now() - timedelta(hours=2))

		if not span == "" and not span == "all":
			span = int(span)
			matches.filter("date_match_formatted < ", datetime.now() + timedelta(hours=span))
			
		for m in matches:
			match_name = "%s vs %s" % (m.team_a_name, m.team_b_name)
			fluctuations = self.calc_fluctuation(m)
			if fluctuations == 2:
				style = "color: orange"
			elif fluctuations == 3:
				style = "color: red"
			else:
				style = ""
			link = "<a style='%s' href='/match?team_a=%s&team_b=%s'>%s</a> at %s" % (style, m.team_a_name, m.team_b_name, match_name, m.date_match_formatted)
			w.write(link)
			two_hours = timedelta(hours=2)
			diff = datetime.now() - m.date_match_formatted
			if diff < two_hours and diff > timedelta():
				w.write(" <a style='color: red' href='%s'>live</a>" % m.source)
			w.write("<br/>")
			

	def calc_fluctuation(self, m):
		bets = Bet.all().filter("match = ", m)
		s = set()
		
		map(s.add, [(b.team_a_odds, b.team_b_odds, b.draw_odds) for b in bets])
		return len(s)


def main():
	application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()

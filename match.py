#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from models import Matchup, Bet

class MainHandler(webapp.RequestHandler):

	def get(self):
		w = self.response.out
		team_a = self.request.get('team_a')
		team_b = self.request.get('team_b')
		if team_a == "":
			w.write('illegal request, need name for team a')
			return
		if team_b == "":
			w.write('illegal request, need name for team b')
			return
			
		matches = Matchup.all().filter('team_a_name = ', team_a).filter('team_b_name = ', team_b).fetch(1)
		if len(matches) == 0:
			w.write('no matches found')
			return
		
		match = matches[0]
		w.write("<h1>%s vs %s</h1>" % (match.team_a_name, match.team_b_name))
		w.write("<div>Match date: %s </div>" % match.date_match_formatted)
		bets = Bet.all().filter('match = ', match).fetch(1000)
		w.write("<table>")
		w.write("<tr><td>%s</td><td>Draw</td><td>%s</td><td>Recorded on</td><td>Current score</td></tr>" % (match.team_a_name, match.team_b_name))
		for b in bets:
			w.write("<tr>")
			w.write("<td>%s</td>" % b.team_a_odds)
			w.write("<td>%s</td>" % b.draw_odds)
			w.write("<td>%s</td>" % b.team_b_odds)
			w.write("<td>%s</td>" % b.date_recorded)
			w.write("<td>%s</td>" % b.current_score)
			w.write("</tr>")
		w.write("</table>")
		w.write('found %s bets' % len(bets))
		
def main():
	application = webapp.WSGIApplication([('/match', MainHandler)], debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()

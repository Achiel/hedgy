#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


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
		w.write("<div>Match date: %s </div>" % match.date_match)
		bets = Bet.all().filter('match = ', match).fetch(1000)
		w.write("<table>")
		w.write("<tr><td>%s</td><td>Draw</td><td>%s</td><td>Recorded on</td></tr>" % (match.team_a_name, match.team_b_name))
		for b in bets:
			w.write("<tr>")
			w.write("<td>%s</td>" % b.team_a_odds)
			w.write("<td>%s</td>" % b.draw_odds)
			w.write("<td>%s</td>" % b.team_b_odds)
			w.write("<td>%s</td>" % b.date_recorded)
			w.write("</tr>")
		w.write("</table>")
		w.write('found %s bets' % len(bets))
		
def main():
	application = webapp.WSGIApplication([('/match', MainHandler)], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()

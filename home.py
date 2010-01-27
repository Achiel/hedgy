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
#			if self.match_hot(m, w) == True:
#				w.write("woot")

	def match_hot(self, m, w):
		
		bets = Bet.all().filter("match = ", m)
		odds_a = None
		odds_b = None
		odds_draw = None
		fluctuation = False
		for b in bets:
			if odds_a == None:
				odds_a = b.team_a_odds
				odds_b = b.team_b_odds
				odds_draw = b.draw_odds
			
			if not odds_a == b.team_a_odds:
				fluctuation = True
			if not odds_b == b.team_b_odds:
				fluctuation = True
			if not odds_draw == b.draw_odds:
				fluctuation = True
		return fluctuation

def main():
	application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()

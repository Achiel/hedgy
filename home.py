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

class MainHandler(webapp.RequestHandler):

	def get(self):
		self.response.out.write('<h1>matches:</h1>')
		writer = self.response.out
		matches = Matchup.all()
		for m in matches:
			match_name = "%s vs %s" % (m.team_a_name, m.team_b_name)
			link = "<a href='/match?team_a=%s&team_b=%s'>%s</a><br/>" % (m.team_a_name, m.team_b_name, match_name)
			writer.write(link)
def main():
	application = webapp.WSGIApplication([('/', MainHandler)], debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()

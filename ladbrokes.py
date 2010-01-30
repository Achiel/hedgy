#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from ladbrokes_parser import LadbrokesParser
import urllib2

class MainHandler(webapp.RequestHandler):

	def get(self):

		url = "http://sports.ladbrokes.com/en-gb/Football-c110000006"
		url = "http://sports.ladbrokes.com/en-gb/Navigation?dispSortId=1&context=bycountryandleague&byocList=s1811|s548|s2522|s295|s150|s84|s93|s816|s85|s99|s100|s131|s1705|s1614|s1616|s76|s79|s127|s109|s1559|s1945|s106|s117|s115|s95|s128"
		try:
			parser = LadbrokesParser(url, self.response.out)
			count = parser.parse()
			self.response.out.write("Finished importing %s records from <a href='%s'>%s</a><br/> " % (count, url, url))
			self.response.out.write("<a href='/'>back to home</a>")
		except urllib2.URLError, e:
			self.response.out.write(e)

def main():
	application = webapp.WSGIApplication([('/ladbrokes', MainHandler)], debug=True)
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()

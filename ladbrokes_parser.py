#!/opt/local/bin/python2.5
from BeautifulSoup import BeautifulSoup
from models import Bet, Matchup, Unparsable
import urllib2
import re
from datetime import datetime
from unparsable_exception import UnparsableException

months = {"January" : 1, "February" : 2, "March" : 3, "April" : 4, "May" : 5, "June" : 6, "July" : 7, "August" : 8, "September" : 9, "October" : 10, "November" : 11, "December" : 12}

def calc_odds(tdstring):
	if tdstring == "evens":
		return 1.0
	odds = tdstring.partition("/")
	return float(odds[0])/float(odds[2])
	
def parse_row(a, row, url):


	safea = a.string.encode('ascii', 'replace')
	score = re.search("[0-9]\-[0-9]", safea)
	if score is not None:
		current_score = score.group()
		teams = safea.partition(' %s ' % current_score)
	else:
		teams = safea.partition(' vs ')

	team_a = teams[0]
	team_b = teams[2]

	match_date = row.td.a
	if match_date is None:
		match_date = row.td.div

	match_date = match_date['title']

	# empty rows:
	team_a_raw_odds = row.find('td', {'class' : 'odds'})
	if team_a_raw_odds == None:
		raise UnparsableException("Odds not found found for first team")
		return 0
	team_b_raw_odds = row.find('td', {'class' : 'odds noBorder '})
	if team_b_raw_odds == None:
		return 0
	draw_raw_odds = row.find('td', {'class' : 'odds noBorder'})
	if draw_raw_odds == None:
		return 0
		

	team_a_odds = calc_odds(team_a_raw_odds.a.string.strip().encode('ascii', 'replace'))
	team_b_odds = calc_odds(team_b_raw_odds.a.string.strip().encode('ascii', 'replace'))
	draw_odds = calc_odds(draw_raw_odds.a.string.strip().encode('ascii', 'replace'))
	matchup = Matchup.all().filter('team_a_name = ', team_a).filter('team_b_name', team_b)
	result = matchup.fetch(1);
	date_split = match_date.split()
	year = int(date_split[2])
	month = months[date_split[1]]
	day = int(date_split[0])
	hour = int(date_split[4].split(":")[0])
	minute = int(date_split[4].split(":")[1])
	
	date_match_formatted = datetime(year, month, day, hour, minute)
	if len(result) == 0:
		matchup = Matchup(team_a_name = team_a, team_b_name = team_b, 
			source = url, date_match = match_date, date_match_formatted = date_match_formatted
			)
		matchup.put()
	else:
		matchup = result[0]
	bet = Bet(team_a_odds = team_a_odds, team_b_odds = team_b_odds, 
			draw_odds = draw_odds,
			match = matchup
		)
	bet.put()
	
def parse_table(table, url):
	count = 0
	for row in table.findAll('tr'):
		for a in row.findAll('a', {'class': 'eventLink'})[:1]:
			try:
				parse_row(a, row, url)
				count += 1
			except Exception, errstr:
				if row.string is None:
					message = errstr
				else:
					message = "%s caused by %s" % (errstr, row.string.encode('ascii', 'replace'))
				u = Unparsable(message="unable to parse %s" % message, source=url)
				u.put()
				# print "unable to parse %s" % row
	return count
	
def parse(url, out):
	result = urllib2.urlopen(url)
	doc = result.read()
	# doc = open("ladbrokesallcups.txt")
	soup = BeautifulSoup(''.join(doc))
	
	count = 0
	for table in soup('table'):
		count += parse_table(table, url)
	
	result.close()
	return count

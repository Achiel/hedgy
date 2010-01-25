#!/opt/local/bin/python2.5
from BeautifulSoup import BeautifulSoup
from models import Bet, Matchup, Unparsable
import urllib2
import re

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
	
	team_a_odds = calc_odds(row.find('td', {'class' : 'odds'}).a.string.strip())
	team_b_odds = calc_odds(row.find('td', {'class' : 'odds noBorder '}).a.string.strip())
	draw_odds = calc_odds(row.find('td', {'class' : 'odds noBorder'}).a.string.strip())
	
	matchup = Matchup.all().filter('team_a_name = ', team_a).filter('team_b_name', team_b)
	result = matchup.fetch(1);
	if len(result) == 0:
		matchup = Matchup(team_a_name = team_a, team_b_name = team_b, 
			source = url, date_match = match_date
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
			except:
				u = Unparsable(message="unable to parse %s" % row, source=url)
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

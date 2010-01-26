import datetime
from google.appengine.ext import db

class Matchup(db.Model):
	team_a_name = db.StringProperty(required=True)
	team_b_name = db.StringProperty(required=True)
	source = db.LinkProperty(required=True)
	date_match = db.StringProperty(required=False)
	date_match_formatted = db.DateTimeProperty(required=False)
	
class Bet(db.Model):
	match = db.ReferenceProperty(Matchup)
	team_a_odds = db.FloatProperty(required=True)
	team_b_odds = db.FloatProperty(required=True)
	draw_odds = db.FloatProperty(required=False)
	date_recorded = db.DateTimeProperty(required=True, auto_now=True)
	current_score = db.StringProperty(required=False)

class Unparsable(db.Model):
	message = db.TextProperty(required=True)
	source = db.LinkProperty(required=False)
	date_recorded = db.DateTimeProperty(required=True, auto_now=True)

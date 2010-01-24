import datetime
from google.appengine.ext import db

class Bet(db.Model):
	team_a_name = db.StringProperty(required=True)
	team_b_name = db.StringProperty(required=True)
	team_a_odds = db.FloatProperty(required=True)
	team_b_odds = db.FloatProperty(required=True)
	draw_odds = db.FloatProperty(required=False)
	source = db.LinkProperty(required=True)
	date_recorded = db.DateTimeProperty(required=True, auto_now=True)
	date_match = db.StringProperty(required=False)
	current_score = db.StringProperty(required=False)

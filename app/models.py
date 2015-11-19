from app import db
from stravalib import unithelper

def minPerMile(meterPerSec):
	secPerMile=unithelper.mile/unithelper.meter/float(meterPerSec)
	return secPerMile/60.


class Run(db.Model):
	__tablename__='Run'
	athId=db.Column(db.Integer, nullable=False)
	actId=db.Column(db.Integer, primary_key=True, unique=True)
	dist=db.Column(db.Float, nullable=False) #distance in miles
	time=db.Column(db.Float, nullable=False) #moving time in seconds
	date=db.Column(db.DateTime, nullable=False)
	pace=db.Column(db.Float, nullable=False)
	maxPace=db.Column(db.Float, nullable=False)
	elevation=db.Column(db.Float, nullable=False) #elevation in feet
	name=db.Column(db.Float, nullable=False) #user's name for run
	def __init__(self, act):
		self.actId=act.id
		self.athId=act.athlete.id
		self.dist=float(unithelper.miles(act.distance))
		self.time=act.moving_time.seconds
		self.date=act.start_date
		print "start_date type",type(act.start_date)
		try:
			self.pace=ru.minPerMile(act.average_speed)
			self.maxPace=ru.minPerMile(act.max_speed)
		except:
			self.pace=0.
			self.maxPace=0.
		self.el=unithelper.feet(act.total_elevation_gain)
		self.name=act.name

class Challenge(db.Model):
	__tablename__='Challenge'
	challengeId=db.Column(db.String(64))
	athId=db.Column(db.Integer, nullable=False, primary_key=True)
	distance=db.Column(db.Float) #distance in miles
	time=db.Column(db.Float) #time in seconds

class AthleteStats(db.Model):
	__tablename__='AthleteStats'
	athId=db.Column(db.Integer, nullable=False, primary_key=True)
	RecentCount=db.Column(db.Integer)
	RecentDistance=db.Column(db.Float) #distance in miles
	RecentTime=db.Column(db.Float) #time in seconds
	RecentElevation=db.Column(db.Float) #elevation in feet
	YTDCount=db.Column(db.Integer)
	YTDDistance=db.Column(db.Float) #distance in miles
	YTDTime=db.Column(db.Float) #time in seconds
	YTDElevation=db.Column(db.Float) #elevation in feet
	AllCount=db.Column(db.Integer)
	AllDistance=db.Column(db.Float) #distance in miles
	AllTime=db.Column(db.Float) #time in seconds
	AllElevation=db.Column(db.Float) #elevation in feet
	def __init__(self, athStats, athId):
		self.athId=athId
		self.RecentCount=athStats.recent_run_totals.count
		self.RecentDistance= float(unithelper.miles(athStats.recent_run_totals.distance))#distance in miles
		self.RecentTime= float(unithelper.seconds(athStats.recent_run_totals.moving_time))#time in seconds
		self.YTDCount=athStats.ytd_run_totals.count
		self.YTDDistance= float(unithelper.miles(athStats.ytd_run_totals.distance))#distance in miles
		self.YTDTime= float(unithelper.seconds(athStats.ytd_run_totals.moving_time))#time in seconds
		self.AllCount=athStats.all_run_totals.count
		self.AllDistance= float(unithelper.miles(athStats.all_run_totals.distance))#distance in miles
		self.AllTime= float(unithelper.seconds(athStats.all_run_totals.moving_time))#time in seconds




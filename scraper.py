import stravalib, logging
import config, requests
from stravalib import unithelper
import simplejson as json
from BeautifulSoup import BeautifulSoup
import time, datetime
from app import db, models

TIME_BT_REQUESTS = 2
TIME_PERIOD_DAYS=365
minNumberRuns=0

def main():
	client = stravalib.client.Client(access_token=config.TOKEN)
	athlete = client.get_athlete()
def getChallengeRuns(challengeName="strava-races-10k-2015-10"):
	# taking athletes from http://www.strava.com/challenges/turn-up-the-heat-run
	# there are 17311 athletes registered for that challenge
	detailsUrl="https://www.strava.com/challenges/"+challengeName+"/details"
	athPerPage=1
	r = requests.get(detailsUrl)
	data = json.loads(r.text)
	nAthletes=int(data["totals"]["participants"])
	nActivities=int(data["totals"]["num_activities"])
	total_pages = nAthletes/athPerPage
	challenges=[]
	for page in range(1, total_pages + 2):
		pageUrl = detailsUrl+('?paging_type='
				'overall&per_page=%s&overall_page=%s&overall_male_page=1'
				'&overall_female_page=1' %(athPerPage, page))

		r = requests.get(pageUrl)
		data = json.loads(r.text)
		for r in data['data'].values():
			challenges.append(models.Challenge(time=float(unithelper.seconds(r['moving_time'])), distance=float(unithelper.miles(r['distance'])), athId=r['id']))

		break
		print len(challenges)
		time.sleep(TIME_BT_REQUESTS)
	return challenges
def getAthleteStats(challenges):
	client = stravalib.client.Client(access_token=config.TOKEN)
	for c in challenges:
		athStats=models.AthleteStats(client.get_athlete_stats(c.athId))
		if athStats.YTDCount > minNumberRuns:
			db.add(athId=c.athId,athStats=athStats)
			db.add(c)
			db.commit()
chall=getChallengeRuns()
getTrainingRuns(chall)

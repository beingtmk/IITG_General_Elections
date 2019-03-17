from apscheduler.schedulers.blocking import BlockingScheduler
import os
import time

def job():
	os.popen("./manage.py dumpdata general_elections.VotesUG general_elections.VotesPG > " "./database_backup/" + str(time.time()) + ".json")


scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval', minutes=10)
scheduler.start()

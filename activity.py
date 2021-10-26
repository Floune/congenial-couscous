from datetime import date, datetime
import time
import json
current = ""
start = ""
activities = {}

def maybeActivities():
	global activities
	today = date.today().strftime("%d-%m-%y")
	with open('excellentsystemededonnees2.json') as json_file:
		data = json.load(json_file)
		for d in data:
			if d["date"] == today:
				activities = d["activity"].copy()

	return activities


def newActivity(activity):
	global current
	global start
	current = activity[7:]
	start = time.localtime()
	if len(activities) < 12:
		activities[time.strftime("%H:%M", start)] = current
		payload = [{"date":date.today().strftime("%d-%m-%y"), "activity": activities}]
		with open('excellentsystemededonnees2.json', 'w') as outfile:
			json.dump(payload, outfile)
	

# def formatActivity(win, i, k, v):
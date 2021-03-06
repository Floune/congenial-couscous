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
		activities[time.strftime("%H:%M:%S", start)] = current
		payload = [{"date":date.today().strftime("%d-%m-%y"), "activity": activities}]
		with open('excellentsystemededonnees2.json', 'w') as outfile:
			json.dump(payload, outfile)
	


def trackDisplayLoop(win, activities):
	keys_list = list(activities)
	for i, (k, v) in enumerate(activities.items()):
		if i > 0:
			key = keys_list[i]
			previousKey = keys_list[i - 1]
			duree = datetime.strptime(key, '%H:%M:%S') - datetime.strptime(previousKey, '%H:%M:%S')
			win.addstr(i + 7, 0, "{}".format(activities[previousKey]))
			win.addstr(i + 7, 20, "{}".format(duree))
		else:
			win.addstr(i + 7, 0, "{} - début de journée sur {}".format(keys_list[i], activities[keys_list[i]]))
		win.refresh()

import mpv
import time

radios = {
  "metal": {
    "url": "http://radio.radiometal.com/radiometal.mp3",
    "commentaire": "metaaaal"
  },
  "nolife": {
    "url": "https://listen.nolife-radio.com/stream",
    "commentaire": "nolife"
  },
  "culture": {
    "url": "http://icecast.radiofrance.fr/franceculture-lofi.mp3",
    "commentaire": "la culture"
  },
}
radioCommands = ["metal", "culture", "nolife","stop"]

volume = 50
p = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True)

def setVolume(comment):
    global volume
    global p
    if comment == "u":
        if volume < 90:
            volume += 10
    if comment == "d":
        if volume > 10:
            volume -= 10        
    p.volume = volume
    return volume


def radioFrenezy(adresse, commentaire):
	global p
	global songTitle
	global alecoute
	alecoute = commentaire
	p.stop()
	# p.audio_set_volume(volume)
	p.play(adresse)
	time.sleep(3)
	if alecoute =="la culture" or alecoute =="plus rien":
		title = ""
	else:	
		title = p.metadata["icy-title"]
	return [alecoute, title]

def updateSongTitle():
	global p
	global songTitle
	if alecoute =="la culture" or alecoute =="plus rien":
		title = ""
	else:
		title = p.metadata["icy-title"]
	return title

def handleRadio(radio):
	global alecoute
	global volume
	if radio == "nolife":
		frenz = radioFrenezy(radios[radio]["url"], radios[radio]["commentaire"])
		alecoute = frenz[0]
		title = frenz[1]
	elif radio == "culture":
		frenz = radioFrenezy(radios[radio]["url"], radios[radio]["commentaire"])
		alecoute = frenz[0]
		title = frenz[1]
	elif radio == "metal":
		frenz = radioFrenezy(radios[radio]["url"], radios[radio]["commentaire"])
		alecoute = frenz[0]
		title = frenz[1]
	elif radio == "stop":
	    alecoute = "plus rien"
	    title = ""
	    p.stop()


	return [alecoute, title]

def handleVolume(vol):
	global volume
	volume = setVolume(vol)
	return volume
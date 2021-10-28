import mpv
import time

radios = {
  "metal": {
    "url": "http://radio.radiometal.com/radiometal.mp3",
    "commentaire": "metaaaal"
  },
  "nolife": {
    "url": "https://listen.nolife-radio.com/stream",
    "commentaire": "nolife mon gars"
  },
  "culture": {
    "url": "http://icecast.radiofrance.fr/franceculture-lofi.mp3",
    "commentaire": "la culture"
  },
}
volume = 50
p = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True)

def setVolume(comment):
    global volume
    global p
    if comment == "up":
        if volume < 90:
            volume += 10
    if comment == "down":
        if volume > 10:
            volume -= 10        
    # p.audio_set_volume(volume)
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
	if alecoute =="culture" or alecoute =="plus rien":
		title = ""
	else:	
		title = p.metadata["icy-title"]
	return [alecoute, title]


def handleRadio(radio):
	global alecoute
	global volume

	if radio == "u":
	    volume = setVolume("up")

	elif radio == "d":
	    volume = setVolume("down")

	elif radio == "stop":
	    alecoute = "plus rien"
	    p.stop()
	else:
		frenz = radioFrenezy(radios[radio]["url"], radios[radio]["commentaire"])
		alecoute = frenz[0]
		title = frenz[1]
	
	return [alecoute, volume, title]
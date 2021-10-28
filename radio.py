import vlc

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

alecoute = ""
p = vlc.MediaPlayer("https://listen.nolife-radio.com/stream")
volume = 50


def setVolume(comment):
    global volume
    global p
    if comment == "up":
        if volume < 90:
            volume += 10
    if comment == "down":
        if volume > 10:
            volume -= 10        
    p.audio_set_volume(volume)
    return volume


def radioFrenezy(adresse, commentaire):
	global p
	global alecoute
	p.stop()
	p = vlc.MediaPlayer(adresse)
	p.audio_set_volume(volume)
	p.play()
	alecoute = commentaire
	return alecoute


def handleRadio(radio):
	global alecoute
	global volume
	if radio == "nolife":
	    alecoute = radioFrenezy(radios[radio]["url"], radios[radio]["commentaire"])

	elif radio == "culture":
	    alecoute = radioFrenezy(radios[radio]["url"], radios[radio]["commentaire"])

	elif radio == "metal":
	    alecoute = radioFrenezy(radios[radio]["url"], radios[radio]["commentaire"])

	elif radio == "u":
	    volume = setVolume("up")

	elif radio == "d":
	    volume = setVolume("down")

	elif radio == "stop":
	    alecoute = "plus rien"
	    p.stop()
	return [alecoute, volume]
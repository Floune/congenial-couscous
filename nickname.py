import random

noms = [
    "marsouin",
    "poutrelle",
    "obama",
    "jambon de parme",
    "ascenceur",
    "hélicoptere",
    "ornithorynque",
    "personne",
    "zèbre",
    "oligarque",
    "assureur",
    "casque bleu",
    "guerrier massai",
    "agriculteur",
    "ministre",
    "alain finkielkraut",
    "chef de projet",
    "chevalier",
    "karatéka",
]

adjectifs = [
    "à la tête coupée",
    "illustre",
    "fragile",
    "sur le retour",
    "gras",
    "sans le sous",
    "russe",
    "à vapeur",
    "en bois",
    "en colere",
    "magenta",
    "impétueux",
    "à la mords moi le noeud",
    "sans foi ni loi",
    "à la fraise",
    "au fromage",
    "au chomage",
]

def randoum():
    nick = random.choice(noms) + " " + random.choice(adjectifs)
    return nick

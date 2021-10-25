import random

noms = [
    "marsouin",
    "poutrelle",
    "obama",
    "jambon de parme",
    "ascenceur",
    "helicoptere",
    "ornithorynque",
    "personne",
    "zebre",
    "oligarque",
    "assureur",
    "casque bleu",
    "guerrier massai"
    "agriculteur",
    "ministre",
    "alain finkielkraut",
    "chef de projet",
    "chevalier",
    "karateka",
]

adjectifs = [
    "a la tete coupee",
    "illustre",
    "fragile",
    "sur le retour",
    "gras",
    "sans le sous",
    "russe",
    "a vapeur",
    "en bois",
    "en colere",
    "magenta",
    "impetueux",
    "a la mords moi le noeud",
    "sans foi ni loi",
    "a la fraise",
    "au fromage",
    "au chomage",
]

def randoum():
    nick = random.choice(noms) + " " + random.choice(adjectifs)
    return nick

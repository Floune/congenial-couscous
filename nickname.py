import random

noms = [
    "marsouin",
    "poutrelle",
    "jambon de parme",
    "ascenceur",
    "helicoptere",
    "ornithorynque",
    "personne",
    "zebre",
    "agriculteur",
    "ministre",
    "chef de projet",
    "chevalier",
    "karateka",
]

adjectifs = [
    "a la tete coupee",
    "illustre",
    "fragile",
    "a vapeur",
    "en bois",
    "en colere",
    "impetueux",
    "a la mords moi le noeud",
    "sans foi ni loi",
    "a la fraise",
    "magenta",
    "au chomage",
    "au fromage",
]

def randoum():
    nick = random.choice(noms) + " " + random.choice(adjectifs)
    return nick

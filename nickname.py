import random

noms = [
    "marsouin",
    "poutrelle",
    "obama",
    "gros batard",
    "jambon de parme",
    "ascenceur",
    "hélicoptere",
    "ornithorynque",
    "personne",
    "politicien",
    "géologue",
    "zèbre",
    "oligarque",
    "papou",
    "assureur",
    "casque bleu",
    "guerrier massaï",
    "banjo",
    "gilet jaune",
    "agriculteur",
    "ministre",
    "mehdi",
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
    "à voile et à vapeur",
    "en bois",
    "en colere",
    "magenta",
    "itinérant",
    "aigri",
    "avec des frites à 14€90",
    "qui pue la merde",
    "impétueux",
    "à la mords-moi-le-noeud",
    "sans foi ni loi",
    "un peu perdu(e)",
    "au fromage",
    "au chomage",
]

def randoum():
    nick = random.choice(noms) + " " + random.choice(adjectifs)
    return nick

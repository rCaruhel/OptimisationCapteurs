import sys
import re
import numpy as np

if len(sys.argv)!=2:
    print("Ajouter le fichier d'entrée")

## Division ouverture du fichier et division du texte par lignes
fileText = open(sys.argv[1]).read()
fileTextTable = fileText.split("\n")

nbrCapteurs = fileTextTable[0]
nbrZones = fileTextTable[1]
dureesDeVie = fileTextTable[2].split(" ")

## récupération des éléments du 4ᵉ jusqu'au dernier
zonesCouvertesParCapteurs = fileTextTable[3:]

if len(dureesDeVie) != int(nbrCapteurs):
    print("les durées de vie ne correspondent pas au nombre de capteurs")

if len(zonesCouvertesParCapteurs) != int(nbrCapteurs):
    print("Mauvaises données d'entrée, pas assez de lignes pour les données d'entrée")

if all(int(n) <= int(nbrZones) for n in re.findall(r'\d+', fileText)):
    print("Le fichier possède des zones n'ayant pas été indiquées dans la deuxième ligne de l'entrée")


coveredZones = []

for zonesParCapteur in zonesCouvertesParCapteurs:
    zones = []
    """
    construction d'un tableau à partir des données de zones couvertes par capteur
    1 2
    2 3
    3
    1 3

    Donne

    1 1 0
    0 1 1
    0 0 1
    1 0 1
    """
    for i in range (int(nbrCapteurs)-1):
        if str(i+1) not in zonesParCapteur:
            zones.append(0)
        else :
            zones.append(1)
    coveredZones.append(zones)

print(coveredZones)

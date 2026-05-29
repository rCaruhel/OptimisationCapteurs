import sys
import re
import numpy as np

if len(sys.argv)!=2:
    print("Mauvaises entrées, il faut un unique argument : le chemin vers le fichier d'entrée")

############# Récupération des données du fichier

## Division ouverture du fichier et division du texte par lignes
fileText = open(sys.argv[1]).read()
fileTextTable = fileText.split("\n")

nbrCapteurs = int(fileTextTable[0])
nbrZones = int(fileTextTable[1])
dureesDeVie = fileTextTable[2].split(" ")

## récupération des éléments du 4ᵉ jusqu'au dernier
zonesCouvertesParCapteurs = fileTextTable[3:]

if len(dureesDeVie) != nbrCapteurs:
    print("les durées de vie ne correspondent pas au nombre de capteurs")

if len(zonesCouvertesParCapteurs) != nbrCapteurs:
    print("Mauvaises données d'entrée, pas assez de lignes pour les données d'entrée")

if all(int(n) <= int(nbrZones) for n in re.findall(r'\d+', fileText)):
    print("Le fichier possède des zones n'ayant pas été indiquées dans la deuxième ligne de l'entrée")



############# Construction de la matrice permettant de construire les solutions élémentaires
coveredZones = []
capteurActuel = 1
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
    for i in range (nbrCapteurs-1):
        if str(i+1) not in zonesParCapteur:
            zones.append(0)
        else :
            zones.append(1)
    coveredZones.append(zones)

coveredZones = np.array(coveredZones)

############# Construction de chacune des solutions valides
conbinaisonCapteursValides = []
for i in range (2**nbrCapteurs):
    combinaison = []
    """
    Phase de récupération de toutes les combinaisons de capteurs 
    """
    capteursChecked = []
    binarySolver = f"{i:0{nbrCapteurs}b}"[::-1]
    for j in range(nbrCapteurs):
        valueChecked = binarySolver[j]
        if binarySolver[j]=='1':
            combinaison.append(coveredZones[j])
            capteursChecked.append(j)



    # initialisation d'un tableau rempli de zéros, il représente les zones couvertes par combinaison de capteurs
    zonesCoveredByCapteur = np.zeros(nbrZones)
    for comb in combinaison:
        zonesCoveredByCapteur += np.array(comb)


    isCombinaisonValid = True
    isElementaire = True
    # on regarde si une zone n'est pas couverte par la combinaison de capteurs
    for zone in zonesCoveredByCapteur:
        if zone == 0:
            isCombinaisonValid = False

    if isCombinaisonValid:
        conbinaisonCapteursValides.append(capteursChecked)



# on trie par longueur croissante
listes_triees = sorted(conbinaisonCapteursValides, key=len)
combinaisonsElementaires = []

# parcours et vérification
for element in listes_triees:
    ensemble_actuel = set(element)

    # On vérifie si un des éléments déjà gardés est inclus dans l'élément actuel
    est_contenu = any(set(deja_garde).issubset(ensemble_actuel) for deja_garde in combinaisonsElementaires)

    # Si aucun sous-ensemble n'est trouvé à l'intérieur, on le garde
    if not est_contenu:
        combinaisonsElementaires.append(element)

print(combinaisonsElementaires)

### À présent, on possède les combinaisons élémentaires, on les gardera pour la suite de l'exercice


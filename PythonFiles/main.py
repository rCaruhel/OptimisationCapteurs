import sys
import re
import numpy as np
import pulp

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

    # construction d'un tableau binaire à partir des données de zones couvertes par capteur
    """
    EXEMPLE : 
    Les données représentent les zones couvertes par chaque capteur 
    dans l'exemple suivant, le capteur 1 couvre les zones 1 et 2, le capteur 3 les zones 2 et 3...
    
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
    zones_list = zonesParCapteur.split()
    for i in range (nbrZones):
        if str(i+1) not in zones_list:
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

#print(combinaisonsElementaires)

### À présent, on possède les combinaisons élémentaires, on les gardera pour la suite de l'exercice
'''
EXEMPLE : 
Avec les combinaisons élémentaires 
u0 : [0, 1], 
u1 : [0, 2], 
u2 : [0, 3], 
u3 : [1, 3]

Et les durées de vie des capteurs
CO : 6
C1 : 3
C2 : 2
C3 : 6

On construit le fichier GLPK pour obtenir le temps max "tui" de chaque zone i, pour maximiser les tui

on maximise tu0 + tu1 + tu2 + tu3
avec 
tu0 + tu1 + tu2 <= 6
tu0 + tu3 <= 3
tu1 <= 2
tu2 + tu3 <= 6
'''
#### Utilisation de pulp, solveur GLPK

problem = pulp.LpProblem("Maximisation",pulp.LpMaximize)
variablesTemps = [[] for _ in range(nbrCapteurs)]


for i,comb in enumerate(combinaisonsElementaires):
    for value in comb:
        variablesTemps[value].append(i)

# Création d'un dictionnaire de variables : t[0], t[1], t[2]...
# lowBound=0 car un temps ne peut pas être négatif
t = {u: pulp.LpVariable(f"tu{u}", lowBound=0) for u in range(len(combinaisonsElementaires))}

problem += pulp.lpSum(t[u] for u in range(len(combinaisonsElementaires))), "Maximisation_Temps_Total"

for capteur in range(nbrCapteurs):
    # On récupère la durée de vie du capteur actuel
    limite = int(dureesDeVie[capteur])
    indices_combinaisons = variablesTemps[capteur]
    contrainte_ligne = pulp.lpSum(t[u] for u in indices_combinaisons)

    # On ajoute la contrainte au problème
    problem += (contrainte_ligne <= limite, f"Contrainte_Capteur_{capteur}")

problem.solve(pulp.GLPK_CMD(msg=True))

for capteur in range(len(combinaisonsElementaires)):
    print(f"Capteur{capteur+1} : {t[capteur].varValue}")
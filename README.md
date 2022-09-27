![alt text](https://github.com/metabolean5/betbots/blob/main/bot_pics/betbot.png?raw=true)

# betbots
Multiplex de paris footballistiques automatisés.

## Présentation

Turfutoday's betbots est un projet open source sur lequel nous uploadons des robots qui parient sur matchs de football.
La ligue en question est la deuxième division du football français que nous estimons de loin comme la plus fraiches et hypé du moment depart sa production absolument fantasque de frustrations et d'emmerdes sportives.
Nos yeux étaient pourtant fixé sur la ligue national (division 3) du faitt de la forme primitive de son football qui donne lieu à des résultat d'ordre baroque.
Cette ligue étant toutefois très peu populaire, il se trouve qu'il est actuellement très difficile de trouver les datsets dont nous avons besoins pour effectuer les paris automatiques.

##Robots

Les robots actuels utilisent sur des stratégies qui ne demandent que à être pefectionnée ou alors radicalement transformées. 
Tout les robts, mis à part Pat Nostat, utilisent un algorithmes d'apprebtissage statistiques rudimentaires pour effectuer leur predictions.
Bien que la modélisation et l'apprentissage machine soient des domaines plus que fascinants, elle n'est d'aucune importance ici puisque nous jouons à un jeu de hasard.
Les stratégies sont donc les seules parties qui nous interessent. Par exemple, les robots Vent d'ofsky utilisent des parites combinés et nous paraissent comme étant très prométeurs.
Pour le reste nous vous renvoyons vers le code.

##Données pour les paris

Le futurs dev doit se référer aux deux méthodes de l'objet Betbot place_bets(self) apply_strategy(self,y_predictions, proba) pour y faire ses implémentations.
Le paramètre principal y_predictions est un vecteur conenant les informations des matchs et les predictions du modèles, c'est tout ce dont les robots actuels ont besoin pour mettre en place leur statégie.

```
{'teams': 'PSGPSG-NiceNIC', 'date': 'Ligue 1 | Round 9'}, 'last5vec': [3, 3, 3, 3, 3, 0, 1, 3, 1, 0]}, {'cotes': {'3': '2.50', '1': '3.75', '0': '2.50'}

array([[0.07342209, 0.14820677, 0.77837113],
       [0.22416424, 0.13586867, 0.63996709]]) //proba pour deux matchs (droite : victoire, centre : nul, gauche : défaite)

```
##Saison 1 



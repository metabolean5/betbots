![alt text](https://github.com/metabolean5/betbots/blob/main/bot_pics/betbot.png?raw=true)

# betbots
Multiplex de paris footballistiques automatisés.

## Présentation

Turfutoday's betbots est un projet open source sur lequel nous uploadons des robots qui parient sur des matchs de football.
La ligue en question est la deuxième division du football français que nous estimons de loin comme la plus fraîche et hypée de par sa production absolument fantasque de frustrations.
Nos yeux étaient pourtant rivés sur la ligue national (division 3) du fait de la forme primitive de son football qui donne lieu à des résultats d'ordre baroque.
Cette ligue étant toutefois très peu populaire, il se trouve qu'il est actuellement impossible de trouver les datasets dont nous avons besoin pour effectuer les paris automatiques sur ce championnat.


## Robots

Les robots actuels utilisent des stratégies qui ne demandent qu'à être perfectionnées ou alors radicalement transformées. 
Tous les robots, mis à part Pat Nostat, utilisent un algorithme d'apprentissage statistique rudimentaire pour effectuer leur prédiction.
Bien que la modélisation et l'apprentissage machine soient des domaines plus que fascinants, elle n'est d'aucune importance ici puisque nous jouons à un jeu de hasard.
Les stratégies sont donc les seules parties qui nous intéressent. Par exemple, les robots Vent d'ofsky utilisent des parties combinées et nous paraissent comme étant très prometteurs.
Pour le reste nous vous renvoyons vers le code.


## Données pour les paris

Le futur dev doit se référer aux deux méthodes de l'objet Betbot place_bets(self) apply_strategy(self,y_predictions, proba) pour y faire ses implémentations.
Le paramètre principal y_predictions est un vecteur contenant les informations des matchs et les prédictions du modèles, c'est tout ce dont les robots actuels ont besoin pour mettre en place leur stratégie.


```
{'teams': 'PSGPSG-NiceNIC', 'date': 'Ligue 1 | Round 9'}, 'last5vec': [3, 3, 3, 3, 3, 0, 1, 3, 1, 0]}, {'cotes': {'3': '2.50', '1': '3.75', '0': '2.50'}

array([[0.07342209, 0.14820677, 0.77837113],
       [0.22416424, 0.13586867, 0.63996709]]) //proba pour deux matchs (droite : victoire, centre : nul, gauche : défaite)

```
## Prochain Paris (Journée du 6 Octobre 2022)

![alt text](https://github.com/metabolean5/betbots/blob/main/bot_pics/curr_stats.png?raw=true)


## Archives

# Saison 1

La saison 1 fut évidemment haute en couleur. Ce fut en toute évidence le moment ultime de la création, de l'engendrement de la forme à partir du de chaos que sont les paris sportifs.

L'apparition progressive de Risky Rifky, de Pat et des Vents d'Ofsky ont marqué une sorte d'âge d'or qui se présente seulement sous la forme de Commencements. Nous avons cela dit la foi du renouveau et du devenir, du duende fougueux de l'anarchie ontologique qui nous surprend et sur lequel nous jouissons de nos outputs => turfutodays's betbots 100 seasons, turfutodays's betbots a 100 years.

**Graphe évolutions**
![alt text](https://github.com/metabolean5/betbots/blob/main/bot_pics/wallstats.png?raw=true)

**Classement S1**
![alt text](https://github.com/metabolean5/betbots/blob/main/bot_pics/class.png?raw=true)









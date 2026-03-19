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
Tous les robots, mis à part Pat Nostat et Way to Claude, utilisent un algorithme d'apprentissage statistique rudimentaire pour effectuer leur prédiction.
Bien que la modélisation et l'apprentissage machine soient des domaines plus que fascinants, elle n'est d'aucune importance ici puisque nous jouons à un jeu de hasard.
Les stratégies sont donc les seules parties qui nous intéressent. Par exemple, les robots Vent d'ofsky utilisent des parties combinées et nous paraissent comme étant très prometteurs.
Pour le reste nous vous renvoyons vers le code.

| Avatar | # | Nom | Modèle | Stratégie |
|---|---|---|---|---|
| <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="60"> | 01 | Billy Bayes | SKLearn | Parie sur les sorties à haute confiance (>60%) |
| <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="60"> | 02 | Risky Rifki | SKLearn | Parie à contre-courant sur les sorties peu probables (<45%) |
| <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="60"> | 03 | Pat Nostat | — | Différentiel de forme brute entre les deux équipes |
| <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="60"> | 04 | Risky Vent d'Ofsky | — | Combiné avec cotes < 1.65 |
| <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="60"> | 05 | Vent d'Ofsky | — | Combiné sélectif avec cotes < 1.50 |
| <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="60"> | 06 | **Way to Claude** | — | **Paris à valeur positive (EV ≥ 20%)** — mise Kelly-inspirée |

### Way to Claude — fonctionnement détaillé

Le modèle estime les probabilités réelles d'un match à partir des vecteurs de forme des 5 derniers matchs :

```
P(victoire dom.) = clip(0.40 + diff_forme × 0.25,  0.05, 0.85)
P(victoire ext.) = clip(0.35 − diff_forme × 0.25,  0.05, 0.85)
P(nul)           = 1 − P(dom.) − P(ext.)
diff_forme       = (forme_dom − forme_ext) / 15     # ∈ [−1, +1]
```

Il calcule ensuite l'**espérance de valeur** (EV) pour chaque issue :

```
EV = P(issue) × cote − 1
```

Un pari n'est validé que si max(EV) ≥ 0.20. La mise suit une grille Kelly-inspirée :

```
EV ≥ 0.60  →  €50
EV ≥ 0.25  →  €35
EV ≥ 0.20  →  €20
```


## Données pour les paris

Le futur dev doit se référer aux deux méthodes de l'objet Betbot place_bets(self) apply_strategy(self,y_predictions, proba) pour y faire ses implémentations.
Le paramètre principal y_predictions est un vecteur contenant les informations des matchs et les prédictions du modèles, c'est tout ce dont les robots actuels ont besoin pour mettre en place leur stratégie.


```
{'teams': 'PSGPSG-NiceNIC', 'date': 'Ligue 1 | Round 9'}, 'last5vec': [3, 3, 3, 3, 3, 0, 1, 3, 1, 0]}, {'cotes': {'3': '2.50', '1': '3.75', '0': '2.50'}

array([[0.07342209, 0.14820677, 0.77837113],
       [0.22416424, 0.13586867, 0.63996709]]) //proba pour deux matchs (droite : victoire, centre : nul, gauche : défaite)

```

## Classement Saison 3

> UCL R16 (10–18 mars 2026) + mode week-end (EPL / Ligue 1). UEL/UECL non vérifiables via l'API gratuite.

| Rang | Bot | Net total | Paris ✅ | Paris ❌ | ROI |
|------|-----|-----------|---------|---------|-----|
| 🥇 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="30"> **Billy Bayes** | **€+110.95** | 5 | 0 | +158% |
| 🥈 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="30"> **Risky Rifki** | **€+98.25** | 3 | 2 | +98% |
| 🥉 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="30"> **Way to Claude** | **€+43.00** | 3 | 8 | +17% |
| #4 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="30"> **Vent d'Ofsky** | **€+22.59** | 1 | 0 | +113% |
| #5 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="30"> **Pat Nostat** | **€-19.40** | 2 | 1 | -39% |
| #6 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="30"> **Risky Vent d'Ofsky** | **€-30.00** | 0 | 2 | -100% |

> Week-end 13–16/03 : Bournemouth vs Manchester United (20/03) remboursé — match trop tardif.

---

## Paris en cours — Week-end 20–22 mars 2026 (EPL / Ligue 1)

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
Aucun pari ce week-end.

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
| Match | Date | Pronostic | Mise | Gain potentiel |
|---|---|---|---|---|
| Bournemouth vs Manchester United | 20/03 20:00 | **Home Win** @3.32 | €25 | +€83.00 |
| Toulouse vs Lorient | 21/03 16:00 | **Away Win** @4.72 | €25 | +€118.00 |
| Auxerre vs Brest | 21/03 18:00 | **Home Win** @2.38 | €25 | +€59.50 |
| Leeds United vs Brentford | 21/03 20:00 | **Home Win** @2.51 | €25 | +€62.75 |
| Nice vs Paris Saint Germain | 21/03 20:00 | **Draw** @5.82 | €25 | +€145.50 |
| Nantes vs Strasbourg | 22/03 19:45 | **Away Win** @2.03 | €25 | +€50.75 |
| Tottenham Hotspur vs Nottingham Forest | 22/03 14:15 | **Home Win** @2.29 | €25 | +€57.25 |

Mise totale : **€175** — Gain potentiel cumulé : **€576.75**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Date | Pronostic | Mise | Gain potentiel |
|---|---|---|---|---|
| Auxerre vs Brest | 21/03 18:00 | **Away Win** @3.24 | €10 | +€32.40 |

Mise totale : **€10**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Date | Pronostic |
|---|---|---|
| Fulham vs Burnley | 21/03 15:00 | **Home Win** @1.57 |
| Nice vs Paris Saint Germain | 21/03 20:00 | **Away Win** (PSG) @1.35 |
| Everton vs Chelsea | 21/03 17:30 | **Home Win** |
| Newcastle United vs Sunderland | 22/03 12:00 | **Home Win** |

Mise : **€15** — Gain potentiel combiné : **€56.62**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky (combiné)
| Match | Date | Pronostic |
|---|---|---|
| Nice vs Paris Saint Germain | 21/03 20:00 | **Away Win** (PSG) @1.35 |
| Everton vs Chelsea | 21/03 17:30 | **Home Win** |
| Newcastle United vs Sunderland | 22/03 12:00 | **Home Win** |

Mise : **€20** — Gain potentiel combiné : **€48.09**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Date | Pronostic | EV | Mise | Gain potentiel |
|---|---|---|---|---|---|
| Fulham vs Burnley | 21/03 15:00 | **Away Win** (Burnley) @6.14 | 0.944 | €50 | +€307.00 |
| Toulouse vs Lorient | 21/03 16:00 | **Away Win** (Lorient) @4.72 | 1.045 | €50 | +€236.00 |
| Everton vs Chelsea | 21/03 17:30 | **Home Win** (Everton) @3.56 | 0.602 | €50 | +€178.00 |
| Auxerre vs Brest | 21/03 18:00 | **Away Win** (Brest) @3.24 | 0.404 | €35 | +€113.40 |
| Nice vs Paris Saint Germain | 21/03 20:00 | **Home Win** (Nice) @8.00 | 1.400 | €50 | +€400.00 |
| Newcastle United vs Sunderland | 22/03 12:00 | **Away Win** (Sunderland) @5.38 | 0.614 | €50 | +€269.00 |
| Paris FC vs Le Havre | 22/03 16:15 | **Away Win** (Le Havre) @4.44 | 0.406 | €35 | +€155.40 |
| Marseille vs Lille | 22/03 16:15 | **Away Win** (Lille) @3.91 | 0.434 | €35 | +€136.85 |
| Nantes vs Strasbourg | 22/03 19:45 | **Home Win** (Nantes) @3.66 | 0.220 | €20 | +€73.20 |

Mise totale : **€375** — Gain potentiel cumulé : **€1 869.85**

<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
<br/>Turfutodays's betbots is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">Attribution-ShareAlike 2.0 France (CC BY-SA 2.0 FR)</a>.

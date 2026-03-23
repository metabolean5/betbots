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

| Rang | Bot | Net total | Paris ✅ | Paris ❌ | Total |
|------|-----|-----------|---------|---------|-------|
| 🥇 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="30"> **Way to Claude** | **€+177.80** | 8 | 21 | 29 |
| 🥈 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="30"> **Billy Bayes** | **€+101.15** | 6 | 1 | 7 |
| 🥉 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="30"> **Risky Rifki** | **€+53.50** | 6 | 9 | 15 |
| #4 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="30"> **Vent d'Ofsky** | **€-17.41** | 1 | 2 | 4 |
| #5 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="30"> **Pat Nostat** | **€-39.40** | 2 | 3 | 5 |
| #6 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="30"> **Risky Vent d'Ofsky** | **€-60.00** | 0 | 4 | 7 |

> Week-end 20–22/03 : Bournemouth vs Manchester United remboursé (match reporté).

---

## Paris — WCQ Europe (Playoffs, 26 mars 2026)

> Qualifications Coupe du Monde 2026 – Demi-finales playoffs UEFA. Données scrappées via l'API Sportradar gismo.

### Programme du 26 mars 2026

| Heure | Match | Stade |
|---|---|---|
| 18:00 | Turkiye vs Romania | Tupras Stadium, Istanbul |
| 20:45 | Wales vs Bosnia and Herzegovina | Cardiff City Stadium, Cardiff |
| 20:45 | Poland vs Albania | National Stadium Warsaw, Varsovie |
| 20:45 | Slovakia vs Kosovo | Tehelne Pole Stadion, Bratislava |
| 20:45 | Czechia vs Ireland | Fortuna Arena, Prague |
| 20:45 | Italy vs Northern Ireland | Gewiss Stadium, Bergame |
| 20:45 | Ukraine vs Sweden | Ciutat de Valencia, Valence |
| 20:45 | Denmark vs North Macedonia | Parken Stadium, Copenhague |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
| Match | Pronostic | Cote | Gain potentiel |
|---|---|---|---|
| Italy vs Northern Ireland | **Italy W** | @1.33 | +€46.55 |
| Ukraine vs Sweden | **Ukraine W** | @3.07 | +€107.45 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
| Match | Pronostic | Cote | Gain potentiel |
|---|---|---|---|
| Czechia vs Ireland | **Czechia W** | @2.03 | +€50.75 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Pronostic | Cote | Gain potentiel |
|---|---|---|---|
| Ukraine vs Sweden | **Ukraine W** | @3.07 | +€30.70 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Pronostic | Cote |
|---|---|---|
| Turkiye vs Romania | Turkiye W | @1.40 |
| Italy vs Northern Ireland | Italy W | @1.33 |
| Denmark vs North Macedonia | Denmark W | @1.36 |

Gain potentiel combiné : **+€37.98**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky (combiné)
| Match | Pronostic | Cote |
|---|---|---|
| Turkiye vs Romania | Turkiye W | @1.40 |
| Italy vs Northern Ireland | Italy W | @1.33 |
| Denmark vs North Macedonia | Denmark W | @1.36 |

Gain potentiel combiné : **+€50.65**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Pronostic | EV estimé | Mise | Gain potentiel |
|---|---|---|---|---|
| Turkiye vs Romania | **Romania W** | — | €50 | +€330 |
| Wales vs Bosnia and Herzegovina | **Bosnia W** | — | €35 | +€148.75 |
| Poland vs Albania | **Albania W** | — | €50 | +€297 |
| Slovakia vs Kosovo | **Kosovo W** | — | €35 | +€145.60 |
| Czechia vs Ireland | **Ireland W** | — | €35 | +€145.60 |
| Italy vs Northern Ireland | **Northern Ireland W** | — | €50 | +€620 |
| Ukraine vs Sweden | **Ukraine W** | — | €50 | +€153.50 |
| Denmark vs North Macedonia | **North Macedonia W** | — | €50 | +€530 |

> Way to Claude joue tous les outsiders (sauf Ukraine) — stratégie contrariante maximale.

---

## Résultats — Week-end 20–22 mars 2026 (EPL / Ligue 1)

### Résultats des matchs

| Match | Score | Résultat |
|---|---|---|
| RC Lens vs Angers | — | — |
| Bournemouth vs Manchester United | — | **Reporté** |
| Fulham vs Burnley | 3–1 | Victoire Fulham |
| Everton vs Chelsea | 3–0 | Victoire Everton |
| Leeds United vs Brentford | 0–0 | Nul |
| Toulouse vs Lorient | 1–0 | Victoire Toulouse |
| Auxerre vs Brest | 3–0 | Victoire Auxerre |
| Nice vs Paris Saint-Germain | 0–4 | Victoire PSG |
| Newcastle United vs Sunderland | 1–2 | **Victoire Sunderland** (surprise) |
| Tottenham Hotspur vs Nottingham Forest | 0–3 | Victoire Nottingham Forest |
| Paris FC vs Le Havre | 3–2 | Victoire Paris FC |
| Marseille vs Lille | 1–2 | Victoire Lille |
| Nantes vs Strasbourg | 2–3 | Victoire Strasbourg |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
Aucun pari ce week-end.

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
| Match | Pronostic | Résultat | Gain |
|---|---|---|---|
| Bournemouth vs Manchester United | Home Win @3.32 | Reporté | €+25 (remb.) |
| Auxerre vs Brest | **Home Win** @2.38 | ✅ Auxerre 3–0 | **+€59.50** |
| Nantes vs Strasbourg | **Away Win** @2.03 | ✅ Nantes 2–3 | **+€50.75** |
| Leeds United vs Brentford | Home Win @2.51 | ❌ 0–0 | -€25 |
| Tottenham vs Nottingham Forest | Home Win @2.29 | ❌ 0–3 | -€25 |
| Toulouse vs Lorient | Away Win @4.72 | ❌ 1–0 | -€25 |
| Nice vs Paris Saint Germain | Draw @5.82 | ❌ 0–4 | -€25 |

Bilan week-end : **2✅ 4❌** — **€-44.75**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Pronostic | Résultat | Gain |
|---|---|---|---|
| Auxerre vs Brest | Away Win @3.24 | ❌ 3–0 | -€10 |

Bilan week-end : **0✅ 1❌** — **€-10**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Pronostic | Résultat |
|---|---|---|
| Fulham vs Burnley | Home Win @1.57 | ✅ 3–1 |
| Nice vs PSG | Away Win (PSG) @1.35 | ✅ 0–4 |
| Everton vs Chelsea | Home Win @3.56 | ✅ 3–0 |
| Newcastle vs Sunderland | **Home Win** @1.67 | ❌ 1–2 |

Combiné **PERDU** (Sunderland upset Newcastle) — **€-15**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky (combiné)
| Match | Pronostic | Résultat |
|---|---|---|
| Nice vs PSG | Away Win (PSG) @1.35 | ✅ 0–4 |
| Everton vs Chelsea | Home Win @3.56 | ✅ 3–0 |
| Newcastle vs Sunderland | **Home Win** @1.67 | ❌ 1–2 |

Combiné **PERDU** (Sunderland upset Newcastle) — **€-20**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Pronostic | EV | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Everton vs Chelsea | **Home Win** (Everton) @3.56 | 0.602 | €50 | ✅ 3–0 | **+€178.00** |
| Newcastle vs Sunderland | **Away Win** (Sunderland) @5.38 | 0.614 | €50 | ✅ 1–2 | **+€269.00** |
| Marseille vs Lille | **Away Win** (Lille) @3.91 | 0.434 | €35 | ✅ 1–2 | **+€136.85** |
| Fulham vs Burnley | Away Win (Burnley) @6.14 | 0.944 | €50 | ❌ 3–1 | -€50 |
| Toulouse vs Lorient | Away Win (Lorient) @4.72 | 1.045 | €50 | ❌ 1–0 | -€50 |
| Auxerre vs Brest | Away Win (Brest) @3.24 | 0.404 | €35 | ❌ 3–0 | -€35 |
| Nice vs PSG | Home Win (Nice) @8.00 | 1.400 | €50 | ❌ 0–4 | -€50 |
| Paris FC vs Le Havre | Away Win (Le Havre) @4.44 | 0.406 | €35 | ❌ 3–2 | -€35 |
| Nantes vs Strasbourg | Home Win (Nantes) @3.66 | 0.220 | €20 | ❌ 2–3 | -€20 |

Bilan week-end : **3✅ 6❌** — **+€134.80** (Newcastle/Sunderland upset = jackpot)

<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
<br/>Turfutodays's betbots is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">Attribution-ShareAlike 2.0 France (CC BY-SA 2.0 FR)</a>.

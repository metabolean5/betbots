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

> UCL R16 (10–18 mars 2026) + mode week-end (EPL / Ligue 1) + WCQ Europe playoffs (26 et 31 mars 2026). UEL/UECL non vérifiables via l'API gratuite.

| Rang | Bot | Net total | Paris ✅ | Paris ❌ | Total |
|------|-----|-----------|---------|---------|-------|
| 🥇 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="30"> **Way to Claude** | **€+404.65** | 12 | 29 | 41 |
| 🥈 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="30"> **Risky Rifki** | **€+79.25** | 7 | 10 | 17 |
| 🥉 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="30"> **Billy Bayes** | **€+77.70** | 7 | 2 | 9 |
| #4 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="30"> **Vent d'Ofsky** | **€+13.24** | 3 | 2 | 5 |
| #5 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="30"> **Risky Vent d'Ofsky** | **€-52.02** | 1 | 5 | 9 |
| #6 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="30"> **Pat Nostat** | **€-59.40** | 2 | 5 | 7 |

> WCQ 26/03 : Way to Claude Kosovo ✅ + Bosnia ✅ (-€60.65). Risky Rifki Czechia ✅ (+€25.75). Les combinés Turkiye+Italy+Denmark gagnent pour les Vent d'Ofsky. WCQ 31/03 : Way to Claude joue les qualifiés Bosnia ✅ (+€317.50) et Czechia ✅ (+€140.00) — remonte en tête.

---

## Paris — WCQ Europe (Finales Playoffs, 31 mars 2026)

> Qualifications Coupe du Monde 2026 – Finales playoffs UEFA. Données scrappées via `betting_arena_wcq.py`.

### Programme du 31 mars 2026

| Heure | Match | Cotes (dom / nul / ext) |
|---|---|---|
| 20:45 | Bosnia and Herzegovina vs Italy | @6.35 / @3.78 / @1.64 |
| 20:45 | Sweden vs Poland | @2.02 / @3.37 / @3.47 |
| 20:45 | Kosovo vs Turkiye | @4.10 / @3.75 / @1.92 |
| 20:45 | Czechia vs Denmark | @4.00 / @3.38 / @2.06 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
Aucun pari ce round (aucune prédiction ne dépasse le seuil de confiance de 60%).

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Bosnia and Herzegovina vs Italy | **Italy W** | @1.64 | €25 | €41.00 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Sweden vs Poland | **Poland W** | @3.47 | €10 | €34.70 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Pronostic | Cote |
|---|---|---|
| Bosnia and Herzegovina vs Italy | Italy W | @1.64 |

Mise combinée : **€15** — Gain potentiel : **€24.60**

> Seule Italy @1.64 passe le seuil < 1.65.

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky
Aucun pari ce round (aucune cote ne passe le seuil < 1.50).

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Bosnia and Herzegovina vs Italy | **Bosnia W** | @6.35 | €50 | €317.50 |
| Sweden vs Poland | **Poland W** | @3.47 | €50 | €173.50 |
| Kosovo vs Turkiye | **Kosovo W** | @4.10 | €35 | €143.50 |
| Czechia vs Denmark | **Czechia W** | @4.00 | €35 | €140.00 |

> Way to Claude joue les 4 outsiders à domicile — stratégie EV contrariante.

---

## Paris — Week-end 3–5 avril 2026 (Ligue 1)

> Données scrappées via `betting_arena_weekend.py`. Pas de fixtures EPL ce week-end.

### Programme

| Date | Match | Cotes (dom / nul / ext) |
|---|---|---|
| Ven 03/04 18:45 | Paris Saint Germain vs Toulouse | @1.32 / @5.88 / @11.40 |
| Sam 04/04 15:00 | Strasbourg vs Nice | @1.90 / @3.76 / @4.47 |
| Sam 04/04 17:00 | Brest vs Rennes | @3.21 / @3.64 / @2.33 *(sans forme)* |
| Sam 04/04 19:05 | Lille vs RC Lens | @2.75 / @3.43 / @2.77 |
| Dim 05/04 13:00 | Angers vs Lyon | @4.88 / @3.67 / @1.86 *(sans forme)* |
| Dim 05/04 15:15 | Le Havre vs Auxerre | @2.53 / @3.23 / @3.23 |
| Dim 05/04 15:15 | Lorient vs Paris FC | @2.38 / @3.37 / @3.35 |
| Dim 05/04 15:15 | Metz vs Nantes | @3.07 / @3.38 / @2.54 *(sans forme)* |
| Dim 05/04 18:45 | AS Monaco vs Marseille | @2.29 / @3.75 / @3.21 *(sans forme)* |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Paris Saint Germain vs Toulouse | **PSG W** | @1.32 | €35 | €46.20 |
| Strasbourg vs Nice | **Strasbourg W** | @1.90 | €35 | €66.50 |
| Lille vs RC Lens | **Lille W** | @2.75 | €35 | €96.25 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Le Havre vs Auxerre | **Nul** | @3.23 | €25 | €80.75 |
| Lorient vs Paris FC | **Paris FC W** | @3.35 | €25 | €83.75 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
Aucun pari ce week-end.

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Pronostic | Cote |
|---|---|---|
| Paris Saint Germain vs Toulouse | PSG W | @1.32 |

Mise combinée : **€15** — Gain potentiel : **€19.80**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky (combiné)
| Match | Pronostic | Cote |
|---|---|---|
| Paris Saint Germain vs Toulouse | PSG W | @1.32 |

Mise combinée : **€20** — Gain potentiel : **€26.40**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Paris Saint Germain vs Toulouse | **Toulouse W** | @11.40 | €50 | €570.00 |
| Lille vs RC Lens | **Lille W** | @2.75 | €35 | €96.25 |
| Le Havre vs Auxerre | **Auxerre W** | @3.23 | €35 | €113.05 |
| Lorient vs Paris FC | **Paris FC W** | @3.35 | €35 | €117.25 |

> Way to Claude joue Toulouse à @11.40 (EV=2.04) — paris contrarian maximal contre le leader PSG.

---

## Résultats — WCQ Europe (Finales Playoffs, 31 mars 2026)

### Résultats des matchs

| Heure | Match | Score | Résultat |
|---|---|---|---|
| 20:45 | Bosnia and Herzegovina vs Italy | **1–1** | Nul — Bosnia qualifiée (pen. 4–1) |
| 20:45 | Sweden vs Poland | **3–2** | Victoire Sweden |
| 20:45 | Kosovo vs Turkiye | **0–1** | Victoire Turkiye |
| 20:45 | Czechia vs Denmark | **2–2** | Nul — Czechia qualifiée (pen. 3–1) |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
Aucun pari ce round.

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Bosnia and Herzegovina vs Italy | Italy W | @1.64 | €25 | ❌ 1–1 | -€25 |

Bilan : **0✅ 1❌** — **€-25**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Sweden vs Poland | Poland W | @3.47 | €10 | ❌ 3–2 | -€10 |

Bilan : **0✅ 1❌** — **€-10**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Pronostic | Cote | Résultat |
|---|---|---|---|
| Bosnia and Herzegovina vs Italy | Italy W | @1.64 | ❌ 1–1 |

Mise : **€15** — Combiné **PERDU** — **€-15**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky
Aucun pari ce round (aucune cote ne passe le seuil < 1.50).

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Bosnia and Herzegovina vs Italy | **Bosnia W** | @6.35 | €50 | ✅ qualifiée (1–1, pen. 4–1) | **+€317.50** |
| Sweden vs Poland | Poland W | @3.47 | €50 | ❌ 3–2 | -€50 |
| Kosovo vs Turkiye | Kosovo W | @4.10 | €35 | ❌ 0–1 | -€35 |
| Czechia vs Denmark | **Czechia W** | @4.00 | €35 | ✅ qualifiée (2–2, pen. 3–1) | **+€140.00** |

Bilan : **2✅ 2❌** — **+€372.50**

---

## Résultats — WCQ Europe (Playoffs, 26 mars 2026)

### Résultats des matchs

| Heure | Match | Score | Résultat |
|---|---|---|---|
| 18:00 | Turkiye vs Romania | **1–0** | Victoire Turkiye |
| 20:45 | Wales vs Bosnia and Herzegovina | **1–1** | Nul (Bosnia qualifiée aux tirs au but 4–2) |
| 20:45 | Poland vs Albania | **2–1** | Victoire Poland |
| 20:45 | Slovakia vs Kosovo | **3–4** | **Victoire Kosovo** (surprise) |
| 20:45 | Czechia vs Ireland | **2–2** | Nul (Czechia qualifiée aux tirs au but 4–3) |
| 20:45 | Italy vs Northern Ireland | **2–0** | Victoire Italy |
| 20:45 | Ukraine vs Sweden | **1–3** | Victoire Sweden (hat-trick Gyökeres) |
| 20:45 | Denmark vs North Macedonia | **4–0** | Victoire Denmark |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Italy vs Northern Ireland | Italy W | @1.33 | €35 | ✅ 2–0 | **+€11.55** |
| Ukraine vs Sweden | Ukraine W | @3.07 | €35 | ❌ 1–3 | -€35 |

Bilan : **1✅ 1❌** — **€-23.45**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Czechia vs Ireland | **Czechia W** | @2.03 | €25 | ✅ 2–2 (qualifiée pen. 4–3) | **+€25.75** |

Bilan : **1✅ 0❌** — **+€25.75**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Ukraine vs Sweden | Ukraine W | @3.07 | €10 | ❌ 1–3 | -€10 |

Bilan : **0✅ 1❌** — **€-10**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Pronostic | Cote | Résultat |
|---|---|---|---|
| Turkiye vs Romania | Turkiye W | @1.40 | ✅ 1–0 |
| Italy vs Northern Ireland | Italy W | @1.33 | ✅ 2–0 |
| Denmark vs North Macedonia | Denmark W | @1.36 | ✅ 4–0 |

Mise : **€15** — Combiné **GAGNÉ** — **+€22.98**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky (combiné)
| Match | Pronostic | Cote | Résultat |
|---|---|---|---|
| Turkiye vs Romania | Turkiye W | @1.40 | ✅ 1–0 |
| Italy vs Northern Ireland | Italy W | @1.33 | ✅ 2–0 |
| Denmark vs North Macedonia | Denmark W | @1.36 | ✅ 4–0 |

Mise : **€20** — Combiné **GAGNÉ** — **+€30.65**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Turkiye vs Romania | Romania W | @6.60 | €50 | ❌ 1–0 | -€50 |
| Wales vs Bosnia | **Bosnia W** | @4.25 | €35 | ✅ qualifiée (1–1, pen. 2–4) | **+€113.75** |
| Poland vs Albania | Albania W | @5.94 | €50 | ❌ 2–1 | -€50 |
| Slovakia vs Kosovo | **Kosovo W** | @4.16 | €35 | ✅ 3–4 | **+€110.60** |
| Czechia vs Ireland | Ireland W | @4.16 | €35 | ❌ 2–2 (Czechia qualifiée pen.) | -€35 |
| Italy vs Northern Ireland | Northern Ireland W | @12.40 | €50 | ❌ 2–0 | -€50 |
| Ukraine vs Sweden | Ukraine W | @3.07 | €50 | ❌ 1–3 | -€50 |
| Denmark vs North Macedonia | North Macedonia W | @10.60 | €50 | ❌ 4–0 | -€50 |

Bilan : **2✅ 6❌** — **€-60.65**

---

## Résultats — Week-end 20–22 mars 2026 (EPL / Ligue 1)

### Résultats des matchs

| Match | Score | Résultat |
|---|---|---|
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
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Bournemouth vs Manchester United | Home Win | @3.32 | €25 | Reporté | €+25 (remb.) |
| Auxerre vs Brest | **Home Win** | @2.38 | €25 | ✅ 3–0 | **+€59.50** |
| Nantes vs Strasbourg | **Away Win** | @2.03 | €25 | ✅ 2–3 | **+€50.75** |
| Leeds United vs Brentford | Home Win | @2.51 | €25 | ❌ 0–0 | -€25 |
| Tottenham vs Nottingham Forest | Home Win | @2.29 | €25 | ❌ 0–3 | -€25 |
| Toulouse vs Lorient | Away Win | @4.72 | €25 | ❌ 1–0 | -€25 |
| Nice vs Paris Saint Germain | Draw | @5.82 | €25 | ❌ 0–4 | -€25 |

Bilan : **2✅ 4❌** — **€-44.75**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Auxerre vs Brest | Away Win | @3.24 | €10 | ❌ 3–0 | -€10 |

Bilan : **0✅ 1❌** — **€-10**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Pronostic | Cote | Résultat |
|---|---|---|---|
| Fulham vs Burnley | Home Win | @1.57 | ✅ 3–1 |
| Nice vs PSG | Away Win (PSG) | @1.35 | ✅ 0–4 |
| Everton vs Chelsea | Home Win | @3.56 | ✅ 3–0 |
| Newcastle vs Sunderland | **Home Win** | @1.67 | ❌ 1–2 |

Mise : **€15** — Combiné **PERDU** (Sunderland upset) — **€-15**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky (combiné)
| Match | Pronostic | Cote | Résultat |
|---|---|---|---|
| Nice vs PSG | Away Win (PSG) | @1.35 | ✅ 0–4 |
| Everton vs Chelsea | Home Win | @3.56 | ✅ 3–0 |
| Newcastle vs Sunderland | **Home Win** | @1.67 | ❌ 1–2 |

Mise : **€20** — Combiné **PERDU** (Sunderland upset) — **€-20**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Everton vs Chelsea | **Home Win** (Everton) | @3.56 | €50 | ✅ 3–0 | **+€178.00** |
| Newcastle vs Sunderland | **Away Win** (Sunderland) | @5.38 | €50 | ✅ 1–2 | **+€269.00** |
| Marseille vs Lille | **Away Win** (Lille) | @3.91 | €35 | ✅ 1–2 | **+€136.85** |
| Fulham vs Burnley | Away Win (Burnley) | @6.14 | €50 | ❌ 3–1 | -€50 |
| Toulouse vs Lorient | Away Win (Lorient) | @4.72 | €50 | ❌ 1–0 | -€50 |
| Auxerre vs Brest | Away Win (Brest) | @3.24 | €35 | ❌ 3–0 | -€35 |
| Nice vs PSG | Home Win (Nice) | @8.00 | €50 | ❌ 0–4 | -€50 |
| Paris FC vs Le Havre | Away Win (Le Havre) | @4.44 | €35 | ❌ 3–2 | -€35 |
| Nantes vs Strasbourg | Home Win (Nantes) | @3.66 | €20 | ❌ 2–3 | -€20 |

Bilan : **3✅ 6❌** — **+€134.80**

---

<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
<br/>Turfutodays's betbots is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">Attribution-ShareAlike 2.0 France (CC BY-SA 2.0 FR)</a>.

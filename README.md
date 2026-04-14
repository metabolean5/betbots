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

## Classement Saison 3 – Week-end (11–13 avril 2026)

| Rang | Bot | Net total | Paris ✅ | Paris ❌ | Total |
|------|-----|-----------|---------|---------|-------|
| 🥇 | **Way to Claude** | **€+566.50** | 17 | 39 | 56 |
| 🥈 | **Risky Rifki** | **€+113.75** | 11 | 14 | 25 |
| 🥉 | **Billy Bayes** | **€+66.15** | 11 | 6 | 17 |
| #4 | **Vent d'Ofsky** | **€-0.36** | 5 | 3 | 7 |
| #5 | **Risky Vent d'Ofsky** | **€-77.22** | 2 | 7 | 12 |
| #6 | **Pat Nostat** | **€-112.40** | 3 | 7 | 10 |
## Paris — UCL QF (7–8 avril 2026)

> Données scrappées via `betting_arena.py`.

### Programme

| Date | Match | Cotes (dom / nul / ext) |
|---|---|---|
| Mar 07/04 19:00 | Sporting Lisbon vs Arsenal | @4.60 / @3.75 / @1.75 |
| Mar 07/04 19:00 | Real Madrid vs Bayern Munich | @2.85 / @3.95 / @2.22 |
| Mer 08/04 19:00 | Barcelona vs Atlético Madrid | @1.50 / @5.00 / @5.60 |
| Mer 08/04 19:00 | Paris Saint Germain vs Liverpool | @1.70 / @4.20 / @4.60 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Real Madrid vs Bayern Munich | **Real Madrid W** | @2.85 | €35 | €99.75 |
| Barcelona vs Atlético Madrid | **Barcelona W** | @1.50 | €35 | €52.50 |
| PSG vs Liverpool | **PSG W** | @1.70 | €35 | €59.50 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
Aucun pari ce round.

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Barcelona vs Atlético Madrid | **Barcelona W** | @1.50 | €50 | €75.00 |
| PSG vs Liverpool | **PSG W** | @1.70 | €10 | €17.00 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Pronostic | Cote |
|---|---|---|
| Barcelona vs Atlético Madrid | Barcelona W | @1.50 |

Mise combinée : **€15** — Gain potentiel : **€22.50**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky
Aucun pari ce round.

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Sporting Lisbon vs Arsenal | **Sporting W** | @4.60 | €50 | €230.00 |
| Barcelona vs Atlético Madrid | **Atlético W** | @5.60 | €35 | €196.00 |

> Way to Claude joue l'upset Sporting @4.60 (EV=0.61) et Atlético @5.60 (EV=0.31) — deux paris contrarians à haute valeur.

## Résultats — UCL QF (7–8 avril 2026)

### Résultats des matchs

| Date | Match | Score | Résultat |
|---|---|---|---|
| Mar 07/04 | Sporting Lisbon vs Arsenal | **0–1** | Victoire Arsenal |
| Mar 07/04 | Real Madrid vs Bayern Munich | **1–2** | Victoire Bayern Munich |
| Mer 08/04 | Barcelona vs Atlético Madrid | **0–2** | Victoire Atlético Madrid |
| Mer 08/04 | PSG vs Liverpool | **2–0** | Victoire PSG |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Real Madrid vs Bayern Munich | Real Madrid W | @2.85 | €35 | ❌ 1–2 | -€35 |
| Barcelona vs Atlético Madrid | Barcelona W | @1.50 | €35 | ❌ 0–2 | -€35 |
| PSG vs Liverpool | **PSG W** | @1.70 | €35 | ✅ 2–0 | **+€59.50** |

Bilan : **1✅ 2❌** — **-€10.50**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
Aucun pari ce round.

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Barcelona vs Atlético Madrid | Barcelona W | @1.50 | €50 | ❌ 0–2 | -€50 |
| PSG vs Liverpool | **PSG W** | @1.70 | €10 | ✅ 2–0 | **+€17.00** |

Bilan : **1✅ 1❌** — **-€33.00**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Pronostic | Cote | Résultat |
|---|---|---|---|
| Barcelona vs Atlético Madrid | Barcelona W | @1.50 | ❌ 0–2 |

Mise : **€15** — Combiné **PERDU** — **-€15**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky
Aucun pari ce round.

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Sporting Lisbon vs Arsenal | Sporting W | @4.60 | €50 | ❌ 0–1 | -€50 |
| Barcelona vs Atlético Madrid | **Atlético W** | @5.60 | €35 | ✅ 0–2 | **+€196.00** |

Bilan : **1✅ 1❌** — **+€146.00**

---

## Paris — Week-end 11–13 avril 2026 (EPL / Ligue 1)

> Données scrappées via `betting_arena_weekend.py`.

### Programme

**Premier League**

| Date | Match | Cotes (dom / nul / ext) |
|---|---|---|
| Sam 11/04 11:30 | Arsenal vs Bournemouth | @1.40 / @4.50 / @6.75 |
| Sam 11/04 14:00 | Brentford vs Everton | @2.05 / @3.30 / @3.35 |
| Sam 11/04 14:00 | Burnley vs Brighton | @4.20 / @3.95 / @1.66 *(sans forme)* |
| Sam 11/04 16:30 | Liverpool vs Fulham | @1.60 / @4.10 / @4.60 |
| Dim 12/04 13:00 | Nottingham Forest vs Aston Villa | @2.60 / @3.40 / @2.75 |
| Dim 12/04 13:00 | Crystal Palace vs Newcastle United | @3.25 / @3.45 / @2.28 |
| Dim 12/04 13:00 | Sunderland vs Tottenham Hotspur | @2.50 / @3.35 / @2.55 |
| Dim 12/04 15:30 | Chelsea vs Manchester City | @2.90 / @3.95 / @2.05 |
| Lun 13/04 19:00 | Manchester United vs Leeds United | @1.69 / @4.32 / @5.23 |

**Ligue 1**

| Date | Match | Cotes (dom / nul / ext) |
|---|---|---|
| Sam 11/04 17:00 | Auxerre vs Nantes | @1.97 / @3.44 / @4.24 |
| Dim 12/04 15:15 | Nice vs Le Havre | @1.94 / @3.20 / @4.77 |
| Dim 12/04 15:15 | Toulouse vs Lille | @3.24 / @3.25 / @2.40 |
| Dim 12/04 18:45 | Lyon vs Lorient | @1.70 / @3.94 / @5.16 |
| Ven 17/04 18:45 | RC Lens vs Toulouse | @1.61 / @4.12 / @5.25 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Arsenal vs Bournemouth | **Arsenal W** | @1.40 | €35 | €49.00 |
| Manchester United vs Leeds United | **Man United W** | @1.69 | €35 | €59.15 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Brentford vs Everton | **Brentford W** | @2.05 | €25 | €51.25 |
| Nottingham Forest vs Aston Villa | **Forest W** | @2.60 | €25 | €65.00 |
| Chelsea vs Manchester City | **Man City W** | @2.05 | €25 | €51.25 |
| Nice vs Le Havre | **Nice W** | @1.94 | €25 | €48.50 |
| Toulouse vs Lille | **Lille W** | @2.40 | €25 | €60.00 |
| Lyon vs Lorient | **Lyon W** | @1.70 | €25 | €42.50 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Arsenal vs Bournemouth | **Arsenal W** | @1.40 | €10 | €14.00 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Pronostic | Cote |
|---|---|---|
| Arsenal vs Bournemouth | Arsenal W | @1.40 |
| Liverpool vs Fulham | Liverpool W | @1.60 |
| Nottingham Forest vs Aston Villa | Forest W | @2.60 |
| RC Lens vs Toulouse | RC Lens W | @1.61 |

Mise combinée : **€15** — Gain potentiel : **€80.29**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky (combiné)
| Match | Pronostic | Cote |
|---|---|---|
| Arsenal vs Bournemouth | Arsenal W | @1.40 |
| Liverpool vs Fulham | Liverpool W | @1.60 |
| Nottingham Forest vs Aston Villa | Forest W | @2.60 |

Mise combinée : **€20** — Gain potentiel : **€41.56**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Arsenal vs Bournemouth | **Bournemouth W** | @6.75 | €35 | €236.25 |
| Brentford vs Everton | **Everton W** | @3.35 | €35 | €117.25 |
| Liverpool vs Fulham | **Fulham W** | @4.60 | €50 | €230.00 |
| Crystal Palace vs Newcastle United | **Crystal Palace W** | @3.25 | €35 | €113.75 |
| Manchester United vs Leeds United | **Leeds W** | @5.23 | €20 | €104.60 |
| Auxerre vs Nantes | **Nantes W** | @4.24 | €35 | €148.40 |
| Nice vs Le Havre | **Le Havre W** | @4.77 | €35 | €166.95 |
| Lyon vs Lorient | **Lorient W** | @5.16 | €50 | €258.00 |

> Way to Claude joue les outsiders à domicile (Bournemouth @6.75, EV=0.76) et les upsets en Ligue 1 (Lorient @5.16, EV=0.58).

---

## Résultats — Week-end 11–13 avril 2026 (EPL / Ligue 1)

### Résultats des matchs

**Premier League**

| Date | Match | Score | Résultat |
|---|---|---|---|
| Sam 11/04 | Arsenal vs Bournemouth | **1–2** | Victoire Bournemouth |
| Sam 11/04 | Brentford vs Everton | **2–2** | Nul |
| Sam 11/04 | Burnley vs Brighton | **0–2** | Victoire Brighton |
| Sam 11/04 | Liverpool vs Fulham | **2–0** | Victoire Liverpool |
| Dim 12/04 | Sunderland vs Tottenham | **1–0** | Victoire Sunderland |
| Dim 12/04 | Crystal Palace vs Newcastle | **2–1** | Victoire Crystal Palace |
| Dim 12/04 | Nottingham Forest vs Aston Villa | **1–1** | Nul |
| Dim 12/04 | Chelsea vs Manchester City | **0–3** | Victoire Manchester City |
| Lun 13/04 | Manchester United vs Leeds United | **1–2** | Victoire Leeds United |

**Ligue 1**

| Date | Match | Score | Résultat |
|---|---|---|---|
| Sam 11/04 | Auxerre vs Nantes | **0–0** | Nul |
| Dim 12/04 | Nice vs Le Havre | **1–1** | Nul |
| Dim 12/04 | Toulouse vs Lille | **0–4** | Victoire Lille |
| Dim 12/04 | Lyon vs Lorient | **2–0** | Victoire Lyon |
| Ven 17/04 | RC Lens vs Toulouse | — | *Pas encore joué* |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Arsenal vs Bournemouth | Arsenal W | @1.40 | €35 | ❌ 1–2 | -€35 |
| Manchester United vs Leeds United | Man United W | @1.69 | €35 | ❌ 1–2 | -€35 |

Bilan : **0✅ 2❌** — **-€70**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Brentford vs Everton | Brentford W | @2.05 | €25 | ❌ 2–2 | -€25 |
| Nottingham Forest vs Aston Villa | Forest W | @2.60 | €25 | ❌ 1–1 | -€25 |
| Chelsea vs Manchester City | **Man City W** | @2.05 | €25 | ✅ 0–3 | **+€51.25** |
| Nice vs Le Havre | Nice W | @1.94 | €25 | ❌ 1–1 | -€25 |
| Toulouse vs Lille | **Lille W** | @2.40 | €25 | ✅ 0–4 | **+€60.00** |
| Lyon vs Lorient | **Lyon W** | @1.70 | €25 | ✅ 2–0 | **+€42.50** |

Bilan : **3✅ 3❌** — **+€78.75**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Arsenal vs Bournemouth | Arsenal W | @1.40 | €10 | ❌ 1–2 | -€10 |

Bilan : **0✅ 1❌** — **-€10**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Pronostic | Cote | Résultat |
|---|---|---|---|
| Arsenal vs Bournemouth | Arsenal W | @1.40 | ❌ 1–2 |
| Liverpool vs Fulham | Liverpool W | @1.60 | ✅ 2–0 |
| Nottingham Forest vs Aston Villa | Forest W | @2.60 | ❌ 1–1 |
| RC Lens vs Toulouse | RC Lens W | @1.61 | — *17/04* |

Mise : **€15** — Combiné **PERDU** (Arsenal éliminé) — **-€15**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky (combiné)
| Match | Pronostic | Cote | Résultat |
|---|---|---|---|
| Arsenal vs Bournemouth | Arsenal W | @1.40 | ❌ 1–2 |
| Liverpool vs Fulham | Liverpool W | @1.60 | ✅ 2–0 |
| Nottingham Forest vs Aston Villa | Forest W | @2.60 | ❌ 1–1 |

Mise : **€20** — Combiné **PERDU** (Arsenal éliminé) — **-€20**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Pronostic | Cote | Mise | Résultat | Gain |
|---|---|---|---|---|---|
| Arsenal vs Bournemouth | **Bournemouth W** | @6.75 | €35 | ✅ 1–2 | **+€236.25** |
| Brentford vs Everton | Everton W | @3.35 | €35 | ❌ 2–2 | -€35 |
| Liverpool vs Fulham | Fulham W | @4.60 | €50 | ❌ 2–0 | -€50 |
| Crystal Palace vs Newcastle | **Crystal Palace W** | @3.25 | €35 | ✅ 2–1 | **+€113.75** |
| Manchester United vs Leeds | **Leeds W** | @5.23 | €20 | ✅ 1–2 | **+€104.60** |
| Auxerre vs Nantes | Nantes W | @4.24 | €35 | ❌ 0–0 | -€35 |
| Nice vs Le Havre | Le Havre W | @4.77 | €35 | ❌ 1–1 | -€35 |
| Lyon vs Lorient | Lorient W | @5.16 | €50 | ❌ 2–0 | -€50 |

Bilan : **3✅ 5❌** — **+€249.60**

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

<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
<br/>Turfutodays's betbots is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">Attribution-ShareAlike 2.0 France (CC BY-SA 2.0 FR)</a>.

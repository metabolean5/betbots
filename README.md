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

---

## Paris — UCL QF 2e manche (14–15 avril 2026)

> Données scrappées via `betting_arena.py`.

### Programme

| Date | Match | Cotes (dom / nul / ext) |
|---|---|---|
| Mar 14/04 19:00 | Atlético Madrid vs Barcelona | @3.60 / @4.20 / @1.80 |
| Mar 14/04 19:00 | Liverpool vs Paris Saint Germain | @2.39 / @4.25 / @2.71 |
| Mer 15/04 19:00 | Arsenal vs Sporting Lisbon | @1.50 / @4.60 / @7.20 |
| Mer 15/04 19:00 | Bayern Munich vs Real Madrid | @1.55 / @5.06 / @4.93 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Bayern Munich vs Real Madrid | **Bayern W** | @1.55 | €35 | €54.25 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Liverpool vs Paris Saint Germain | **PSG W** | @2.71 | €25 | €67.75 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Atlético Madrid vs Barcelona | **Barcelona W** | @1.80 | €10 | €18.00 |
| Liverpool vs Paris Saint Germain | **PSG W** | @2.71 | €10 | €27.10 |
| Bayern Munich vs Real Madrid | **Bayern W** | @1.55 | €10 | €15.50 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Pronostic | Cote |
|---|---|---|
| Arsenal vs Sporting Lisbon | Arsenal W | @1.50 |
| Bayern Munich vs Real Madrid | Bayern W | @1.55 |

Mise combinée : **€15** — Gain potentiel : **€34.88**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky
Aucun pari ce round (aucune cote ne passe le seuil < 1.50).

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Pronostic | Cote | Mise | Gain potentiel |
|---|---|---|---|---|
| Liverpool vs Paris Saint Germain | **PSG W** | @2.71 | €35 | €94.85 |
| Arsenal vs Sporting Lisbon | **Sporting W** | @7.20 | €50 | €360.00 |
| Bayern Munich vs Real Madrid | **Nul** | @5.06 | €35 | €177.10 |

> Way to Claude joue l'upset Sporting @7.20 (EV=1.76) — plus haut EV de la saison — et le nul surprise Bayern-Real @5.06 (EV=0.27).

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

## Paris — UCL QF 1e manche (7–8 avril 2026)

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

## Résultats — UCL QF 1e manche (7–8 avril 2026)

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

<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
<br/>Turfutodays's betbots is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">Attribution-ShareAlike 2.0 France (CC BY-SA 2.0 FR)</a>.

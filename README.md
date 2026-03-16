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

> UCL + mode week-end (EPL / Ligue 1). UEL/UECL non vérifiables via l'API gratuite.

| Rang | Bot | Net total | Paris ✅ | Paris ❌ | ROI |
|------|-----|-----------|---------|---------|-----|
| 🥇 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="30"> **Risky Rifki** | **€+70.75** | 3 | 4 | +40% |
| 🥈 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="30"> **Billy Bayes** | **€+61.95** | 3 | 1 | +44% |
| 🥉 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="30"> **Pat Nostat** | **€+17.50** | 1 | 1 | +29% |
| #4 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="30"> **Vent d'Ofsky** | **€-20.00** | 0 | 1 | -100% |
| #5 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="30"> **Risky Vent d'Ofsky** | **€-30.00** | 0 | 2 | -100% |
| #6 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="30"> **Way to Claude** | **€-40.05** | 3 | 9 | -8% |

> Week-end 13–16/03 : Bournemouth vs Manchester United (20/03) remboursé — match trop tardif.

---

## Paris en cours — UCL R16 Second Legs (17–18 mars 2026)

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
| Match | Date | Pronostic | Mise | Gain potentiel |
|---|---|---|---|---|
| Arsenal vs Bayer Leverkusen | 17/03 20:00 | **Home Win** | €35 | +45.15 |
| Barcelona vs Newcastle United | 18/03 17:45 | **Home Win** | €35 | +53.20 |
| Bayern Munich vs Atalanta BC | 18/03 20:00 | **Home Win** | €35 | +45.85 |

Mise totale : **€105**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
| Match | Date | Pronostic | Mise | Gain potentiel |
|---|---|---|---|---|
| Chelsea vs Paris Saint Germain | 17/03 20:00 | **Away Win** (PSG) | €25 | +72.50 |
| Manchester City vs Real Madrid | 17/03 20:00 | **Home Win** (Man City) | €25 | +37.50 |

Mise totale : **€50**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Date | Pronostic | Mise | Gain potentiel |
|---|---|---|---|---|
| Bayern Munich vs Atalanta BC | 18/03 20:00 | **Home Win** | €10 | +13.10 |
| Tottenham Hotspur vs Atlético Madrid | 18/03 20:00 | **Away Win** (Atlético) | €50 | +131.00 |

Mise totale : **€60**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Date | Pronostic |
|---|---|---|
| Sporting Lisbon vs Bodø/Glimt | 17/03 17:45 | **Home Win** |
| Arsenal vs Bayer Leverkusen | 17/03 20:00 | **Home Win** |
| Manchester City vs Real Madrid | 17/03 20:00 | **Home Win** |
| Barcelona vs Newcastle United | 18/03 17:45 | **Home Win** |
| Bayern Munich vs Atalanta BC | 18/03 20:00 | **Home Win** |
| Liverpool vs Galatasaray | 18/03 20:00 | **Home Win** |

Mise : **€15** — Gain potentiel combiné : **119.43**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky (combiné)
| Match | Date | Pronostic |
|---|---|---|
| Arsenal vs Bayer Leverkusen | 17/03 20:00 | **Home Win** |
| Bayern Munich vs Atalanta BC | 18/03 20:00 | **Home Win** |
| Liverpool vs Galatasaray | 18/03 20:00 | **Home Win** |

Mise : **€20** — Gain potentiel combiné : **42.59**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude
| Match | Date | Pronostic | EV | Mise | Gain potentiel |
|---|---|---|---|---|---|
| Sporting Lisbon vs Bodø/Glimt | 17/03 17:45 | **Away Win** (Bodø) | — | €50 | +244.00 |
| Arsenal vs Bayer Leverkusen | 17/03 20:00 | **Away Win** (Leverkusen) | — | €50 | +550.00 |
| Chelsea vs Paris Saint Germain | 17/03 20:00 | **Away Win** (PSG) | — | €35 | +101.50 |
| Manchester City vs Real Madrid | 17/03 20:00 | **Away Win** (Real Madrid) | — | €50 | +262.50 |
| Barcelona vs Newcastle United | 18/03 17:45 | **Away Win** (Newcastle) | — | €35 | +175.00 |
| Bayern Munich vs Atalanta BC | 18/03 20:00 | **Away Win** (Atalanta) | — | €50 | +430.50 |
| Tottenham Hotspur vs Atlético Madrid | 18/03 20:00 | **Away Win** (Atlético) | — | €35 | +91.70 |
| Liverpool vs Galatasaray | 18/03 20:00 | **Away Win** (Galatasaray) | — | €50 | +482.00 |

Mise totale : **€355** — Gain potentiel cumulé : **€2337.20**

<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
<br/>Turfutodays's betbots is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">Attribution-ShareAlike 2.0 France (CC BY-SA 2.0 FR)</a>.

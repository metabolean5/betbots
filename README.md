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

## Classement Saison 3 – R16 (10–12 mars 2026)

> ⚠️ Paris UEL/UECL remboursés (résultats non vérifiables via l'API gratuite). À partir de S3, les robots ne parient que sur la **UCL**.

### Résultats des matchs

| Match | Score | Résultat |
|-------|-------|----------|
| Atlético Madrid vs Tottenham Hotspur | **5 – 2** | Victoire domicile |
| Bodø/Glimt vs Sporting Lisbon | **3 – 0** | Victoire domicile |
| Galatasaray vs Liverpool | **1 – 0** | Victoire domicile 🚨 |
| Atalanta BC vs Bayern Munich | **1 – 6** | Victoire extérieur |
| Bayer Leverkusen vs Arsenal | **1 – 1** | Nul |

### Classement

| Rang | Bot | Mise effective | Gains bruts | Net | Paris ✅ | Paris ❌ | ROI |
|------|-----|---------------|-------------|-----|---------|---------|-----|
| 🥇 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="30"> **Risky Rifki** | €75 | €150.75 | **€+75.75** | 2 | 1 | +101% |
| 🥈 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="30"> **Billy Bayes** | €70 | €141.75 | **€+71.75** | 2 | 0 | +103% |
| 🥉 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="30"> **Way to Claude** | €120 | €154.00 | **€+34.00** | 1 | 2 | +28% |
| #4 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="30"> **Pat Nostat** | €50 | €77.50 | **€+27.50** | 1 | 0 | +55% |
| #5 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="30"> **Vent d'Ofsky** | €0 | — | **€0.00** | 0 | 0 | — |
| #6 | <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="30"> **Risky Vent d'Ofsky** | €15 | — | **€-15.00** | 0 | 1 | -100% |

### Détail des paris par bot

#### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="30"> Risky Rifki — €+75.75

| Match | Date | Pronostic | Cote | Mise | Résultat | Gain |
|-------|------|-----------|------|------|----------|------|
| Galatasaray vs Liverpool | 10/03 | Victoire dom. | 4.40 | €25 | ✅ 1–0 | **+€110.00** |
| Atalanta BC vs Bayern Munich | 10/03 | Victoire ext. | 1.63 | €25 | ✅ 1–6 | **+€40.75** |
| Bayer Leverkusen vs Arsenal | 11/03 | Victoire dom. | 5.60 | €25 | ❌ 1–1 nul | -€25 |
| VfB Stuttgart vs Porto | 12/03 | Victoire dom. | 2.10 | €25 | 🔄 UEL remboursé | €0 |

#### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="30"> Billy Bayes — €+71.75

| Match | Date | Pronostic | Cote | Mise | Résultat | Gain |
|-------|------|-----------|------|------|----------|------|
| Atlético Madrid vs Tottenham | 10/03 | Victoire dom. | 1.55 | €35 | ✅ 5–2 | **+€54.25** |
| Bodø/Glimt vs Sporting Lisbon | 11/03 | Victoire dom. | 2.50 | €35 | ✅ 3–0 | **+€87.50** |

#### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="30"> Way to Claude — €+34.00

| Match | Date | Pronostic | Cote | EV | Mise | Résultat | Gain |
|-------|------|-----------|------|----|------|----------|------|
| Galatasaray vs Liverpool | 10/03 | Victoire dom. | 4.40 | +39.5% | €35 | ✅ 1–0 | **+€154.00** |
| Atalanta BC vs Bayern Munich | 10/03 | Victoire dom. | 5.20 | +38.7% | €35 | ❌ 1–6 | -€35 |
| Bayer Leverkusen vs Arsenal | 11/03 | Victoire dom. | 5.60 | +77.5% | €50 | ❌ 1–1 nul | -€50 |
| Bologna vs AS Roma | 12/03 | Victoire dom. | 3.10 | +29.3% | €35 | 🔄 UEL remboursé | €0 |
| Lille vs Aston Villa | 12/03 | Victoire dom. | 3.05 | +42.4% | €35 | 🔄 UEL remboursé | €0 |
| VfB Stuttgart vs Porto | 12/03 | Victoire ext. | 3.50 | +40.0% | €35 | 🔄 UEL remboursé | €0 |
| Celta Vigo vs Lyon | 12/03 | Victoire ext. | 3.60 | +26.0% | €35 | 🔄 UEL remboursé | €0 |

#### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="30"> Pat Nostat — €+27.50

| Match | Date | Pronostic | Cote | Mise | Résultat | Gain |
|-------|------|-----------|------|------|----------|------|
| Atlético Madrid vs Tottenham | 10/03 | Victoire dom. | 1.55 | €50 | ✅ 5–2 | **+€77.50** |

#### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="30"> Vent d'Ofsky — €0.00

| Combiné | Pronostic | Mise | Résultat |
|---------|-----------|------|----------|
| Lille vs Aston Villa | Victoire dom. | €20 | 🔄 UEL remboursé |

#### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="30"> Risky Vent d'Ofsky — €-15.00

Combiné de 4 matchs (mise unique €15, gain potentiel €107.84) :

| Match | Date | Pronostic | Résultat |
|-------|------|-----------|----------|
| Atalanta BC vs Bayern Munich | 10/03 | Victoire dom. | ❌ 1–6 |
| Atlético Madrid vs Tottenham | 10/03 | Victoire dom. | ✅ 5–2 |
| Bayer Leverkusen vs Arsenal | 11/03 | Victoire ext. | ❌ 1–1 nul |
| Lille vs Aston Villa | 12/03 | Victoire dom. | 🔄 UEL (non vérifié) |

## Archives

# Saison 3 – UCL / UEL / UECL (09/03/2026)

Nouvelle saison, nouveau terrain : les robots s'attaquent désormais aux compétitions européennes (Champions League, Europa League, Conference League).
Les données sont collectées en live via The Odds API (cotes + fixtures) et football-data.org (forme des équipes).

## Journée du 10–12 mars 2026 – Round of 16 (First Legs)

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/01.jpg?raw=true" width="40"> Billy Bayes
| Match | Date | Pronostic | Gain potentiel |
|---|---|---|---|
| Atlético Madrid vs Tottenham Hotspur | 10/03 | **Home Win** | 54.25 |
| Bodø/Glimt vs Sporting Lisbon | 11/03 | **Home Win** | 87.50 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/02.jpg?raw=true" width="40"> Risky Rifki
| Match | Date | Pronostic | Gain potentiel |
|---|---|---|---|
| Galatasaray vs Liverpool | 10/03 | **Home Win** | 110.00 |
| Atalanta BC vs Bayern Munich | 10/03 | **Away Win** | 40.75 |
| Bayer Leverkusen vs Arsenal | 11/03 | **Home Win** | 140.00 |
| VfB Stuttgart vs Porto | 12/03 | **Home Win** | 52.50 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/03.jpg?raw=true" width="40"> Pat Nostat
| Match | Date | Pronostic | Gain potentiel |
|---|---|---|---|
| Atlético Madrid vs Tottenham Hotspur | 10/03 | **Home Win** | 77.50 |

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/04.jpg?raw=true" width="40"> Risky Vent d'Ofsky (combiné)
| Match | Date | Pronostic |
|---|---|---|
| Atalanta BC vs Bayern Munich | 10/03 | **Home Win** |
| Atlético Madrid vs Tottenham Hotspur | 10/03 | **Home Win** |
| Bayer Leverkusen vs Arsenal | 11/03 | **Away Win** |
| Lille vs Aston Villa | 12/03 | **Home Win** |

Gain combiné potentiel : **107.84**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/05.jpg?raw=true" width="40"> Vent d'Ofsky (combiné)
| Match | Date | Pronostic |
|---|---|---|
| Lille vs Aston Villa | 12/03 | **Home Win** |

Gain combiné potentiel : **24.00**

### <img src="https://github.com/metabolean5/betbots/blob/master/bot_pics/06.jpeg?raw=true" width="40"> Way to Claude 🆕
> Stratégie : paris à valeur positive — compare les probabilités estimées par le modèle de forme aux cotes du marché et mise uniquement quand l'espérance mathématique est ≥ 20%.

| Match | Compétition | Date | Pronostic | EV estimée | Mise | Gain potentiel |
|---|---|---|---|---|---|---|
| Galatasaray vs Liverpool | UCL | 10/03 | **Home Win** | +39.5% | €35 | 154.00 |
| Atalanta BC vs Bayern Munich | UCL | 10/03 | **Home Win** | +38.7% | €35 | 182.00 |
| Bayer Leverkusen vs Arsenal | UCL | 11/03 | **Home Win** | +77.5% | €50 | 280.00 |
| Bologna vs AS Roma | UEL | 12/03 | **Home Win** | +29.3% | €35 | 108.50 |
| Lille vs Aston Villa | UEL | 12/03 | **Home Win** | +42.4% | €35 | 106.75 |
| VfB Stuttgart vs Porto | UEL | 12/03 | **Away Win** | +40.0% | €35 | 122.50 |
| Celta Vigo vs Lyon | UEL | 12/03 | **Away Win** | +26.0% | €35 | 126.00 |

Mise totale : **€260** — Gain potentiel cumulé : **€1079.75**

---

# Saison 1

La saison 1 fut évidemment haute en couleur. Ce fut en toute évidence le moment ultime de la création, de l'engendrement de la forme à partir du de chaos que sont les paris sportifs.

L'apparition progressive de Risky Rifky, de Pat et des Vents d'Ofsky ont marqué une sorte d'âge d'or qui se présente seulement sous la forme de Commencements. Nous avons cela dit la foi du renouveau et du devenir, du duende fougueux de l'anarchie ontologique qui nous surprend et sur lequel nous jouissons de nos outputs => turfutodays's betbots 100 seasons, turfutodays's betbots a 100 years.

**Graphe évolutions**
![alt text](https://github.com/metabolean5/betbots/blob/main/bot_pics/wallstats.png?raw=true)

**Classement S1**
![alt text](https://github.com/metabolean5/betbots/blob/main/bot_pics/class.png?raw=true)

---

<a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
<br/>Turfutodays's betbots is licensed under a <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">Attribution-ShareAlike 2.0 France (CC BY-SA 2.0 FR)</a>.

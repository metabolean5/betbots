#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
BetBots Arena – European Football Edition
==========================================
Run this script each week to generate predictions for upcoming
UCL / UEL / UECL matches.

Usage:
    python betting_arena.py
"""
__author__ = "mpdev"
__copyright__ = "Copyright 2026, Turfutoday's Betbots"
__license__ = "CC BY-SA 2.0 FR"

import json
import pprint as pp
import joblib

exec(open("Betbot.py").read())


# ─── Load bots ────────────────────────────────────────────────────────────────

print("=" * 60)
print("  BETBOTS ARENA  –  UCL / UEL / UECL")
print("=" * 60)

billy_bayes       = Betbot("Billy Bayes",
                            "classifiers/billy_bayes.pkl",
                            "bots_data/01_billybayes.json",    "01")
risky_rifki       = Betbot("Risky Rifki",
                            "classifiers/billy_bayes.pkl",
                            "bots_data/02_risky_rifky.json",   "02")
pat_nostat        = Betbot("Pat Nostat",
                            "none",
                            "bots_data/03_pat_nostat.json",    "03")
vent_dofsky       = Betbot("Vent d'Ofsky",
                            "none",
                            "bots_data/05_vent_dof.json",      "05")
risky_vent_dofsky = Betbot("Risky Vent d'Ofsky",
                            "none",
                            "bots_data/04_risky_vent_dof.json","04")
way_to_claude     = Betbot("Way to Claude",
                            "none",
                            "bots_data/06_valeur_darb.json",   "06")

botlist = [billy_bayes, risky_rifki, pat_nostat, risky_vent_dofsky, vent_dofsky, way_to_claude]


# ─── Scrape fixtures (only Billy Bayes fetches; others share his data) ────────

print("\nGathering live fixture data from Sofascore...")
billy_bayes.get_bets(billy_bayes)

for bot in [risky_rifki, pat_nostat, risky_vent_dofsky, vent_dofsky, way_to_claude]:
    bot.get_bets(billy_bayes)


# ─── Place bets ───────────────────────────────────────────────────────────────

print("\n" + "-" * 60)
print("Placing bets...")
print("-" * 60)

for bot in botlist:
    bot.place_bets()


# ─── Display confirmed bets ───────────────────────────────────────────────────

print("\n" + "=" * 60)
print("  CONFIRMED BETS FOR THIS WEEK")
print("=" * 60)

for bot in botlist:
    bot.printConfirmedBets()


# ─── Rankings ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("  PERFORMANCE RANKINGS")
print("=" * 60)

printClassification(botlist)


# ─── Save ─────────────────────────────────────────────────────────────────────

input("\nPress Enter to save bot data...")
input("Press Enter again to confirm...")

print("\nSaving bots data...")
for bot in botlist:
    bot.save_bot_data()

exec(open("htmlgen.py").read())
print("\nDone. Open betbot.html to view the full report.")

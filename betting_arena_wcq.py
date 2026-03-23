#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
BetBots WCQ Arena – UEFA World Cup Qualifiers
=============================================
Run before the WCQ matchdays to generate predictions.
Uses separate bot data files (*_wcq.json) so UCL/weekend data is never overwritten.
Results can be verified after matchday via verify_arena_wcq.py.

Usage:
    python3 betting_arena_wcq.py
"""
__author__ = "mpdev"

import json
import pprint as pp
import joblib

exec(open("Betbot.py").read())

WCQ_DATA = {
    "01": "bots_data/01_billybayes_wcq.json",
    "02": "bots_data/02_risky_rifky_wcq.json",
    "03": "bots_data/03_pat_nostat_wcq.json",
    "04": "bots_data/04_risky_vent_dof_wcq.json",
    "05": "bots_data/05_vent_dof_wcq.json",
    "06": "bots_data/06_valeur_darb_wcq.json",
}

print("=" * 60)
print("  BETBOTS WCQ ARENA  –  UEFA WC QUALIFIERS")
print("=" * 60)

billy_bayes       = Betbot("Billy Bayes",        "classifiers/billy_bayes.pkl", WCQ_DATA["01"], "01")
risky_rifki       = Betbot("Risky Rifki",         "classifiers/billy_bayes.pkl", WCQ_DATA["02"], "02")
pat_nostat        = Betbot("Pat Nostat",           "none", WCQ_DATA["03"], "03")
risky_vent_dofsky = Betbot("Risky Vent d'Ofsky",  "none", WCQ_DATA["04"], "04")
vent_dofsky       = Betbot("Vent d'Ofsky",         "none", WCQ_DATA["05"], "05")
way_to_claude     = Betbot("Way to Claude",        "none", WCQ_DATA["06"], "06")

botlist = [billy_bayes, risky_rifki, pat_nostat, risky_vent_dofsky, vent_dofsky, way_to_claude]

# ─── Scrape WCQ fixtures ──────────────────────────────────────────────────────

print("\nScraping WCQ fixtures via Sportradar...")
fixtures = scrap_fixtures_wcq_sr()

if not fixtures:
    print("No WCQ fixtures found.")
    exit(1)

for bot in botlist:
    bot.getMemory()["current_bets"] = fixtures

# ─── Place bets ───────────────────────────────────────────────────────────────

print("\n" + "-" * 60)
print("Placing bets...")
print("-" * 60)

for bot in botlist:
    bot.place_bets()

# ─── Display confirmed bets ───────────────────────────────────────────────────

print("\n" + "=" * 60)
print("  CONFIRMED WCQ BETS")
print("=" * 60)

for bot in botlist:
    bot.printConfirmedBets()

# ─── Save ─────────────────────────────────────────────────────────────────────

print("\nSaving WCQ bot data...")
for bot in botlist:
    bot.save_bot_data()

print("\nDone.")

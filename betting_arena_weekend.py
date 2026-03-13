#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
BetBots Weekend Arena – EPL / Ligue 1
======================================
Run each Friday/Saturday to generate predictions for the weekend's
Premier League and Ligue 1 matches.

Uses separate bot data files (*_wkd.json) so UCL data is never overwritten.
Results can be verified Monday via verify_arena_weekend.py.

Usage:
    python3 betting_arena_weekend.py
"""
__author__ = "mpdev"

import json
import pprint as pp
import joblib

exec(open("Betbot.py").read())

# ─── Weekend bot data files (separate from UCL files) ─────────────────────────

WKD_DATA = {
    "01": "bots_data/01_billybayes_wkd.json",
    "02": "bots_data/02_risky_rifky_wkd.json",
    "03": "bots_data/03_pat_nostat_wkd.json",
    "04": "bots_data/04_risky_vent_dof_wkd.json",
    "05": "bots_data/05_vent_dof_wkd.json",
    "06": "bots_data/06_valeur_darb_wkd.json",
}

print("=" * 60)
print("  BETBOTS WEEKEND ARENA  –  EPL / LIGUE 1")
print("=" * 60)

billy_bayes       = Betbot("Billy Bayes",
                            "classifiers/billy_bayes.pkl",
                            WKD_DATA["01"], "01")
risky_rifki       = Betbot("Risky Rifki",
                            "classifiers/billy_bayes.pkl",
                            WKD_DATA["02"], "02")
pat_nostat        = Betbot("Pat Nostat",
                            "none",
                            WKD_DATA["03"], "03")
risky_vent_dofsky = Betbot("Risky Vent d'Ofsky",
                            "none",
                            WKD_DATA["04"], "04")
vent_dofsky       = Betbot("Vent d'Ofsky",
                            "none",
                            WKD_DATA["05"], "05")
way_to_claude     = Betbot("Way to Claude",
                            "none",
                            WKD_DATA["06"], "06")

botlist = [billy_bayes, risky_rifki, pat_nostat, risky_vent_dofsky, vent_dofsky, way_to_claude]

# ─── Scrape EPL + Ligue 1 fixtures ────────────────────────────────────────────

print("\nBuilding team-ID cache...")
_build_team_cache()

print("\nScraping EPL + Ligue 1 fixtures...")
fixtures = scrap_fixtures_01(["EPL", "FL1"], round_prefix="Weekend EPL/FL1")

if not fixtures:
    print("No fixtures found this weekend.")
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
print("  CONFIRMED BETS THIS WEEKEND")
print("=" * 60)

for bot in botlist:
    bot.printConfirmedBets()

# ─── Save ─────────────────────────────────────────────────────────────────────

print("\nSaving weekend bot data...")
for bot in botlist:
    bot.save_bot_data()

print("\nDone.")

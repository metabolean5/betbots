#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
BetBots WCQ Verify Arena – UEFA World Cup Qualifiers
====================================================
Run after the WCQ matchday to verify all bets,
update each bot's money/stats, and show combined standings.

Usage:
    python3 verify_arena_wcq.py
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

UCL_DATA = {
    "01": "bots_data/01_billybayes.json",
    "02": "bots_data/02_risky_rifky.json",
    "03": "bots_data/03_pat_nostat.json",
    "04": "bots_data/04_risky_vent_dof.json",
    "05": "bots_data/05_vent_dof.json",
    "06": "bots_data/06_valeur_darb.json",
}

WKD_DATA = {
    "01": "bots_data/01_billybayes_wkd.json",
    "02": "bots_data/02_risky_rifky_wkd.json",
    "03": "bots_data/03_pat_nostat_wkd.json",
    "04": "bots_data/04_risky_vent_dof_wkd.json",
    "05": "bots_data/05_vent_dof_wkd.json",
    "06": "bots_data/06_valeur_darb_wkd.json",
}

print("=" * 60)
print("  BETBOTS WCQ VERIFY  –  UEFA WC QUALIFIERS")
print("=" * 60)

billy_bayes       = Betbot("Billy Bayes",        "classifiers/billy_bayes.pkl", WCQ_DATA["01"], "01")
risky_rifki       = Betbot("Risky Rifki",         "classifiers/billy_bayes.pkl", WCQ_DATA["02"], "02")
pat_nostat        = Betbot("Pat Nostat",           "none", WCQ_DATA["03"], "03")
risky_vent_dofsky = Betbot("Risky Vent d'Ofsky",  "none", WCQ_DATA["04"], "04")
vent_dofsky       = Betbot("Vent d'Ofsky",         "none", WCQ_DATA["05"], "05")
way_to_claude     = Betbot("Way to Claude",        "none", WCQ_DATA["06"], "06")

botlist = [billy_bayes, risky_rifki, pat_nostat, risky_vent_dofsky, vent_dofsky, way_to_claude]

# ─── Build API-Football team cache from confirmed bets ────────────────────────

print("\nBuilding API-Football team cache from confirmed bets...")
all_team_names = set()
for bot in botlist:
    for key, val in bot.getMemory().get("confirmed_bets", {}).items():
        if key == "potential_gain":
            continue
        teams_str = val.get("bet_data", {}).get("info", {}).get("teams", "")
        if " vs " in teams_str:
            h, a = teams_str.split(" vs ", 1)
            all_team_names.add(h.strip())
            all_team_names.add(a.strip())

if all_team_names:
    _build_af_team_cache(list(all_team_names))
else:
    print("  No confirmed bets found to verify.")


# ─── Verification logic ───────────────────────────────────────────────────────

def verify_bot(bot):
    print(f"\n  --- {bot.getName()} ---")
    mem  = bot.getMemory()
    bets = mem.get("confirmed_bets", {})

    if not bets:
        print("  No confirmed bets.")
        return

    if bot.id in ("04", "05"):
        real_bets = {k: v for k, v in bets.items() if k != "potential_gain"}
        if not real_bets:
            print(f"  → No bets placed this round, skipping.")
            return
        all_won = True
        for key, val in real_bets.items():
            if not verify_bet_wcq(val, key):
                all_won = False
        if all_won:
            gain = bets.get("potential_gain", 0)
            mem["money"] += gain
            mem["successful_bets"] += 1
            print(f"  → COMBINED BET WON  +€{gain:.2f}")
        else:
            mem["unsuccessful_bets"] += 1
            print(f"  → Combined bet LOST")
        return

    for key, val in bets.items():
        match_name = val.get("bet_data", {}).get("info", {}).get("teams", f"bet {key}")
        if verify_bet_wcq(val, key):
            gain = val.get("potential_gain", 0)
            mem["money"] += gain
            mem["successful_bets"] += 1
            val["result"] = "won"
            print(f"  → {match_name}: WON +€{gain:.2f}")
        else:
            mem["unsuccessful_bets"] += 1
            val["result"] = "lost"
            print(f"  → {match_name}: Lost")


# ─── Run verification ─────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("  VERIFYING WCQ BETS")
print("=" * 60)

for bot in botlist:
    verify_bot(bot)

# ─── Combined standings (UCL + WKD + WCQ) ────────────────────────────────────

print("\n" + "=" * 60)
print("  COMBINED STANDINGS (UCL + WEEKEND + WCQ)")
print("=" * 60)

combined = {}
for idn in WCQ_DATA:
    wcq  = json.load(open(WCQ_DATA[idn]))
    ucl  = json.load(open(UCL_DATA[idn]))
    wkd  = json.load(open(WKD_DATA[idn]))
    name = [b.getName() for b in botlist if b.id == idn][0]
    combined[name] = {
        "money":      ucl["money"] + wkd["money"] + wcq["money"],
        "bets_won":   ucl["successful_bets"] + wkd["successful_bets"] + wcq["successful_bets"],
        "bets_lost":  ucl["unsuccessful_bets"] + wkd["unsuccessful_bets"] + wcq["unsuccessful_bets"],
        "total_bets": ucl["total_bets_made"] + wkd["total_bets_made"] + wcq["total_bets_made"],
    }

sorted_bots = sorted(combined.items(), key=lambda x: x[1]["money"], reverse=True)

print(f"\n{'Rank':<5} {'Bot':<22} {'Money':>9} {'Won':>5} {'Lost':>6} {'Total':>7}")
print("-" * 58)
for rank, (name, stats) in enumerate(sorted_bots, 1):
    money_str = f"€{stats['money']:+.2f}"
    print(f"{rank:<5} {name:<22} {money_str:>9} {stats['bets_won']:>5} {stats['bets_lost']:>6} {stats['total_bets']:>7}")

# ─── Save ─────────────────────────────────────────────────────────────────────

print("\nSaving WCQ bot data...")
for bot in botlist:
    bot.save_bot_data()
print("Done.")

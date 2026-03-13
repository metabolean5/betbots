#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
BetBots Weekend Verify Arena – EPL / Ligue 1
=============================================
Run on Monday after the weekend matches to verify all weekend bets,
update each bot's money/stats, save, and update the README leaderboard.

Usage:
    python3 verify_arena_weekend.py
"""
__author__ = "mpdev"

import json
import re
import pprint as pp
import joblib

exec(open("Betbot.py").read())

WKD_DATA = {
    "01": "bots_data/01_billybayes_wkd.json",
    "02": "bots_data/02_risky_rifky_wkd.json",
    "03": "bots_data/03_pat_nostat_wkd.json",
    "04": "bots_data/04_risky_vent_dof_wkd.json",
    "05": "bots_data/05_vent_dof_wkd.json",
    "06": "bots_data/06_valeur_darb_wkd.json",
}

UCL_DATA = {
    "01": "bots_data/01_billybayes.json",
    "02": "bots_data/02_risky_rifky.json",
    "03": "bots_data/03_pat_nostat.json",
    "04": "bots_data/04_risky_vent_dof.json",
    "05": "bots_data/05_vent_dof.json",
    "06": "bots_data/06_valeur_darb.json",
}

print("=" * 60)
print("  BETBOTS WEEKEND VERIFY  –  EPL / LIGUE 1")
print("=" * 60)

billy_bayes       = Betbot("Billy Bayes",        "classifiers/billy_bayes.pkl", WKD_DATA["01"], "01")
risky_rifki       = Betbot("Risky Rifki",         "classifiers/billy_bayes.pkl", WKD_DATA["02"], "02")
pat_nostat        = Betbot("Pat Nostat",           "none", WKD_DATA["03"], "03")
risky_vent_dofsky = Betbot("Risky Vent d'Ofsky",  "none", WKD_DATA["04"], "04")
vent_dofsky       = Betbot("Vent d'Ofsky",         "none", WKD_DATA["05"], "05")
way_to_claude     = Betbot("Way to Claude",        "none", WKD_DATA["06"], "06")

botlist = [billy_bayes, risky_rifki, pat_nostat, risky_vent_dofsky, vent_dofsky, way_to_claude]

print("\nBuilding team-ID cache...")
_build_team_cache()

_match_result_cache = {}

def verify_bet_robust(bet_obj, betkey):
    try:
        bd         = bet_obj["bet_data"]
        home_name, away_name = bd["info"]["teams"].split(" vs ", 1)
        date_str   = bd["info"].get("date", "")[:10]
        prediction = int(bd.get("prediction", -1))

        home_fd = _team_cache.get(_norm(home_name))
        away_fd = _team_cache.get(_norm(away_name))

        if not home_fd:
            print(f"  [warn] Cannot map home '{home_name}'.")
            return False
        if not away_fd:
            print(f"  [warn] Cannot map away '{away_name}'.")
            return False

        cache_key = (home_fd, away_fd, date_str)
        if cache_key in _match_result_cache:
            truth = _match_result_cache[cache_key]
            if truth is None:
                print(f"  Not finished yet (cached).")
                return False
            print(f"  {bd['info']['teams']} | truth={truth} prediction={prediction} (cached)")
            return prediction == truth

        data    = _fd_get(f"/teams/{home_fd}/matches",
                          params={"status": "FINISHED", "limit": 30})
        for m in data.get("matches", []):
            if m.get("utcDate", "")[:10] != date_str:
                continue
            if m["awayTeam"]["id"] != away_fd:
                continue
            ft = m.get("score", {}).get("fullTime", {})
            h, a = ft.get("home"), ft.get("away")
            if h is None or a is None:
                _match_result_cache[cache_key] = None
                print(f"  Match not finished yet.")
                return False
            truth = 3 if h > a else (1 if h == a else 0)
            _match_result_cache[cache_key] = truth
            print(f"  {m['homeTeam']['name']} {h}–{a} {m['awayTeam']['name']}"
                  f"  | truth={truth} prediction={prediction}")
            return prediction == truth

        print(f"  Result not found for '{bd['info']['teams']}' on {date_str}.")
        return False
    except Exception as e:
        print(f"  [error] {betkey}: {e}")
        return False


def verify_bot(bot):
    print(f"\n  --- {bot.getName()} ---")
    mem  = bot.getMemory()
    bets = mem["confirmed_bets"]

    if bot.id in ("04", "05"):
        all_won = True
        for key, val in bets.items():
            if key == "potential_gain":
                continue
            if not verify_bet_robust(val, key):
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
        if verify_bet_robust(val, key):
            gain = val.get("potential_gain", 0)
            mem["money"] += gain
            mem["successful_bets"] += 1
            print(f"  → WON +€{gain:.2f}")
        else:
            mem["unsuccessful_bets"] += 1
            print(f"  → Lost")


print("\n" + "=" * 60)
print("  VERIFYING WEEKEND BETS")
print("=" * 60)

for bot in botlist:
    verify_bot(bot)

# ─── Combined standings (UCL + weekend) ───────────────────────────────────────

print("\n" + "=" * 60)
print("  COMBINED STANDINGS (UCL + WEEKEND)")
print("=" * 60)

combined = {}
for idn, wkd_path in WKD_DATA.items():
    ucl_path = UCL_DATA[idn]
    wkd = json.load(open(wkd_path))
    ucl = json.load(open(ucl_path))
    name = [b.getName() for b in botlist if b.id == idn][0]
    combined[name] = {
        "money":      ucl["money"] + wkd["money"],
        "bets_won":   ucl["successful_bets"] + wkd["successful_bets"],
        "bets_lost":  ucl["unsuccessful_bets"] + wkd["unsuccessful_bets"],
        "total_bets": ucl["total_bets_made"] + wkd["total_bets_made"],
    }

sorted_bots = sorted(combined.items(), key=lambda x: x[1]["money"], reverse=True)

print(f"\n{'Rank':<5} {'Bot':<22} {'Money':>9} {'Won':>5} {'Lost':>6} {'Total':>7}")
print("-" * 58)
for rank, (name, stats) in enumerate(sorted_bots, 1):
    money_str = f"€{stats['money']:+.2f}"
    print(f"{rank:<5} {name:<22} {money_str:>9} {stats['bets_won']:>5} {stats['bets_lost']:>6} {stats['total_bets']:>7}")

# ─── Save ─────────────────────────────────────────────────────────────────────

print("\nSaving weekend bot data...")
for bot in botlist:
    bot.save_bot_data()
print("Done.")

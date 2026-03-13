#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
BetBots Arena – Bet Verification
=================================
Run this script after matches have finished to verify all confirmed bets,
update each bot's money/stats, save the results, and update the README
with a leaderboard.

Usage:
    python3 verify_arena.py
"""
__author__ = "mpdev"

import json
import re
import pprint as pp
import joblib

exec(open("Betbot.py").read())


# ─── Load bots ────────────────────────────────────────────────────────────────

print("=" * 60)
print("  BETBOTS VERIFY ARENA  –  UCL / UEL / UECL")
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
risky_vent_dofsky = Betbot("Risky Vent d'Ofsky",
                            "none",
                            "bots_data/04_risky_vent_dof.json","04")
vent_dofsky       = Betbot("Vent d'Ofsky",
                            "none",
                            "bots_data/05_vent_dof.json",      "05")
way_to_claude     = Betbot("Way to Claude",
                            "none",
                            "bots_data/06_valeur_darb.json",   "06")

botlist = [billy_bayes, risky_rifki, pat_nostat, risky_vent_dofsky, vent_dofsky, way_to_claude]


# ─── Build team cache ─────────────────────────────────────────────────────────

print("\nBuilding team-ID cache from football-data.org...")
_build_team_cache()


# ─── Robust bet verification (matches by team ID, not name string) ─────────────

_match_result_cache = {}  # (home_fd_id, date_str) -> truth (3/1/0) or None

def verify_bet_robust(bet_obj, betkey):
    """
    Like betSuccess() but matches the away team by football-data.org ID
    rather than normalised name string — avoids "Liverpool" vs "Liverpool FC".
    """
    try:
        bd        = bet_obj["bet_data"]
        teams_str = bd["info"]["teams"]
        home_name, away_name = teams_str.split(" vs ", 1)
        date_str  = bd["info"].get("date", "")[:10]
        prediction = int(bd.get("prediction", -1))

        home_norm = _norm(home_name)
        away_norm = _norm(away_name)
        home_fd   = _team_cache.get(home_norm)
        away_fd   = _team_cache.get(away_norm)

        if not home_fd:
            print(f"  [warn] Cannot map home team '{home_name}' to a FD ID.")
            return False
        if not away_fd:
            print(f"  [warn] Cannot map away team '{away_name}' to a FD ID.")
            return False

        # Check result cache first
        cache_key = (home_fd, away_fd, date_str)
        if cache_key in _match_result_cache:
            truth = _match_result_cache[cache_key]
            if truth is None:
                print(f"  Match not finished (cached).")
                return False
            print(f"  {teams_str} | truth={truth} prediction={prediction} (cached)")
            return prediction == truth

        data    = _fd_get(f"/teams/{home_fd}/matches",
                          params={"status": "FINISHED", "limit": 30})
        matches = data.get("matches", [])

        for m in matches:
            if m.get("utcDate", "")[:10] != date_str:
                continue
            if m["awayTeam"]["id"] != away_fd:
                continue
            ft   = m.get("score", {}).get("fullTime", {})
            h    = ft.get("home")
            a    = ft.get("away")
            if h is None or a is None:
                print(f"  Match not yet finished.")
                _match_result_cache[cache_key] = None
                return False
            truth = 3 if h > a else (1 if h == a else 0)
            _match_result_cache[cache_key] = truth
            print(f"  {m['homeTeam']['name']} {h}–{a} {m['awayTeam']['name']}"
                  f"  | truth={truth} prediction={prediction}")
            return prediction == truth

        print(f"  Could not find finished result for '{teams_str}' on {date_str}.")
        return False

    except Exception as e:
        print(f"  [error] verify_bet_robust({betkey}): {e}")
        return False


def verify_bot(bot):
    """Verify all confirmed bets for a bot and update its money/stats."""
    print(f"\n  --- {bot.getName()} ---")
    mem  = bot.getMemory()
    bets = mem["confirmed_bets"]

    # ── combined-bet bots (04, 05) ──────────────────────────────────────────
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

    # ── individual-bet bots (01, 02, 03, 06) ────────────────────────────────
    for key, val in bets.items():
        if verify_bet_robust(val, key):
            gain = val.get("potential_gain", 0)
            mem["money"] += gain
            mem["successful_bets"] += 1
            print(f"  → WON +€{gain:.2f}")
        else:
            mem["unsuccessful_bets"] += 1
            print(f"  → Lost")


# ─── Run verification ─────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("  VERIFYING BETS")
print("=" * 60)

for bot in botlist:
    verify_bot(bot)


# ─── Rankings ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("  PERFORMANCE RANKINGS")
print("=" * 60)

results = {}
for bot in botlist:
    mem = bot.getMemory()
    results[bot.getName()] = {
        "money":      mem["money"],
        "bets_won":   mem["successful_bets"],
        "bets_lost":  mem["unsuccessful_bets"],
        "total_bets": mem["total_bets_made"],
    }

sorted_bots = sorted(results.items(), key=lambda x: x[1]["money"], reverse=True)

print(f"\n{'Rank':<5} {'Bot':<22} {'Money':>9} {'Won':>5} {'Lost':>6} {'Total':>7}")
print("-" * 58)
for rank, (name, stats) in enumerate(sorted_bots, 1):
    money_str = f"€{stats['money']:+.2f}"
    print(f"{rank:<5} {name:<22} {money_str:>9} {stats['bets_won']:>5} {stats['bets_lost']:>6} {stats['total_bets']:>7}")


# ─── Save updated bot data ────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("Saving updated bot data...")
for bot in botlist:
    bot.save_bot_data()
print("All bots saved.")


# ─── Update README with leaderboard ──────────────────────────────────────────

print("\nUpdating README.md with leaderboard...")

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

medal = {1: "🥇", 2: "🥈", 3: "🥉"}

leaderboard_lines = [
    "## Classement Saison 3 – R16 (10–12 mars 2026)\n",
    "\n",
    "| Rang | Bot | Mise totale | Argent | Paris gagnés | Paris perdus |\n",
    "|------|-----|------------|--------|--------------|---------------|\n",
]

# Compute total stake per bot (money is always negative = stakes spent)
stakes = {
    "Billy Bayes":         70,
    "Risky Rifki":        100,
    "Pat Nostat":          50,
    "Risky Vent d'Ofsky":  15,
    "Vent d'Ofsky":        20,
    "Way to Claude":      260,
}

for rank, (name, stats) in enumerate(sorted_bots, 1):
    m     = medal.get(rank, f"#{rank}")
    money = stats["money"]
    stake = stakes.get(name, "?")
    sign  = "+" if money >= 0 else ""
    leaderboard_lines.append(
        f"| {m} | **{name}** | €{stake} | **€{sign}{money:.2f}** "
        f"| {stats['bets_won']} | {stats['bets_lost']} |\n"
    )

leaderboard_lines.append("\n")
leaderboard = "".join(leaderboard_lines)

MARKER_START  = "## Classement Saison 3"
MARKER_INSERT = "## Archives"

if MARKER_START in content:
    content = re.sub(
        r"## Classement Saison 3.*?(?=\n## |\Z)",
        leaderboard.rstrip(),
        content,
        flags=re.DOTALL,
    )
else:
    content = content.replace(
        "## Archives\n",
        leaderboard + "## Archives\n",
    )

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("README.md updated.")
print("\nDone.")

#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "mpdev"
__copyright__ = "Copyright 2026, Turfutoday's Betbots"
__license__ = "CC BY-SA 2.0 FR"

"""
Data sources
────────────
Fixtures  : The Odds API  (all 3 comps)   https://the-odds-api.com
Odds      : The Odds API                   same key
Form      : football-data.org             https://www.football-data.org

Keys are loaded from config.json.
"""

import requests
import json
import datetime
import time
import os
import unicodedata
import pandas as pd
import pprint as pp


# ─── Keys ─────────────────────────────────────────────────────────────────────

_cfg = {}
if os.path.exists("config.json"):
    with open("config.json") as _f:
        _cfg = json.load(_f)

FOOTBALL_DATA_KEY = _cfg.get("FOOTBALL_DATA_KEY", "")
ODDS_API_KEY      = _cfg.get("ODDS_API_KEY", "")

FD_BASE   = "https://api.football-data.org/v4"
ODDS_BASE = "https://api.the-odds-api.com/v4"

FD_HEADERS = {"X-Auth-Token": FOOTBALL_DATA_KEY}

# Competitions available in football-data.org free tier
# Used to build team-ID lookup for form data
FD_TEAM_SOURCES = ["CL", "PL", "PD", "BL1", "SA", "FL1", "DED", "PPL"]

# The Odds API sport keys
ODDS_SPORTS = {
    "UCL":  "soccer_uefa_champs_league",
    "UEL":  "soccer_uefa_europa_league",
    "UECL": "soccer_uefa_europa_conference_league",
}

COMP_NAMES = {
    "UCL":  "UEFA Champions League",
    "UEL":  "UEFA Europa League",
    "UECL": "UEFA Conference League",
}


# ─── Low-level helpers ────────────────────────────────────────────────────────

def _fd_get(path, params=None):
    url  = FD_BASE + path
    resp = requests.get(url, headers=FD_HEADERS, params=params, timeout=20)
    if resp.status_code == 429:
        print("  [rate-limit] football-data.org – waiting 65s...")
        time.sleep(65)
        resp = requests.get(url, headers=FD_HEADERS, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


def _odds_get(path, params=None):
    url  = ODDS_BASE + path
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


def _norm(name):
    """
    Normalise a team name for cross-API matching:
      1. Lowercase + strip
      2. Unicode decompose (é→e, ü→u, á→a, ø→o …)
      3. Manual aliases for genuinely different names across APIs
    """
    n = name.lower().strip()
    # Strip diacritics (é→e, ü→u, ó→o, etc.)
    n = unicodedata.normalize('NFD', n)
    n = ''.join(c for c in n if not unicodedata.combining(c))
    n = n.replace('\u00f8', 'o')   # ø → o (doesn't decompose via NFD)

    aliases = {
        # ── Mismatches between The Odds API and football-data.org ──────────
        "bayern munich":   "bayern",             # "Bayern Munich" → shortName cache key
        "paris saint germain": "psg",           # Odds has no hyphen
        "sporting lisbon":  "sporting cp",      # Odds uses English city name
        "fc barcelona": "barcelona",
        "paris saint-germain fc": "psg",
        "paris saint-germain": "psg",
        "paris sg": "psg",
        "bayer 04 leverkusen": "bayer leverkusen",
        "club atlético de madrid": "atletico madrid",
        "atletico madrid": "atletico madrid",
        "atlético madrid": "atletico madrid",
        "manchester city fc": "manchester city",
        "manchester united fc": "manchester united",
        "tottenham hotspur fc": "tottenham",
        "tottenham hotspur": "tottenham",
        "newcastle united fc": "newcastle",
        "newcastle united": "newcastle",
        "nottingham forest fc": "nottingham forest",
        "bologna fc 1909": "bologna",
        "lille osc": "lille",
        "losc lille": "lille",
        "sporting clube de portugal": "sporting cp",
        "fk bodø/glimt": "bodo/glimt",
        "galatasaray sk": "galatasaray",
        "atalanta bc": "atalanta",
        "fc porto": "porto",
        "sc braga": "braga",
        "vfb stuttgart": "stuttgart",
        "sc freiburg": "freiburg",
        "as roma": "roma",
        "aston villa fc": "aston villa",
        "vv st. truiden": "st truiden",
        "panathinaikos fc": "panathinaikos",
        "real betis balompié": "real betis",
        "rc celta de vigo": "celta vigo",
        "olympique lyonnais": "lyon",
        "fc midtjylland": "midtjylland",
        "krc genk": "genk",
        "fc ferencváros": "ferencvaros",
        "ferencvárosi tc": "ferencvaros",
        "az alkmaar": "az",
        "fiorentina": "fiorentina",
        "crystal palace fc": "crystal palace",
        "rc strasbourg alsace": "strasbourg",
        "1. fsv mainz 05": "mainz",
        "mainz 05": "mainz",
        "kks lech poznań": "lech poznan",
        "lech poznań": "lech poznan",
        "fc shakhtar donetsk": "shakhtar donetsk",
        "hnk rijeka": "rijeka",
        "nk celje": "celje",
        "aek athens fc": "aek athens",
        "sk sigma olomouc": "sigma olomouc",
        "samsunspor": "samsunspor",
        "rayo vallecano": "rayo vallecano",
        "aek larnaca fc": "aek larnaca",
        "ac sparta prague": "sparta prague",
        "raków częstochowa": "rakow czestochowa",
    }
    n = name.lower().strip()
    return aliases.get(n, n)


# ─── Team ID cache (name → football-data.org ID) ─────────────────────────────

_team_cache = {}   # _norm(name) → fd_team_id

def _build_team_cache():
    """Populate _team_cache from all accessible competitions."""
    if _team_cache:
        return
    print("  Building team-ID cache from football-data.org...")
    for code in FD_TEAM_SOURCES:
        try:
            data = _fd_get(f"/competitions/{code}/teams")
            for t in data.get("teams", []):
                for alias in [t.get("name",""), t.get("shortName",""), t.get("tla","")]:
                    if alias:
                        _team_cache[_norm(alias)] = t["id"]
            time.sleep(7)   # free-tier: 10 req/min
        except Exception as e:
            print(f"    [warn] Could not load teams for {code}: {e}")
            time.sleep(7)
    print(f"  Team cache built: {len(_team_cache)} entries")


# ─── Form data ────────────────────────────────────────────────────────────────

_form_cache = {}   # team_id → list[3/1/0]

def get_team_form(team_id, n=5):
    """Last n results for a team (3=W, 1=D, 0=L), most recent first."""
    if team_id in _form_cache:
        return _form_cache[team_id]
    try:
        data    = _fd_get(f"/teams/{team_id}/matches",
                          params={"status": "FINISHED", "limit": 10})
        matches = sorted(data.get("matches", []),
                         key=lambda m: m.get("utcDate", ""), reverse=True)
        form = []
        for m in matches:
            if len(form) >= n:
                break
            ft   = m.get("score", {}).get("fullTime", {})
            home = ft.get("home")
            away = ft.get("away")
            if home is None or away is None:
                continue
            is_home = m["homeTeam"]["id"] == team_id
            if home > away:
                form.append(3 if is_home else 0)
            elif home < away:
                form.append(0 if is_home else 3)
            else:
                form.append(1)
        time.sleep(7)
        _form_cache[team_id] = form
        return form
    except Exception as e:
        print(f"  [warn] No form for team {team_id}: {e}")
        time.sleep(7)
        return []


# ─── Main scraping function ───────────────────────────────────────────────────

def scrap_fixtures_01(competition_keys=None):
    """
    Scrape this week's UCL / UEL / UECL fixtures.

    Returns  { round_label: [ fixture, ... ] }

    Fixtures with form data for both teams go into the first round key
    (used by all bots including ML models).
    Fixtures missing form go into a second round key
    (used only by odds-based bots: Vent d'Ofsky, Risky Vent d'Ofsky).
    """
    if competition_keys is None:
        competition_keys = ["UCL", "UEL", "UECL"]

    _form_cache.clear()
    _build_team_cache()

    today     = datetime.date.today()
    week_end  = today + datetime.timedelta(days=7)
    label_date = today.strftime("%d/%m/%Y")

    with_form  = []
    odds_only  = []

    for comp_key in competition_keys:
        sport    = ODDS_SPORTS[comp_key]
        compname = COMP_NAMES[comp_key]
        print(f"\n  [{comp_key}] Fetching fixtures + odds from The Odds API...")

        try:
            games = _odds_get(f"/sports/{sport}/odds/", params={
                "apiKey":     ODDS_API_KEY,
                "regions":    "eu",
                "markets":    "h2h",
                "oddsFormat": "decimal",
                "dateFormat": "iso",
            })
        except Exception as e:
            print(f"  [error] Could not fetch {comp_key} odds: {e}")
            continue

        for game in games:
            # Filter to this week
            commence = game.get("commence_time", "")
            if commence:
                try:
                    match_date = datetime.date.fromisoformat(commence[:10])
                    if not (today <= match_date <= week_end):
                        continue
                except:
                    pass

            home_name = game.get("home_team", "")
            away_name = game.get("away_team", "")
            event_id  = game.get("id", "")
            commence_str = commence[:16].replace("T", " ") if commence else ""

            # Parse 1X2 odds (first EU bookmaker)
            odds = {"3": "2.00", "1": "3.50", "0": "3.00"}
            for bm in game.get("bookmakers", []):
                for mkt in bm.get("markets", []):
                    if mkt.get("key") != "h2h":
                        continue
                    out = {o["name"]: o["price"] for o in mkt.get("outcomes", [])}
                    h = out.get(home_name, 2.00)
                    a = out.get(away_name, 3.00)
                    d = next((v for k, v in out.items()
                               if k not in (home_name, away_name)), 3.50)
                    odds = {
                        "3": str(round(h, 2)),
                        "1": str(round(d, 2)),
                        "0": str(round(a, 2)),
                    }
                    break
                break

            match_str  = f"{home_name} vs {away_name}"
            home_norm  = _norm(home_name)
            away_norm  = _norm(away_name)
            home_fd_id = _team_cache.get(home_norm)
            away_fd_id = _team_cache.get(away_norm)

            # Get form if both team IDs are known
            last5vec = []
            if home_fd_id and away_fd_id:
                h_form = get_team_form(home_fd_id)
                a_form = get_team_form(away_fd_id)
                last5vec = h_form[:5] + a_form[:5]

            fixture = {
                "event_id": event_id,
                "cotes":    odds,
                "info": {
                    "teams":       match_str,
                    "competition": compname,
                    "date":        commence_str,
                },
                "last5vec": last5vec,
            }

            if len(last5vec) >= 6:
                print(f"    ✓ {match_str}  (form OK, odds {odds['3']}/{odds['1']}/{odds['0']})")
                with_form.append(fixture)
            else:
                print(f"    ~ {match_str}  (no form, odds only)")
                odds_only.append(fixture)

    if not with_form and not odds_only:
        print("No fixtures found for this week.")
        return {}

    result = {}
    if with_form:
        result[f"European R16 – {label_date}"] = with_form
    if odds_only:
        result[f"European R16 odds-only – {label_date}"] = odds_only

    print(f"\n  Ready: {len(with_form)} with form, {len(odds_only)} odds-only.")
    return result


# ─── Result verification ──────────────────────────────────────────────────────

def betSuccess(bet, betkey, urlround=None):
    """
    Verify a past bet via football-data.org using the stored event_id
    (which is the football-data.org match ID if available, otherwise skip).
    """
    try:
        match_id = bet["bet_data"].get("event_id") or bet["bet_data"].get("match_id")
        if not match_id:
            print(f"  [warn] No match ID for bet {betkey}.")
            return False

        # The Odds API event_id is a string, not a football-data.org integer ID.
        # For verification we need to find the match in football-data.org by teams + date.
        home_name = bet["bet_data"]["info"]["teams"].split(" vs ")[0]
        away_name = bet["bet_data"]["info"]["teams"].split(" vs ")[1]
        date_str  = bet["bet_data"]["info"].get("date", "")[:10]

        home_norm = _norm(home_name)
        away_norm = _norm(away_name)
        home_fd   = _team_cache.get(home_norm)
        if not home_fd:
            print(f"  [warn] Cannot map '{home_name}' to a football-data.org team ID.")
            return False

        data    = _fd_get(f"/teams/{home_fd}/matches",
                          params={"status": "FINISHED", "limit": 20})
        matches = data.get("matches", [])
        for m in matches:
            if m.get("utcDate", "")[:10] != date_str:
                continue
            away_in_match = _norm(m["awayTeam"]["name"])
            if away_in_match != away_norm:
                continue
            ft   = m.get("score", {}).get("fullTime", {})
            home = ft.get("home")
            away = ft.get("away")
            if home is None or away is None:
                print("  Match not yet finished.")
                return False
            truth      = 3 if home > away else (1 if home == away else 0)
            prediction = int(bet["bet_data"].get("prediction", -1))
            print(f"  {m['homeTeam']['name']} {home}–{away} {m['awayTeam']['name']}"
                  f" | truth={truth} prediction={prediction}")
            return prediction == truth

        print(f"  Could not find finished result for bet {betkey}.")
        return False

    except Exception as e:
        print(f"  [error] Verify bet {betkey}: {e}")
        return False


# ─── Rankings ─────────────────────────────────────────────────────────────────

def printClassification(botlist):
    botdic = {}
    for bot in botlist:
        botdic[bot.getName()] = {
            "money":           bot.getMemory()["money"],
            "successful bets": bot.getMemory()["successful_bets"],
            "failed bets":     bot.getMemory()["unsuccessful_bets"],
        }

    df = pd.DataFrame(botdic).T
    df = df.sort_values(by=["money"], ascending=False)

    with open("betbot.html", "a") as htmlfile:
        htmlfile.write("<p></p>")
        htmlfile.write(df.to_html(classes="redTable"))

    print("\n--- RANKINGS ---")
    pp.pprint(botdic)

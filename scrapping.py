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
AF_API_KEY = _cfg.get("API_FOOTBALL_KEY", "")
AF_BASE    = "https://v3.football.api-sports.io"
AF_HEADERS = {"x-apisports-key": AF_API_KEY}

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
    "EPL":  "soccer_epl",
    "FL1":  "soccer_france_ligue_one",
    "WCQ":  "soccer_fifa_world_cup_qualifiers_europe",
}

COMP_NAMES = {
    "UCL":  "UEFA Champions League",
    "UEL":  "UEFA Europa League",
    "UECL": "UEFA Conference League",
    "EPL":  "Premier League",
    "FL1":  "Ligue 1",
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


def _af_get(path, params=None):
    url  = AF_BASE + path
    resp = requests.get(url, headers=AF_HEADERS, params=params, timeout=20)
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
        "club atletico de madrid": "atletico madrid",
        "atletico madrid": "atletico madrid",
        "atletico madrid": "atletico madrid",
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
        "fk bodo/glimt": "bodo/glimt",
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
        "real betis balompie": "real betis",
        "rc celta de vigo": "celta vigo",
        "olympique lyonnais": "lyon",
        "fc midtjylland": "midtjylland",
        "krc genk": "genk",
        "fc ferencvaros": "ferencvaros",
        "ferencvarosi tc": "ferencvaros",
        "az alkmaar": "az",
        "fiorentina": "fiorentina",
        "crystal palace fc": "crystal palace",
        "rc strasbourg alsace": "strasbourg",
        "1. fsv mainz 05": "mainz",
        "mainz 05": "mainz",
        "kks lech poznan": "lech poznan",
        "lech poznan": "lech poznan",
        "fc shakhtar donetsk": "shakhtar donetsk",
        "hnk rijeka": "rijeka",
        "nk celje": "celje",
        "aek athens fc": "aek athens",
        "sk sigma olomouc": "sigma olomouc",
        "samsunspor": "samsunspor",
        "rayo vallecano": "rayo vallecano",
        "aek larnaca fc": "aek larnaca",
        "ac sparta prague": "sparta prague",
        "rakow czestochowa": "rakow czestochowa",
    }
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


# ─── API-Football (api-sports.io) — national teams ───────────────────────────

_AF_NAME_ALIASES = {
    "bosnia & herzegovina": "bosnia",
    "bosnia and herzegovina": "bosnia",
    "north macedonia":      "north macedonia",
    "northern ireland":     "northern ireland",
    "czechia":              "czech republic",
    "ireland":              "republic of ireland",
    "turkiye":              "turkey",
}

_af_team_cache  = {}   # _norm(name) → api-football team ID
_af_form_cache  = {}   # team_id → list[3/1/0]
_af_result_cache = {}  # (norm_home, norm_away, date_str) → truth or None


def _build_af_team_cache(team_names):
    """Look up API-Football IDs for a list of national team names (one API call each)."""
    for name in team_names:
        key = _norm(name)
        if key in _af_team_cache:
            continue
        search_name = _AF_NAME_ALIASES.get(key, name)
        print(f"  [AF] Searching: {search_name}")
        try:
            data = _af_get("/teams", params={"search": search_name})
            found = False
            for item in data.get("response", []):
                t = item.get("team", {})
                if not t.get("national"):
                    continue
                # Skip youth / women teams (contain "U17", "U21", " W", etc.)
                if any(x in t.get("name", "") for x in [" U1", " U2", " U3", " W "]):
                    continue
                _af_team_cache[key] = t["id"]
                print(f"    → id={t['id']} ({t['name']})")
                found = True
                break
            if not found:
                print(f"    → not found")
        except Exception as e:
            print(f"    → [error] {e}")
        time.sleep(7)


def get_team_form_af(team_id, n=5):
    """Last n match results for a national team via API-Football (3=W, 1=D, 0=L)."""
    if team_id in _af_form_cache:
        return _af_form_cache[team_id]
    try:
        data    = _af_get("/fixtures", params={"team": team_id, "season": 2024})
        matches = sorted(
            data.get("response", []),
            key=lambda m: m["fixture"]["date"],
            reverse=True,
        )
        form = []
        for m in matches:
            if len(form) >= n:
                break
            if m["fixture"]["status"]["short"] != "FT":
                continue
            h = m["goals"]["home"]
            a = m["goals"]["away"]
            if h is None or a is None:
                continue
            is_home = m["teams"]["home"]["id"] == team_id
            if h > a:
                form.append(3 if is_home else 0)
            elif h < a:
                form.append(0 if is_home else 3)
            else:
                form.append(1)
        time.sleep(7)
        _af_form_cache[team_id] = form
        return form
    except Exception as e:
        print(f"  [warn] No AF form for team {team_id}: {e}")
        time.sleep(7)
        return []


def scrap_fixtures_wcq(cutoff_dt=None):
    """
    Scrape WCQ Europe fixtures up to cutoff_dt.
    Fixtures + odds from The Odds API; form from API-Football.
    Returns { round_label: [ fixture, ... ] }
    """
    today = datetime.date.today()
    if cutoff_dt is None:
        cutoff_dt = datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(days=8)

    _af_form_cache.clear()
    label_date = today.strftime("%d/%m/%Y")

    print(f"\n  [WCQ] Fetching fixtures + odds from The Odds API...")
    try:
        games = _odds_get("/sports/soccer_fifa_world_cup_qualifiers_europe/odds/", params={
            "apiKey":     ODDS_API_KEY,
            "regions":    "eu",
            "markets":    "h2h",
            "oddsFormat": "decimal",
            "dateFormat": "iso",
        })
    except Exception as e:
        print(f"  [error] Could not fetch WCQ odds: {e}")
        return {}

    upcoming = []
    today_dt  = datetime.datetime(today.year, today.month, today.day)
    for g in games:
        commence = g.get("commence_time", "")
        if not commence:
            continue
        try:
            dt = datetime.datetime.fromisoformat(commence.replace("Z", "+00:00")).replace(tzinfo=None)
            if today_dt <= dt < cutoff_dt:
                upcoming.append((dt, g))
        except Exception:
            pass

    if not upcoming:
        print("  No WCQ fixtures found in the given date range.")
        return {}

    # Build API-Football team ID cache for all involved teams
    all_names = list({name for _, g in upcoming for name in (g["home_team"], g["away_team"])})
    print(f"\n  [WCQ] Looking up {len(all_names)} national team IDs via API-Football...")
    _build_af_team_cache(all_names)

    with_form = []
    odds_only = []

    for dt, game in upcoming:
        home_name    = game["home_team"]
        away_name    = game["away_team"]
        event_id     = game["id"]
        commence_str = game["commence_time"][:16].replace("T", " ")

        # Parse odds from first EU bookmaker
        odds = {"3": "2.00", "1": "3.50", "0": "3.00"}
        for bm in game.get("bookmakers", []):
            for mkt in bm.get("markets", []):
                if mkt.get("key") != "h2h":
                    continue
                out = {o["name"]: o["price"] for o in mkt.get("outcomes", [])}
                h = out.get(home_name, 2.00)
                a = out.get(away_name, 3.00)
                d = next((v for k, v in out.items() if k not in (home_name, away_name)), 3.50)
                odds = {"3": str(round(h, 2)), "1": str(round(d, 2)), "0": str(round(a, 2))}
                break
            break

        home_af  = _af_team_cache.get(_norm(home_name))
        away_af  = _af_team_cache.get(_norm(away_name))
        last5vec = []

        if home_af and away_af:
            h_form   = get_team_form_af(home_af)
            a_form   = get_team_form_af(away_af)
            last5vec = h_form[:5] + a_form[:5]

        fixture = {
            "event_id": event_id,
            "cotes":    odds,
            "info": {
                "teams":       f"{home_name} vs {away_name}",
                "competition": "WCQ Europe",
                "date":        commence_str,
            },
            "last5vec": last5vec,
        }

        if len(last5vec) >= 6:
            print(f"    ✓ {home_name} vs {away_name}  (form OK, odds {odds['3']}/{odds['1']}/{odds['0']})")
            with_form.append(fixture)
        else:
            print(f"    ~ {home_name} vs {away_name}  (no form, odds only)")
            odds_only.append(fixture)

    result = {}
    if with_form:
        result[f"WCQ Europe – {label_date}"] = with_form
    if odds_only:
        result[f"WCQ Europe odds-only – {label_date}"] = odds_only

    print(f"\n  Ready: {len(with_form)} with form, {len(odds_only)} odds-only.")
    return result


# ─── Sportradar Gismo API ─────────────────────────────────────────────────────

SR_GISMO_BASE  = "https://stats.fn.sportradar.com/bet365/en/Europe:Berlin/gismo"
SR_HEADERS     = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Referer":    "https://s5.sir.sportradar.com/",
}
WCQ_SR_SEASON  = 127075   # FIFA WCQ UEFA 2026

# Sportradar name → The Odds API name (when they differ)
_SR_TO_ODDS = {
    "Turkiye":                "Turkey",
    "Bosnia and Herzegovina": "Bosnia & Herzegovina",
}


def _sr_get(path):
    url  = SR_GISMO_BASE + "/" + path.lstrip("/")
    resp = requests.get(url, headers=SR_HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.json()


def _sr_team_form(team_id, all_matches, n=5):
    """
    Compute last n form results for team_id from completed season matches.
    Returns list of [3=W, 1=D, 0=L], most-recent first.
    """
    now_uts = int(time.time())
    played = [
        m for m in all_matches
        if (m["teams"]["home"]["_id"] == team_id or m["teams"]["away"]["_id"] == team_id)
        and m["time"]["uts"] < now_uts
        and m.get("periods", {}).get("ft", {}).get("home") is not None
    ]
    played.sort(key=lambda m: m["time"]["uts"], reverse=True)
    form = []
    for m in played:
        if len(form) >= n:
            break
        is_home = m["teams"]["home"]["_id"] == team_id
        h = m["periods"]["ft"]["home"]
        a = m["periods"]["ft"]["away"]
        if h > a:
            form.append(3 if is_home else 0)
        elif h < a:
            form.append(0 if is_home else 3)
        else:
            form.append(1)
    return form


def scrap_fixtures_wcq_sr(days_ahead=8):
    """
    Scrape WCQ Europe upcoming fixtures via Sportradar gismo API (no browser).
    Form is computed from the season's completed matches.
    Odds are fetched from The Odds API.
    Returns { round_label: [ fixture, ... ] }
    """
    today      = datetime.date.today()
    label_date = today.strftime("%d/%m/%Y")
    now_uts    = int(time.time())
    cutoff_uts = now_uts + days_ahead * 86400

    print(f"\n  [WCQ-SR] Fetching season fixtures from Sportradar gismo API...")
    try:
        data = _sr_get(f"stats_season_fixtures2/{WCQ_SR_SEASON}/1")
    except Exception as e:
        print(f"  [error] Sportradar API failed: {e}")
        return {}

    all_matches = data["doc"][0]["data"]["matches"]

    # Upcoming real matches (exclude TBD playoff slots like "Wsf1")
    _tbd = {"Wsf1", "Wsf2", "Wsf3", "Wsf4", "Wsf5", "Wsf6", "Wsf7", "Wsf8"}
    upcoming = [
        m for m in all_matches
        if now_uts <= m["time"]["uts"] < cutoff_uts
        and m["teams"]["home"]["name"] not in _tbd
        and m["teams"]["away"]["name"] not in _tbd
    ]

    if not upcoming:
        print("  No WCQ fixtures found in the given date range.")
        return {}

    print(f"  Found {len(upcoming)} upcoming fixtures.")

    # ── Odds from The Odds API ──────────────────────────────────────────────
    print(f"\n  [WCQ-SR] Fetching odds from The Odds API...")
    odds_lookup = {}   # (_norm(home), _norm(away)) → {"3":..., "1":..., "0":...}
    try:
        games = _odds_get("/sports/soccer_fifa_world_cup_qualifiers_europe/odds/", params={
            "apiKey":     ODDS_API_KEY,
            "regions":    "eu",
            "markets":    "h2h",
            "oddsFormat": "decimal",
            "dateFormat": "iso",
        })
        for g in games:
            for bm in g.get("bookmakers", []):
                for mkt in bm.get("markets", []):
                    if mkt.get("key") != "h2h":
                        continue
                    out = {o["name"]: o["price"] for o in mkt.get("outcomes", [])}
                    hv = out.get(g["home_team"], 2.00)
                    av = out.get(g["away_team"], 3.00)
                    dv = next((v for k, v in out.items()
                               if k not in (g["home_team"], g["away_team"])), 3.50)
                    odds_lookup[(_norm(g["home_team"]), _norm(g["away_team"]))] = {
                        "3": str(round(hv, 2)),
                        "1": str(round(dv, 2)),
                        "0": str(round(av, 2)),
                    }
                    break
                break
    except Exception as e:
        print(f"  [warn] Could not fetch Odds API data: {e}")

    # ── Build fixtures ──────────────────────────────────────────────────────
    with_form = []
    odds_only = []

    for m in sorted(upcoming, key=lambda x: x["time"]["uts"]):
        sr_home  = m["teams"]["home"]["name"]
        sr_away  = m["teams"]["away"]["name"]
        home_id  = m["teams"]["home"]["_id"]
        away_id  = m["teams"]["away"]["_id"]
        match_id = str(m["_id"])

        # "26/03/26" + "18:00" → "2026-03-26 18:00"
        dd, mm, yy = m["time"]["date"].split("/")
        date_str = f"20{yy}-{mm}-{dd} {m['time']['time']}"

        # Look up odds with fallback aliases
        odds_home = _SR_TO_ODDS.get(sr_home, sr_home)
        odds_away = _SR_TO_ODDS.get(sr_away, sr_away)
        odds = odds_lookup.get((_norm(odds_home), _norm(odds_away)))
        if odds is None:
            # Fuzzy scan (substring match)
            nh, na = _norm(odds_home), _norm(odds_away)
            for (kh, ka), v in odds_lookup.items():
                if (nh in kh or kh in nh) and (na in ka or ka in na):
                    odds = v
                    break
        if odds is None:
            odds = {"3": "2.00", "1": "3.50", "0": "3.00"}

        # Form from season data
        h_form   = _sr_team_form(home_id, all_matches)
        a_form   = _sr_team_form(away_id, all_matches)
        last5vec = h_form[:5] + a_form[:5]

        fixture = {
            "event_id": match_id,
            "cotes":    odds,
            "info": {
                "teams":       f"{sr_home} vs {sr_away}",
                "competition": "WCQ Europe",
                "date":        date_str,
            },
            "last5vec": last5vec,
        }

        if len(last5vec) >= 6:
            print(f"    ✓ {sr_home} vs {sr_away}  (form OK, odds {odds['3']}/{odds['1']}/{odds['0']})")
            with_form.append(fixture)
        else:
            print(f"    ~ {sr_home} vs {sr_away}  (no form, odds only)")
            odds_only.append(fixture)

    result = {}
    if with_form:
        result[f"WCQ Europe – {label_date}"] = with_form
    if odds_only:
        result[f"WCQ Europe odds-only – {label_date}"] = odds_only

    print(f"\n  Ready: {len(with_form)} with form, {len(odds_only)} odds-only.")
    return result


def verify_bet_wcq(bet_obj, betkey):
    """Verify a WCQ bet result via API-Football."""
    try:
        bd         = bet_obj["bet_data"]
        home_name, away_name = bd["info"]["teams"].split(" vs ", 1)
        date_str   = bd["info"].get("date", "")[:10]
        prediction = int(bd.get("prediction", -1))

        cache_key = (_norm(home_name), _norm(away_name), date_str)
        if cache_key in _af_result_cache:
            truth = _af_result_cache[cache_key]
            if truth is None:
                print(f"  Not finished yet (cached).")
                return False
            print(f"  {bd['info']['teams']} | truth={truth} prediction={prediction} (cached)")
            return prediction == truth

        home_af = _af_team_cache.get(_norm(home_name))
        if not home_af:
            print(f"  [warn] No AF ID for '{home_name}' — cannot verify.")
            return False
        away_af = _af_team_cache.get(_norm(away_name))

        data = _af_get("/fixtures", params={"team": home_af, "date": date_str})
        time.sleep(7)

        for m in data.get("response", []):
            af_away_id = m["teams"]["away"]["id"]
            if away_af and af_away_id != away_af:
                continue
            if not away_af:
                if _norm(m["teams"]["away"]["name"]) != _norm(away_name):
                    continue

            status = m["fixture"]["status"]["short"]
            if status != "FT":
                _af_result_cache[cache_key] = None
                print(f"  Match not finished (status={status}).")
                return False

            h = m["goals"]["home"]
            a = m["goals"]["away"]
            if h is None or a is None:
                _af_result_cache[cache_key] = None
                print(f"  Match not finished yet.")
                return False

            truth = 3 if h > a else (1 if h == a else 0)
            _af_result_cache[cache_key] = truth
            print(f"  {m['teams']['home']['name']} {h}–{a} {m['teams']['away']['name']}"
                  f"  | truth={truth} prediction={prediction}")
            return prediction == truth

        print(f"  Result not found for '{bd['info']['teams']}' on {date_str}.")
        return False
    except Exception as e:
        print(f"  [error] {betkey}: {e}")
        return False


# ─── Main scraping function ───────────────────────────────────────────────────

def scrap_fixtures_01(competition_keys=None, round_prefix=None):
    """
    Scrape this week's fixtures for the given competition keys.

    Returns  { round_label: [ fixture, ... ] }

    Fixtures with form data for both teams go into the first round key
    (used by all bots including ML models).
    Fixtures missing form go into a second round key
    (used only by odds-based bots: Vent d'Ofsky, Risky Vent d'Ofsky).
    """
    if competition_keys is None:
        competition_keys = ["UCL"]
    if round_prefix is None:
        round_prefix = "Round"

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
        result[f"{round_prefix} – {label_date}"] = with_form
    if odds_only:
        result[f"{round_prefix} odds-only – {label_date}"] = odds_only

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

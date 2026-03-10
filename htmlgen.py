import json
import glob
import re
exec(open("Betbot.py").read())

PRED_LABELS = {3: "Home Win", 1: "Draw", 0: "Away Win"}

htmlfile = open("betbot.html", "w")
htmlfile.write(
    '<!DOCTYPE html><html><head><title>BetBots – UCL/UEL/UECL</title>'
    '<link rel="stylesheet" href="table.css"></head><body>'
    '<img style="width:400px;" src="bot_pics/betbot.png">'
)

print("Loading betting bots for HTML generation")
billy_bayes       = Betbot("Billy Bayes",       "classifiers/billy_bayes.pkl", "bots_data/01_billybayes.json",    "01")
risky_rifki       = Betbot("Risky Rifki",        "classifiers/billy_bayes.pkl", "bots_data/02_risky_rifky.json",   "02")
pat_nostat        = Betbot("Pat Nostat",          "none",                        "bots_data/03_pat_nostat.json",    "03")
vent_dofsky       = Betbot("Vent d'Ofsky",        "none",                        "bots_data/05_vent_dof.json",      "05")
risky_vent_dofsky = Betbot("Risky Vent d'Ofsky",  "none",                        "bots_data/04_risky_vent_dof.json","04")
way_to_claude     = Betbot("Way to Claude",         "none",                        "bots_data/06_valeur_darb.json",   "06")

botlist = [billy_bayes, risky_rifki, pat_nostat, risky_vent_dofsky, vent_dofsky, way_to_claude]

for bot in botlist:
    print(bot.name)
    botdic = {}
    is_combined = "potential_gain" in bot.memory["confirmed_bets"]

    for bet in bot.memory["confirmed_bets"]:
        if bet == "potential_gain":
            continue
        currbet = bot.memory["confirmed_bets"][bet]
        pred_val = currbet["bet_data"].get("prediction", -1)
        prediction = PRED_LABELS.get(int(pred_val), "Unknown")
        comp = currbet["bet_data"]["info"].get("competition", "")
        date = currbet["bet_data"]["info"].get("date", "")
        match_key = f"[{comp}] {currbet['bet_data']['info']['teams']} ({date})"

        if is_combined:
            botdic[match_key] = {"Prediction": prediction, "Potential Gain": "combined"}
        else:
            botdic[match_key] = {
                "Prediction":    prediction,
                "Potential Gain": currbet.get("potential_gain", 0),
            }

    if is_combined:
        botdic["COMBINED TOTAL"] = {
            "Prediction":    "—",
            "Potential Gain": bot.memory["confirmed_bets"]["potential_gain"],
        }

    df = pd.DataFrame(botdic).T
    htmltable = df.to_html(classes='greenTable')
    bet_type = "combined bets" if is_combined else "bets"

    htmlfile.write('<p></p>')
    htmlfile.write('<div class="dotgreen"><div class="center">')
    htmlfile.write(f'<p style="float:left;"><img src="bot_pics/{bot.id}.jpg" class="rounded"></p>')
    htmlfile.write(f'<h4><br><br>{bot.name}`s upcoming {bet_type}:</h4>')
    htmlfile.write('</div>')
    htmlfile.write(htmltable)
    htmlfile.write('</div>')

htmlfile.close()

printClassification(botlist)

htmlfile = open("betbot.html", 'a')
htmlfile.write("</body></html>")
htmlfile.close()

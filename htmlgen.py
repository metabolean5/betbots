import json
import glob, re
exec(open("Betbot.py").read())



htmlfile = open("betbot.html", "w")

htmlfile.write('<!DOCTYPE html><html><head><title>BetBots</title><link rel="stylesheet" href="table.css"></head><body><img style= "width: 400px;" src="bot_pics/betbot.png">')


#GENERATE CONFIRMED BETS TABLE


print("Loading betting bots")
billy_bayes = Betbot("Billy Bayes","classifiers/billy_bayes.pkl","bots_data/01_billybayes.json", "01")
risky_rifki = Betbot("Risky Rifki","classifiers/billy_bayes.pkl","bots_data/02_risky_rifky.json", "02")
pat_nostat = Betbot("Pat Nostat","none","bots_data/03_pat_nostat.json", "03")
vent_dofsky = Betbot("Vent d'Ofsky","none","bots_data/05_vent_dof.json", "05")
risky_vent_dofsky = Betbot("Risky Vent d'Ofsky","none","bots_data/04_risky_vent_dof.json", "04")

botlist = [
			billy_bayes,
			risky_rifki,
			pat_nostat,
			risky_vent_dofsky,
			vent_dofsky
		  ]

botdic = {}
for bot in botlist:
	print(str(bot.name))
	botdic = {}
	for bet in bot.memory["confirmed_bets"]:
		currbet = bot.memory["confirmed_bets"][bet]
		prediction = "unknown"

		if "potential_gain" not in bot.memory["confirmed_bets"]:

			print(currbet["bet_data"]["prediction"])

			if int(currbet["bet_data"]["prediction"]) == 3:
				prediction = "Home Win"
			else:
				prediction = "Away Win"

			botdic[currbet["bet_data"]["info"]["teams"]] = {"Prediction": prediction, "Potential Gain": currbet["potential_gain"] }
		else:
			if bet == "potential_gain": continue

			print(currbet["bet_data"]["prediction"])

			if int(currbet["bet_data"]["prediction"]) == 3:
				prediction = "Home Win"
			else:
				prediction = "Away Win"

			botdic[currbet["bet_data"]["info"]["teams"]] = {"Prediction": prediction, "potential gain": "0"}
		
	if "potential_gain" in bot.memory["confirmed_bets"]: #in case of combined bets
		botdic["potential_gain"] = {"potential gain":bot.memory["confirmed_bets"]["potential_gain"]}
		df = pd.DataFrame(botdic).T
		htmltable = df.to_html(classes='greenTable')
		htmlfile.write("<p></p>")
		htmlfile.write('<div class="dotgreen">')
		htmlfile.write('<div class="center">')
		htmlstr = '<p style = "float: left;">'
		htmlfile.write(htmlstr)
		htmlstr = '<img src="bot_pics/'+bot.id+'.jpg" class="rounded">' 
		htmlfile.write(htmlstr)
		htmlfile.write('</p>')
		htmlstr = '<h4> <br><br>'+bot.name+'`s upcoming combined bets are:</h4		>'
		htmlfile.write(htmlstr)
		htmlfile.write("</div>")
		htmlfile.write(htmltable)
		htmlfile.write("</div>")
	else:
		df = pd.DataFrame(botdic).T
		htmltable = df.to_html(classes='greenTable')
		htmlfile.write("<p></p>")
		htmlfile.write('<div class="dotgreen">')
		htmlfile.write('<div class="center">')
		htmlstr = '<p style = "float: left;">'
		htmlfile.write(htmlstr)
		htmlstr = '<img src="bot_pics/'+bot.id+'.jpg" class="rounded">' 
		htmlfile.write(htmlstr)
		htmlfile.write('</p>')
		htmlstr = '<h4> <br><br>'+bot.name+'`s upcoming bets are:</h4>'
		htmlfile.write(htmlstr)
		htmlfile.write("</div>")
		htmlfile.write(htmltable)
		htmlfile.write("</div>")

htmlfile.close()
printClassification(botlist)
htmlfile = open("betbot.html",'a')
htmlfile.write("</body></html>")
	#sorted_x = sorted(botdic.items(), key=operator.itemgetter(1), reverse=True)

htmlfile.close()



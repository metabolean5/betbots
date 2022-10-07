import json
import os
import glob, re
import pprint as pp
import matplotlib.pyplot as plt
import numpy as np

files = glob.glob("bots_data/*.*")
files.sort(key=os.path.getmtime)

bot_wallets = {}

for filepath in files: 

	f = open(filepath)

	jsonf = json.load(f)

	try:
		print(jsonf["money"])
	except:
		continue

	key = filepath.split('.')[0].split("/")[1].split("_")[0]
	
	if key not in bot_wallets:
		bot_wallets.setdefault(key,[jsonf["money"]])
	else:
		bot_wallets[key].append(jsonf["money"])

	bot_wallets[key].insert(0,0)



plt.title("Wallet Statistics")
plt.xlabel("Number of Bets")
plt.ylabel("Money in euros")
plt.grid()


plt.plot(list(dict.fromkeys(bot_wallets['01']))[0::2], label="Billy Bayes")
plt.plot(list(dict.fromkeys(bot_wallets['02']))[0::2],label="Risky Rifki" )
plt.plot(list(dict.fromkeys(bot_wallets['03']))[0::2],label="Pat Nostat")
plt.plot(list(dict.fromkeys(bot_wallets['04']))[0::2], label="Risky Vent d'Ofsky")
plt.plot(list(dict.fromkeys(bot_wallets['05']))[0::2], label="Vent d'Ofsky")
plt.legend(loc="upper left")

plt.show()


pp.pprint(bot_wallets)

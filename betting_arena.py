import json
import pprint as pp
import pickle
import joblib
from joblib import dump, load
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

exec(open("Betbot.py").read())

#LOADING BETTING BOTS
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


billy_bayes.makeModification2()
"""
round1 = "round/21-3" #21-3 for UCL | 21-10 for Ligue 2
billy_bayes.verifyBets(round1)
risky_rifki.verifyBets(round1)
pat_nostat.verifyBets(round1)
risky_vent_dofsky.verifyBets(round1)
vent_dofsky.verifyBets(round1)

"""



print("\nGathering fixture data for bots...")
#OPEN BETS (scrap data)
billy_bayes.get_bets(billy_bayes)
risky_rifki.get_bets(billy_bayes)
pat_nostat.get_bets(billy_bayes)
risky_vent_dofsky.get_bets(billy_bayes)
vent_dofsky.get_bets(billy_bayes)


print("\nPlacing bets...")
#PLACE BETS
billy_bayes.place_bets()
risky_rifki.place_bets()
pat_nostat.place_bets()
vent_dofsky.place_bets()
risky_vent_dofsky.place_bets()



#PRINTING AND MODIF ARENA
billy_bayes.printConfirmedBets()
risky_rifki.printConfirmedBets()
pat_nostat.printConfirmedBets()
risky_vent_dofsky.printConfirmedBets()
vent_dofsky.printConfirmedBets()



print("\n\nPERFORMANCE RANKINGS")
printClassification(botlist)


input("press enter to save")
input("presse enter if you REALLY want to save")

print("\nSaving bots data...")
#POST BET CONFIGURATIONS
risky_rifki.save_bot_data()
billy_bayes.save_bot_data()
risky_vent_dofsky.save_bot_data()
vent_dofsky.save_bot_data()
pat_nostat.save_bot_data()



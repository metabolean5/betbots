#!/usr/bin/python
# -*- coding: utf-8 -*-

exec(open('scrapping.py').read())

class Betbot:

    betbotCount = 0

    def __init__(
        self,
        name,
        modelpath,
        memorypath,
        idnum,
        ):

        try: #in case robot is new
            with open(memorypath) as json_file:
                self.memory = json.load(json_file)
        
        except:
            self.memory = {}
            self.memory.setdefault("total_bets_made", 0)
            self.memory.setdefault("successful_bets", 0)
            self.memory.setdefault("unsuccessful_bets", 0)
            self.memory["money"] = 0

        try: #in case robot does not use machine learning model
            with open(modelpath) as json_file:
                self.model = joblib.load(modelpath)  # model (sklearn classifier)
        except:
            self.model = "none"

        self.memorypath = memorypath
        self.name = name
        self.descritpion = ''
        self.id = idnum
    
        Betbot.betbotCount += 1
        print('-Loaded bot ' + name)

    def getName(self):
        return self.name


    def get_bets(self,bot):  # load bets to memory
        if self.id == '01':  # Billy Bayes
            self.memory['current_bets'] = scrap_fixtures_01("https://s5.sir.sportradar.com/bet365/en/1/season/93959/fixtures") #2022-2023

        if self.id == '02':  # Risky Rifki
            self.memory['current_bets'] = bot.getMemory()["current_bets"]

        if self.id == '03':  # Pat Nostat
            self.memory['current_bets'] = bot.getMemory()["current_bets"]

        if self.id == '04':  # Risky Vent d'Ofsky
            self.memory['current_bets'] = bot.getMemory()["current_bets"]

        if self.id == '05':  # Vent d'Ofsky
            self.memory['current_bets'] = bot.getMemory()["current_bets"]
      
    def printConfirmedBets(self):
        print(self.name + "'s bets are:\n")
        pp.pprint(self.memory["confirmed_bets"])

    def getMemory(self):
        return self.memory

    def place_bets(self):

        self.memory["confirmed_bets"] = {}

        print('-'+ self.name + ' is placing bets')
        X_bets = []

        for rounds in self.memory['current_bets']:
            for bet in self.memory['current_bets'][rounds]:
                if len(bet["last5vec"]) > 5:
                    X_bets.append(bet['last5vec'])

        y_predictions = self.model.predict(X_bets)
        try: #in case robot does not use machine learning models
            y_predictions = self.model.predict(X_bets)
            proba = self.model.predict_proba(X_bets)
        except:
            y_predictions = X_bets
            proba = []

        self.apply_strategy(y_predictions, proba)


        print(self.name +"'s predictions")
        pp.pprint(y_predictions)
        pp.pprint(proba)

    def save_bot_data(self):
        
        mempath = self.memorypath + str(datetime.datetime.now()) + ".json"

        with open(self.memorypath, 'w') as outfile:
            json.dump(self.memory, outfile, indent=4, separators=(',', ': '))

        with open("archives/" + mempath, 'w') as outfile:
            json.dump(self.memory, outfile, indent=4, separators=(',', ': '))
        pp.pprint(self.memory)
        print('\n-'+self.name + "'s data saved")

    def apply_strategy(self,y_predictions, proba):

        print(proba)


        if self.id == '01':  # Billy Bayes
            i=0
            for pb in proba:

                self.memory['current_bets'][list(self.memory["current_bets"].keys())[0]][i]["prediction"] = int(y_predictions[i])

                if max(pb) > 0.6:

                    self.memory["confirmed_bets"][i] = {'bet_data' : self.memory['current_bets'][list(self.memory["current_bets"].keys())[0]][i]}

                    if max(pb) > 0.75:
                        potential_gain =  50 * getOdds(y_predictions[i], self.memory["current_bets"][list(self.memory["current_bets"].keys())[0]][i]["cotes"])
                        self.memory["confirmed_bets"][i]["potential_gain"] = potential_gain
                        self.memory["money"] -= 50

                        print(self.name + ' just made a bet with a potential gain of: '+ str(potential_gain))

                    else:
                        potential_gain =  35 * getOdds(y_predictions[i], self.memory["current_bets"][list(self.memory["current_bets"].keys())[0]][i]["cotes"])
                        self.memory["confirmed_bets"][i]["potential_gain"] = potential_gain 
                        self.memory["money"] -= 35

                        print(self.name + ' just made a bet with a potential gain of: '+ str(potential_gain))

                    self.memory["total_bets_made"] +=1
                i+=1

        if self.id == '02':

            i=0

            for pb in proba:

                if max(pb) < 0.45:
                    self.memory["confirmed_bets"][i] = {'bet_data' : self.memory['current_bets'][list(self.memory["current_bets"].keys())[0]][i]}

                    low_confidence = list(pb).index(min(pb))

                    if low_confidence==0: low_confidence=3
                    if low_confidence==1: low_confidence=0
                    if low_confidence==2: low_confidence=1

                    self.memory['current_bets'][list(self.memory["current_bets"].keys())[0]][i]["prediction"] = int(low_confidence)

                    potential_gain = 25 *  getOdds(low_confidence, self.memory["current_bets"][list(self.memory["current_bets"].keys())[0]][i]["cotes"])

                    self.memory["confirmed_bets"][i]["potential_gain"] = potential_gain
                    self.memory["money"] -= 25

                    print(self.name + ' just made a bet with a potential gain of: '+ str(potential_gain))

                    self.memory["total_bets_made"] +=1

                i+=1

        if self.id == '03':  # Pat No stat

            i = 0
            for vec in y_predictions:

                self.memory["confirmed_bets"][i] = {'bet_data' : self.memory['current_bets'][list(self.memory["current_bets"].keys())[0]][i]}

                left=0
                right = 0 ##counting match weights according to last five
                for val in vec[0:4]:
                    left+=val
                for val in vec[5:9]:
                    right += val

                print(vec)

                print("right:"+ str(right))
                print("left:"+ str(left))

                if (right > left ) and (right-left > 8):
                        potential_gain =  50 * getOdds(0, self.memory["current_bets"][list(self.memory["current_bets"].keys())[0]][i]["cotes"])
                        self.memory["confirmed_bets"][i]["potential_gain"] = potential_gain
                        self.memory["money"] -= 50
                        print(self.name + ' just made a bet with a potential gain of: '+ str(potential_gain))
                        pred = 0
                      
                elif (right > left) and (right-left > 5):
                        potential_gain =  10 * getOdds(0, self.memory["current_bets"][list(self.memory["current_bets"].keys())[0]][i]["cotes"])
                        self.memory["confirmed_bets"][i]["potential_gain"] = potential_gain
                        self.memory["money"] -= 10
                        print(self.name + ' just made a bet with a potential gain of: '+ str(potential_gain))
                        pred = 0
                        
                elif (left > right ) and (left-right > 8):
                        potential_gain =  50 * getOdds(3, self.memory["current_bets"][list(self.memory["current_bets"].keys())[0]][i]["cotes"])
                        self.memory["confirmed_bets"][i]["potential_gain"] = potential_gain
                        self.memory["money"] -= 50
                        print(self.name + ' just made a bet with a potential gain of: '+ str(potential_gain))
                        pred = 3
                        
                elif (left > right) and (left-right > 5):
                        potential_gain =  10 * getOdds(3, self.memory["current_bets"][list(self.memory["current_bets"].keys())[0]][i]["cotes"])
                        self.memory["confirmed_bets"][i]["potential_gain"] = potential_gain
                        self.memory["money"] -= 10
                        print(self.name + ' just made a bet with a potential gain of: '+ str(potential_gain))
                        pred = 3
                else:
                    del self.memory["confirmed_bets"][i]
                    i+=1
                    continue


                self.memory["confirmed_bets"][i]["potential_gain"] = float(potential_gain)
                self.memory['current_bets'][list(self.memory["current_bets"].keys())[0]][i]["prediction"] = int(pred)
                self.memory["total_bets_made"] +=1

                i+=1

        if self.id == '04':  # Risky Vent d'Ofsky

            final_cote = 1

            for rounds in self.memory["current_bets"]:
                i=0
                for candidat in self.memory["current_bets"][rounds]:
                    
                    #checking each cotes
                    cotes = candidat["cotes"]
                    j=0
                    for cote in cotes:
                        if float(cotes[cote]) < 1.65:
                            self.memory["confirmed_bets"][i] = {'bet_data' : self.memory['current_bets'][list(self.memory["current_bets"].keys())[0]][i]}
                            final_cote = final_cote * float(cotes[cote])
                            print(self.name + ' added a match to his cobmined bet with a betting odd at : '+ str(float(cotes[cote])))

                            if j == 0: pred = 3
                            if j == 1: pred = 1
                            if j == 2: pred = 0

                            self.memory['current_bets'][list(self.memory["current_bets"].keys())[0]][i]["prediction"] = str(cote)

                            break
                            j+=1
                    i+=1

         

            if len(self.memory["confirmed_bets"]) >= 1:
                self.memory["confirmed_bets"]["potential_gain"] = float(15 * final_cote)
                self.memory["money"] -= 15
                self.memory["total_bets_made"] +=1
            else:
                self.memory["confirmed_bets"]["potential_gain"] = 0


        if self.id == '05':  # Vent d'Ofsky

            final_cote = 1

            for rounds in self.memory["current_bets"]:
                i=0
                for candidat in self.memory["current_bets"][rounds]:
                    
                    #checking each cotes
                    cotes = candidat["cotes"]
                    j=0
                    for cote in cotes:
                        if float(cotes[cote]) < 1.5:
                            self.memory["confirmed_bets"][i] = {'bet_data' : self.memory['current_bets'][list(self.memory["current_bets"].keys())[0]][i]}
                            final_cote = final_cote * float(cotes[cote])
                            print(self.name + ' added a match to his cobmined bet with a betting odd at : '+ str(float(cotes[cote])))   

                            if j == 0:
                                pred = 3
                            if j == 1:
                                pred = 1
                            if j == 2:
                                pred = 0

                            self.memory['current_bets'][list(self.memory["current_bets"].keys())[0]][i]["prediction"] = pred

                            break
                            j+=1
                    i+=1

            if len(self.memory["confirmed_bets"]) >= 1:
                self.memory["confirmed_bets"]["potential_gain"] = 20 * final_cote
                self.memory["money"] -= 20
                self.memory["total_bets_made"] +=1
            else:
                self.memory["confirmed_bets"]["potential_gain"] = 0




    def setBetData(self,key,key2,data):
        self.memory["confirmed_bets"][key2] =  self.memory.pop(key2)
        self.save_bot_data()

    def makeModification(self):
        print("code here")



    def makeModification2(self):
        print("code here")

    

    def verifyBets(self,round1):   
        print("\n-Verifying bets for "+ self.name)

        if self.id in ["05","04"]: #for bots using combined bets
            allwon = True
            for bet in self.memory["confirmed_bets"]:
                currbet = self.memory["confirmed_bets"][bet]
                if not isinstance(bet,int): continue # hacky code solving problems for bad code management
                if not betSuccess(currbet,bet,round1):
                    allwon = False

            if allwon:
                self.memory["money"] += self.memory["confirmed_bets"]["potential_gain"]
                print(self.name + 'made a successful combined bet and won ' + str( self.memory["confirmed_bets"]["potential_gain"]))
                print("bet info: " + str(self.memory["confirmed_bets"]))
                self.memory["successful_bets"] +=1
            else:
                self.memory["unsuccessful_bets"] +=1

            return None


        for bet in self.memory["confirmed_bets"]:
            currbet = self.memory["confirmed_bets"][bet]
            if betSuccess(currbet,bet,round1):
                self.memory["money"] += currbet["potential_gain"]
                print(self.name + 'made a successful bet and won ' + str( currbet["potential_gain"]))
                print("bet info: " + str(currbet))
                self.memory["successful_bets"] +=1
            else:
                self.memory["unsuccessful_bets"] +=1

#free functions

def getOdds(val, odds):

    print(odds)
    print(val)

    if val == 3:
        return float(odds[str(3)])
    if val == 1:
        return float(odds[str(1)])
    return float(odds[str(0)])

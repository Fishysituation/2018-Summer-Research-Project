import random as r

# 0 represents cooperate
# 1 represents defect

# for payoff matrix
# y represents current perspective's move, x opponents move
#
# e.g. player cooperates, opponent defects - payoff[0][1] - 0 points
# opponent perspective - player defects, opp. co-ops  - payoff[1][0] - 5 points
payoffs = [
    [3, 0],
    [5, 1],
]


strategies = ["allC", "allD", "random", "TFT", "PAV", "grim"]
qStrategies = ["allD", "TFT", "DDC"]
netStrategies = ["allD", "TFT", "grim", "CCD", "DDC"]

# base player class - to train net
class player:

    strategy = ""
    #state variable availiable for strategies to use
    state = 0

    def __init__(self, strategy):
        self.strategy = strategy


    def move(self, history = [], custom = None):
        #simple strategies - training net
        if self.strategy == "allC":
            return 0
        elif self.strategy == "allD":
            return 1
        elif self.strategy == "random":
            return r.randint(0, 1)
        #short memory strategies - ecological
        elif self. strategy == "TFT":
            return self.TFT(history)
        elif self.strategy == "PAV":
            return self.PAV(history)

        #other strategies
        elif self.strategy == "grim":
            return self.grim(history)
        elif self.strategy == "CCD":
            return self.CCD()
        elif self.strategy == "DDC":
            return self.DDC()
        
        #for genetic/neural net player
        elif self.strategy == "other":
            return custom


    # for history in following strategies
    # 2D array, [[player], [opponent]]

    def TFT(self, history):
        #cooperate if first round
        if len(history[0]) < 1:
            return 0
        #else copy opponent's last move
        else:
            return history[1][-1]

    def PAV(self, history):
        #cooperate if first round
        if len(history[0]) < 1:
            return 0
        #check if last round WON i.e. player def. opp. coop.
        elif history[0][-1] == 1 and history[1][-1] == 0:
            #stick with same strategy
            return self.state
        #if lost or drew
        else:
            #swap strategy
            if self.state == 0:
                self.state = 1
                return 1
            else:
                self.state = 0
                return 0

    def grim(self, history):
        #cooperate first round
        if len(history[0]) < 1:
            return 0
        #yeet on them if they've yeeted on you
        else:
            if self.state == 1:
                return 1
            elif history[1][-1] == 1:
                self.state = 1
                return 1
            else:
                return 0

    def CCD(self):
        if self.state == 0:
            return 0
        elif self.state == 1:
            return 0
        elif self.state == 2:
            self.state = 0
            return 1


    def DDC(self):
        if self.state == 0:
            return 1
        elif self.state == 1:
            return 1
        elif self.state == 2:
            self.state = 0
            return 0
            

# special player - ecological, genetic, net
class adaptivePlayer(player):

    score = 0

    def __init__(self, strategy):
        super().__init__(strategy)


    def payoff(self, playerMove, opponentMove):
        self.score += payoffs[playerMove][opponentMove]
        return payoffs[playerMove][opponentMove]

    
import prisoner

strat = int(input())
opponent = prisoner.adaptivePlayer(prisoner.strategies[strat])
player = prisoner.adaptivePlayer("other")

print("Playing against " + opponent.strategy)

playerHistory = []
oppHistory = []

while True:
    
    oppMove = opponent.move([oppHistory, playerHistory])
    print(oppMove)

    print("Coop (0) or Defect (1): ", end = '')
    playerMove = player.move([playerHistory, oppHistory], int(input()))
    
    oppHistory.append(oppMove)
    playerHistory.append(playerMove)

    if oppMove == 0 and playerMove == 1:
        print("Player wins")
    
    elif oppMove == 1 and playerMove == 0:
        print("Opponent wins")

    else:
        print("Draw")

    player.payoff(playerMove, oppMove)
    opponent.payoff(oppMove, playerMove)

    print("Scores: player: " + str(player.score) + " opponent: " + str(opponent.score))

    print()
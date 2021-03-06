#multiStrategies4
STRATEGY_ONE = 'forecastMyMove' 
STRATEGY_TWO = 'forecastOponentMove'

def defeatMove(obj):
	if obj == 'R':
		return 'P'
	elif obj == 'P':
		return 'S'
	else:
		return 'R'

def lostLastMatche(myMove, oponentMove):
	if myMove == defeatMove(oponentMove) or myMove == oponentMove:
		return False
	else:
		return True	

def mostPlayed(dic):
	if dic['R'] > dic['P'] and dic['R'] > dic['S']:
		return 'R'
	elif dic['P'] > dic['S']:
		return 'P'
	else:
		return 'S'

if input == '':
	oponentMoves = {'R': 0, 'P': 0, 'S': 0}
	myMoves = {'R': 0, 'P': 0, 'S': 0}

	consecutiveLoses = 0

	oponentHistory = []
	myHistoriy = ['R']
	strategy = STRATEGY_ONE
	output = mylastMove = 'R'
else:
	oponentMoves[input] += 1
	oponentHistory.append(input)
	myHistoriy.append(input)
	
	if lostLastMatche(mylastMove, input):
		consecutiveLoses += 1

	if consecutiveLoses == 2: #swap stretegies
		strategy = STRATEGY_TWO if strategy == STRATEGY_ONE else STRATEGY_ONE

	# 1 calculate my most frequent move
	# 2 assume that the oponent would try to defeat this move
	# 3 defeat this move
	if STRATEGY_ONE: 
		myMostPlayed = mostPlayed(myMoves)
		move = defeatMove(defeatMove(myMostPlayed))
	
	# 1 calculate my oponent's most frequent move
	# 2 defeat this move
	else:
		oponentMostPlayed = mostPlayed(oponentMoves)
		move = defeatMove(oponentMostPlayed)

	myMoves[move] += 1
	output = mylastMove = move
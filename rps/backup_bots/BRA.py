# BRA

import random

beat = {'R':'P', 'P':'S', 'S':'R'}
moves = ['R', 'P', 'S']
pattern = []
patterns = {}

def keyBuilder(array):
	string = ""
	for i in array:
		string += i
	return string

if input == "":
	output = random.choice(moves)
	matches = []
else:
	matches.append(input)
	if(len(matches) > 3):
		pattern.append(matches[len(matches):-3])
		for i in range(0, len(matches)-4):
			if(pattern == matches[i:i+3]):
				key = keyBuilder(pattern + list(matches[i:i+4]))
				if key in patterns:
					patterns[key] += 1
				else:
					patterns[key] = 1
		if len(patterns) > 0:
			best = max(patterns, key=patterns.get)
			last = best[-1]
			output = beat[last]
		else:
			output = random.choice(moves)
	else:
		output = random.choice(moves)
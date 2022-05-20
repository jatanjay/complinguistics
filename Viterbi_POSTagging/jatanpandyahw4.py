"""
Jatan pandya
hw4
"""

"""
hidden states (s)
observed (o)
pi =
a = transition
b = emission


forward : P(O|HMM)
I.E. P(TIME FLIES QUICKLY (or whatver) | hmm )
observed

"""

"""
Ideas

Forward : p of seeing
viterbi : what's the most probable sequence?
"""

pi = {
	'N': 0.63,
	'V': 0.27,
	'R': 0.10
	}

## DISREGARD
pi2 = {
	's': 0.6,
	'r': 0.4
	}
## DISREGARD
b = {
	('s', 'paint'): 0.4,
	('s', 'clean'): 0.1,
	('s', 'shop'): 0.2,
	('s', 'bike'): 0.3,
	('r', 'paint'): 0.3,
	('r', 'clean'): 0.45,
	('r', 'shop'): 0.2,
	('r', 'bike'): 0.05,
	}

# i.e n given r is 0.19
A = {
	('N', 'N'): 0.64,
	('N', 'V'): 0.28,
	('N', 'R'): 0.08,
	('V', 'N'): 0.67,
	('V', 'V'): 0.20,
	('V', 'R'): 0.13,
	('R', 'N'): 0.19,
	('R', 'V'): 0.70,
	('R', 'R'): 0.11
	}
## DISREGARD
a = {
	('s', 's'): 0.8,
	('s', 'r'): 0.2,
	('r', 's'): 0.4,
	('r', 'r'): 0.6,
	}

B = {
	('N', 'time'): 0.98,
	('N', 'flies'): 0.015,
	('N', 'quickly'): 0.005,
	('V', 'time'): 0.33,
	('V', 'flies'): 0.64,
	('V', 'quickly'): 0.03,
	('R', 'time'): 0.01,
	('R', 'flies'): 0.01,
	('R', 'quickly'): 0.98,
	}

b_swat = {
	('N', 'time'): 0.98,
	('N', 'flies'): 1.00,
	('N', 'quickly'): 0.005,
	('V', 'time'): 0.33,
	('V', 'flies'): 0.64,
	('V', 'quickly'): 0.03,
	('R', 'time'): 0.01,
	('R', 'flies'): 0.01,
	('R', 'quickly'): 0.98,
	('N', 'swat'): 0,
	('V', 'swat'): 1.00,
	('R', 'swat'): 0
	}


def forwardProcedure(test_seq, A, B, pi, see_matrix=False):
	table = {0: pi}
	seq = test_seq.split()
	time = 1
	
	for word in seq:
		table[time] = {}
		for tag in pi:
			table[time][tag] = 0
			for tag2 in pi:
				fp = table[time - 1][tag2] * A[(tag2, tag)] * B[(tag2, word)]
				table[time][tag] += fp
		time += 1
	
	f = sum(table[time - 1].values())
	return f


def viterbiAlgorithm(test_seq, A, B, pi, see_matrix=False):
	table = {0: pi}
	seq = test_seq.split()
	psi = {0: {n: '_' for n in pi}}
	time = 1
	
	for word in seq:
		table[time] = {}
		psi[time] = {}
		for tag in pi:
			table[time][tag] = -1
			psi[time][tag] = "_"
			for tag2 in pi:
				fp = table[time - 1][tag2] * A[(tag2, tag)] * B[(tag2, word)]
				if fp > table[time][tag]:
					table[time][tag] = fp
					psi[time][tag] = tag2
		time += 1
	
	f = max(table[time - 1].values())
	time -= 1
	res = ''
	while time > 0:
		state = max(table[time])  # v
		new_state = psi[time][state]
		state = new_state
		res = state + res
		time -= 1
	return res


if __name__ == '__main__':
	# fp = forwardProcedure('paint clean shop bike', a, b, pi2, True)
	# print(fp)
	# va = viterbiAlgorithm('shop clean bike paint', a, b, pi2, False)
	# print(va)
	fp = forwardProcedure('time flies quickly', A, B, pi)
	print(fp)
	va = viterbiAlgorithm('time flies quickly', A, B, pi)
	print(va)
	va2 = viterbiAlgorithm('swat flies quickly', A, b_swat, pi)
	print(va2)

"""
What is the probability of the sequence 'time flies quickly'
--> 0.0174441666775
--> 3*3*3 (N/V/R) for each word. i.e. 3^3 = 29 ways.

Q2: What is the best tag sequence for 'time flies quickly'?
--> NVR

Q3: What's the probability of 'quickly time flies'? What parameters could you change to make 'quickly time flies'
more likely than 'time flies quickly'? Be specific!
--> p(forward_procedure) : 0.008166993082499999
In order to make quickly time flies > time flies quickly I would tweak the Adverb to Noun i.e. (N|R) probabilities.
Further I can also reduce the (R|V) prob to further increase.

Q4: Modify matrix B to add a new word 'swat' to the lexicon. Assume that 'swat' can *only* be a verb, and make sure
your matrix defines proper probability distributions. Set the probabilities so that the most likely sequence for
'swat flies quickly' is 'V N R'.
--> I made ('N', flies) as 1.00.
	Further, Since it can only be a verb,
	('N', 'swat'): 0,
	('V', 'swat'): 1.00,
	('R', 'swat'): 0
"""

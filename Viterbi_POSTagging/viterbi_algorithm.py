# """
# jatan
# viterbi
# """
#
from collections import defaultdict

B = {
	('N', 'time'): 0.98,
	('N', 'flies'): 0.015,
	('N', 'quickly'): 0.005,
	('V', 'time'): 0.33,
	('V', 'flies'): 0.64,
	('V', 'quickly'): 0.03,
	('R', 'time'): 0.01,
	('R', 'flies'): 0.01,
	('R', 'quickly'): 0.98
	}

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

pi = {
	'N': 0.63,
	'V': 0.27,
	'R': 0.10
	}


def trellis_builder(pi, test_sequence):
	sequence = test_sequence.split()
	total_number_of_states = len(sequence) + 1
	curr_state = 0
	trellis = defaultdict(dict)  # init, this will change every state
	while curr_state < total_number_of_states:
		for tag in pi.keys():
			trellis[curr_state][tag] = 0
		curr_state += 1
	return trellis


def viterbiAlgorithm(test_sequence, A, B, pi):
	trellis = trellis_builder(pi, test_sequence)
	psi = defaultdict(list)
	state = 0
	for tag in pi.keys():
		trellis[state][tag] = pi[tag]
		psi[tag].append("_")

	print(trellis)
	print(psi)

	curr_state = 0
	sequence = test_sequence.split()
	psi = defaultdict(list)
	total_number_of_states = len(sequence) + 1

	# init
	for tag, start_prob in pi.items():
		trellis[curr_state][tag] = start_prob
		psi[tag].append('_')

	for word in sequence[:1]:
		for i in pi.keys():
			alpha = trellis[curr_state][i] * B[(i, word)]
			trellis[curr_state + 1][i] = alpha
	curr_state += 2

	while curr_state < len(sequence):
		for word in sequence[1:]:
			for j in pi.keys():
				res = []
				psi_res = []
				for i in pi.keys():
					prev_delta_for_tag_i = trellis[curr_state - 1][i]
					transition_prob = A[(i, j)]
					emission_prob = B[(j, word)]
					alpha = prev_delta_for_tag_i * transition_prob * emission_prob
					print(prev_delta_for_tag_i, transition_prob, emission_prob, alpha)
					res.append(alpha)
				trellis[curr_state][j] = max(res)
			curr_state += 1

	print(trellis)


if __name__ == '__main__':
	f = viterbiAlgorithm('time flies quickly', A, B, pi)


states = ('N', 'V', 'R')

observations = ('time', 'flies', 'quickly')

start_probability = {'N': 0.63, 'V': 0.27, 'R': 0.10}

transition_probability = {
	'N': {'N': 0.64, 'V': 0.28, 'R': 0.08},
	'V': {'N': 0.67, 'V': 0.20, 'R': 0.13},
	'R': {'N': 0.19, 'V': 0.70, 'R': 0.11}
	}

emission_probability = {
	'N': {'time': 0.98, 'flies': 0.015, 'quickly': 0.005},
	'V': {'time': 0.33, 'flies': 0.64, 'quickly': 0.03},
	'R': {'time': 0.01, 'flies': 0.01, 'quickly': 0.98}
	
	}


# Helps visualize the steps of Viterbi.
def print_dptable(V):
	s = "    " + " ".join(("%7d" % i) for i in range(len(V))) + "\n"
	for y in V[0]:
		s += "%.5s: " % y
		s += " ".join("%.7s" % ("%f" % v[y]) for v in V)
		s += "\n"
	print(s)


def viterbi(obs, states, start_p, trans_p, emit_p):
	V = [{}]
	path = {}
	
	# Initialize base cases (t == 0)
	for y in states:
		V[0][y] = start_p[y] * emit_p[y][obs[0]]
		path[y] = [y]
	
	# alternative Python 2.7+ initialization syntax
	# V = [{y:(start_p[y] * emit_p[y][obs[0]]) for y in states}]
	# path = {y:[y] for y in states}
	
	# Run Viterbi for t > 0
	for t in range(1, len(obs)):
		V.append({})
		newpath = {}
		
		for y in states:
			(prob, state) = max((V[t - 1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
			V[t][y] = prob
			newpath[y] = path[state] + [y]
		
		# Don't need to remember the old paths
		path = newpath
	
	print_dptable(V)
	(prob, state) = max((V[t][y], y) for y in states)
	return (prob, path[state])


def example():
	return viterbi(observations,
	               states,
	               start_probability,
	               transition_probability,
	               emission_probability)


print(example())

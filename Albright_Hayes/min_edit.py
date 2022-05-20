"""
author : jatan pandya
file : min_edit.py
prof. b. dillon, a. lamont
2/14
"""

# this regexp will match any vowel symbol
import sys

V = r"[0123456789$@EI{VQUiu#cq]"

# Specifically, this model works almost exactly like the
# basic Levenshtein−with a penalty of 1 for an insertion or a deletion or for a substitution
# that does not change a vowel to a consonant or vice
# versa−but the penalty for substituting a vowel for a
# consonant (or vice versa) is 2.
#
# - McCoy Phonologically Informed Edit Distance Algorithms for Word Alignment with Low-Resource Languages (2018)


"""
I haven't made any improvements in this script. everything was done in analogy.py
I tried implementing a model described in a paper (above) where the penalty for substituting a vowel
for a consonant, or for substituting a consonant for
a vowel, is greater than that for substituting a vowel
for a vowel or for substituting a consonant for a consonant.

... but that didn't give any improved results.

below is the function that checked if the c,d are vowels or not
"""


# not working out // skip

# def vow_conso_helper(s1, s2):
# 	if re.search(V, s1):
# 		# S1 is vowel
# 		s1_flag = True
#
# 	else:
# 		# s1 is a consonant
# 		s1_flag = False
#
# 	if re.search(V, s2):
# 		# S2 is vowel
# 		s2_flag = True
#
# 	else:
# 		# S2 is conso
# 		s2_flag = False
#
# 	if s1_flag == s2_flag:
# 		# i.e. if s1 and s2 are both vowels or both are consonants
# 		return True
# 	else:
# 		return False


def ins_cost(c, source):
	return 1


def del_cost(c, source):
	return 1


def sub_cost(c, d, source):
	if c == d:
		return 0
	# if vow_conso_helper(c, d):
	# return 2
	else:
		return 2


def min_edit(source='', target='', verbose=False):
	"""
	:param source: source string
	:type source: str
	:param target: target string
	:type target: str
	:param verbose: if the user wants to see the table
	:type verbose: bool
	:return: cost / distance of transformation
	:rtype: int
	"""
	m = len(source)
	n = len(target)
	
	# create a
	dist = [
		[0] * (n + 1) for i in range(m + 1)
		]
	
	"""
	if source = 'carry' and target = 'car'
	dist = [
		 [0, x, x, x],
		 [x, x, x, x],
		 [x, x, x, x],
		 [x, x, x, x],
		 [x, x, x, x],
		 [x, x, x, xx],
		 ]
	   min edit distance will be xx or dist[m][n]

	"""
	
	# initialization
	dist[0][0] = 0
	
	"""
	Fill the upside down 'L'


			C   A   R
		0   1   2   3
	C   1   .   .   .
	A   2   .   .   .
	R   3   .   .   .
	R   4   .   .   .
	Y	5   .   .   d
	"""
	
	for col in range(1, n + 1):
		dist[0][col] = dist[0][col - 1] + ins_cost(target[col - 1], source)
	
	for row in range(1, m + 1):
		dist[row][0] = dist[row - 1][0] + del_cost(source[row - 1], source)
	
	# Recurrence relation
	
	for row in range(1, m + 1):
		for col in range(1, n + 1):
			dist[row][col] = min(
				dist[row - 1][col] + del_cost(source[row - 1], source),
				dist[row - 1][col - 1] + sub_cost(source[row - 1], target[col - 1], source),
				dist[row][col - 1] + ins_cost(target[col - 1], source)
				)
	
	return dist[m][n]


def main():
	s = sys.argv[1]
	t = sys.argv[2]
	print(min_edit(source=s, target=t, verbose=True))


if __name__ == "__main__":
	main()

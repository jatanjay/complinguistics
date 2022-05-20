"""
jpandya
b. dillon , a. lamont
3/15
"""
import math
import sys
from collections import defaultdict

base = 2
start_char = "<"
end_char = ">"


def txt_to_list(file_name):
	"""
	opens file name, outputs a list of words with the first word having "<" start char and last having ">"
	further, white space is added between each word since white space is crucial when creating a bigram
	:param file_name:
	:type file_name: str
	:return: list
	:rtype:
	"""
	res = ''
	with open(file=file_name, mode='r') as f:
		res += f.readline()
	split = res.split()
	return padder(split)


def padder(list_words):
	"""
	takes a list of words, adds '<' and '>' plus white space
	:param list_words:
	:type list_words: list
	:return:
	:rtype: list
	"""
	# adding ' ' at both start and end since whitespace char is crucial (except first and last word)
	# Further, adding a <start> <end> char (and some text cleaning)
	
	return [start_char + list_words[0].replace('"', '') + ' '] + [' ' + word + ' ' for word in list_words[1:-1]] + [
		' ' + list_words[-1].replace('"', '') + end_char]


def bigram_builder(char_list):
	"""
	takes list of words, and makes bigrams by words i.e. '<c ar>' becomes [(<,c),(c,' '),(' ',a) ...]'
	:param char_list:
	:type char_list: list
	:return:
	:rtype: list
	"""
	t_bigrams = []
	for char in char_list:
		bigram_by_char = [(char[i], char[i + 1]) for i in range(len(char) - 1)]
		t_bigrams += bigram_by_char
	# t_bigrams has bigrams by chars i.e. [('<', 'i'), ('i', 'n'), ('n', 'u'),
	# ('u', 't'), ('t', 't'), ...]
	
	return t_bigrams


def bigramModel(bigrams, k, vocab, default_vocab='abcdefghijklmnopqrstuvwxyz'):
	"""
	to compute a particular bigram probability of a word y given a previous word x, we’ll compute the
	count of the bigram C(xy) and normalize by the sum of
	all the bigrams that share the same first word x:

	input : bigrams i.e. a list of observed bigrams in the text. [(),()] list of tuples
	"""
	k = float(k)
	all_possible_bigrams = set()
	char_freq = defaultdict(int)
	bigram_freqDict = defaultdict(float)
	bigram_prob = defaultdict(float)
	
	def_set = set(list(default_vocab))  # latin letters
	
	vocab_set = set(list(vocab))  # what the user will pass in
	
	# unique chars in the specified
	u_chars = {char for bigram_tuple in bigrams for char in bigram_tuple}
	# langauge maybe can be something like ?, white space etc.
	
	unique_chars = set()
	
	# all the characters that are needed to create bigrams for
	unique_chars = unique_chars.union(def_set, vocab_set, u_chars)
	
	for chy in unique_chars:
		for chx in unique_chars:
			all_possible_bigrams.add((chy, chx))
	"""
	step 1 : create a frequency dict of all possible bigrams (22^2) (greenlandic) (23^2 ilocano)
	in which bigrams that are not possible in given input will be zero
	bigrams that are seen will have their frequency.

	# plus add the vocab too (by default latin std)

	create a freqdict of all observed bigrams like you would
	then for each all possible bigram in the set:
		if bigram is in freqdict:
			skip
		else:
			freqdict[bigram] = 0
	"""
	
	# bigrams seen for the given language
	
	for bigram in bigrams:
		bigram_freqDict[bigram] += 1 + k  # smoothing param
	for a_bigram_candidate in all_possible_bigrams:
		if a_bigram_candidate not in bigram_freqDict:
			bigram_freqDict[a_bigram_candidate] = 0 + k
	
	# necessary when dividing it (from the formula)
	# how many times each character is seen
	
	for bg, freq in bigram_freqDict.items():
		for u_q in unique_chars:
			if u_q == bg[0]:
				char_freq[u_q] += freq
	
	"""
	step 2:

	Build bigram_prob dict

	{'for a bigram (i,x)' : freq of that bigram (i,x) / freq of i occurring in position 0

	curr we have:
	freq of that bigram --> check
	freq of char --> char_freq['that_char'] --> check
	"""
	
	for bigram, its_freq in bigram_freqDict.items():
		its_first_char = bigram[0]
		bigram_prob[bigram] = its_freq / char_freq[its_first_char]
	
	# print(bigram_prob[('<', 'z')])
	# f = sorted(((v, k) for k, v in bigram_prob.items()), reverse=True)
	# pprint.pprint(f)
	
	return bigram_prob, unique_chars


def perplexity(bigram_model, test_set):
	"""
	Between two models m1 and m2, the more accurate model will be the one with the
	lower cross-entropy

	perplexity = 2^cross_entropy

	branching factor : vocab size (number of chars)

	PP = 2 ^ (-1/n * summation of log ( p of char i | bigram model))

	"""
	bModel = bigram_model[0]
	log_sum = 0
	
	# create  a list of bigrams for given text sentence, also add the start
	# and end chars plus
	bigrammed = bigram_builder(padder(test_set.split()))
	# white spaces
	n = len(bigrammed) - 1
	
	for b_tuple in bigrammed:
		# for a bigram seen in test sentence, find it's prob according to the langauge model and a calc it's log val
		# base 2
		log_sum += math.log(bModel[b_tuple], base)
	
	exp = 1 / n * log_sum
	perplexing = math.pow(2, -exp)
	print(
		f"Test sentence {start_char + test_set + end_char}'s perplexity is :: {perplexing}\n")
	return perplexing


def main():
	by_text_perplex = {}
	test_sentence = sys.argv[1]
	k = sys.argv[2]
	
	texts = ['greenlandic.txt', 'ilocano.txt']
	
	for text in texts:
		print(f'\nModel built on Language: {text[:-4]}')
		bigram_Builder = bigram_builder(
			txt_to_list(text))  # make bigrams of the given text
		# takes test sentence, k=param, lang bigram
		bigram_Model = bigramModel(bigram_Builder, vocab=test_sentence, k=k)
		perPlex = perplexity(bigram_Model, test_set=test_sentence)
		by_text_perplex[text] = perPlex
	
	print(
		f"Predicted language (i.e. language with lowest perplexity) : \n"
		f"{min(by_text_perplex, key=by_text_perplex.get)[:-4]}\n")


if __name__ == "__main__":
	main()

"""
Part 4 : Responses

1.
The model works perfectly. I tested the script on some randomly stitched sentences from wiki. It correctly predicted
the langauge.

Results ::

Actual Language: Kalaalit
Model built on Language: greenlandic
Test sentence <Namminersornerulernermut allaffik Nuummiippoq>'s perplexity is :: 10.551540410350102
Model built on Language: ilocano
Test sentence <Namminersornerulernermut allaffik Nuummiippoq>'s perplexity is :: 76.39636097638298
Predicted language (i.e. language with lowest perplexity) : greenlandic


Actual Language: ilocano
Model built on Language: greenlandic
Test sentence <Ti laeng pagdumaanna ket no dakamaten ti sao wenno pagsasao ken ti tao nga agsasao wenno agus-usar iti
pagsasao>'s perplexity is :: 75.84737032694233
Model built on Language: ilocano
Test sentence <Ti laeng pagdumaanna ket no dakamaten ti sao wenno pagsasao ken ti tao nga agsasao wenno agus-usar iti
pagsasao>'s perplexity is :: 9.272812698322438
Predicted language (i.e. language with lowest perplexity) : ilocano


/
Factors that influenced the prediction:
Well exactly what we modelled, that is most frequent patterns observed in a language. what letter follows what letter,
and how frequently. Also are there any common patterns, or patterns that are specific to only one language. For example,
can same letter occur twice in consequently? Further, white spaces between words also a characteristic of a language
which influenced the prediction.

2.
I choose following words :
Paamiut, Maniitsoq (in order to trick ilocano)
Kordiliera, bersion, aginggana, porsiento (in order to trick greenlandic)

approach : I sorted the prob dict in descending order. Picked the top 5 frequent character bigrams. I search for
words containing these bigrams preferably in the same starting position. This was extremely difficult as these bigrams
are the characteristic of respective languages. In a way this was the original idea. If a bigram appears more
frequent then that should be reflected in it's prob, which maybe correlates to the idea that these bigrams are
important candidates in distinguishing that language from another. (I.e. how some morphemes can't occur at the end of
an english word while some can)

I fooled my model with word "bersion" but by a very small margin. Perplexity for Ilocano was 95.06744164154486 while
Greenlandic's 95.95063261559157. The word means 'version' in Ilocano!

3.
If we don't do any smoothing we run into errors. This is because if no smoothing is done, the frequency of the char
not seen will be zero. and hence the perplexity will be ∞. This is exactly the reason we do smoothing in first place.

The ability changes over various values of k parameter. Since it changes the frequency, which in turn changes the cross
entropy when we calculate. Greater value of smoothing parameter will reduce the accuracy of the model for the same
reason.

4.
Adding the k parameter for the bigrams we don't see has an effect on our further calculations specifically when we calc
the probabilities.
For example when we add a high k, we get a higher value when we divide it by the char freq when calculating
the prob of the sequence. Hence greater the 'k' greater the prob of the sequence

5.
Thinking of perplexity in terms of entropy we see can see the Lower perplexity scores indicate a better model fit to a
set of test data. Firstly, entropy is a parameter that indicates is the average number of bits to encode the
information contained in a random variable.Then, perplexity is just the exponentiation of this entropy. That is
perplexity tells us total amt of
all possible information that can be contained. For a model, less entropy is more favourable as this tell us that
prediction is more accurate. Perplexity tells us how "perplexed" the model gets when given a text.

"""

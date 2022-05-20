"""
Jatan Pandya / 492B Homework 6
file : hw6.py
"""
import re
import os
from collections import defaultdict
import math
import sys

from nltk.corpus import stopwords

"""
for a give word,
go to it's dict file, create a tag uid dict, add def and example too!

whole line is crucial


do pred,
go to gold, search that tag, real_val
if pred != real_val , accuracy


algo

In other words, the Bayesian decision rule says label an observation with the class that has the highest conditional
probability, given its features.x


What are the features we are going to use to classify senses? For this task we are going to use the bag of words
approach. On the bag of words approach, we are going to take an item's context, remove all stopwords, tokenize on
white-space, and optionally lemmatize/stem the contents to create an unstructured bag of words.


class is the sense

open train, for the word.cov
take the context, tokenize the word,
"""

stop_words = set(stopwords.words('english'))


def data_files(word):
	"""
	:param word: interested word
	:type word: string
	:return: data files for that word
	:rtype: object
	"""
	
	"""
	train : .cor
	test = .eval
	gold = -n/a/v
	dict = .dic

	"""
	
	dict_file = {}
	train_file_raw = defaultdict(list)
	eval_file_raw = defaultdict(list)
	gold_file = {}
	
	for dir in os.listdir():
		if '.py' not in dir:  # get rid of the hw6.py file cz in same dir
			for file in os.listdir(dir):
				if word in file:
					os.chdir(dir)
					with open(file, 'r') as fout:
						if file[-4:] == '.dic':  # dic file
							for line in fout.readlines():
								uid = re.search('(\\d+\\s{2})', line)
								tag = re.search('(tag=\\w*)', line)
								if uid and tag:
									dict_file[uid.group(0).strip()] = tag.group()[
									                                  4:]
						
						if file[-4:] == '.cor':  # train
							i = 0
							for line in fout.readlines():
								if line.strip() != "\n":
									train_file_raw[i].append(line)
									o = ''
									for w in train_file_raw[i]:
										o += w
									train_file_raw[i] = [o]
								if line.strip() == "":
									i += 1
						
						if file[-5:] == '.eval':
							i = 0
							for line in fout.readlines():
								if line.strip() != "\n":
									eval_file_raw[i].append(line)
									o = ''
									for w in eval_file_raw[i]:
										o += w
									eval_file_raw[i] = [o]
								if line.strip() == "":
									i += 1
						
						else:  # gold
							for line in fout.readlines():
								s = line.split(":")
								gold_file[s[0]] = s[1].strip()
					
					os.chdir("..")
	
	return dict_file, train_file_raw, eval_file_raw, gold_file


def files_helper(raw_train_dict, raw_eval_dict):
	train_dict = defaultdict(list)
	
	eval_dict = defaultdict(list)
	class_freq = {}
	
	for k, v in raw_train_dict.items():
		# v is a list
		for _ in v:
			# _ is a string
			tag = re.search('("\\d+")', _)
			
			if tag:
				tg = tag.group(0).replace('"', '')
				if tg not in class_freq:
					class_freq[tg] = 0
				else:
					class_freq[tg] += 1
			
			for single_word in _.split():
				# fine tune words
				if single_word not in stop_words:
					single_word = re.sub('[\\d\\s\\W]', '', single_word)
					single_word = single_word.replace('tag', '')
				if tag and single_word:
					train_dict[tag.group(0).replace('"', '')].append(
						single_word.strip().lower())
	
	for k, v in raw_eval_dict.items():
		# v is a list
		for _ in v:
			# _ is a string
			tag = re.search('(\\d+)', _)
			for single_word in _.split():
				# fine tune words
				if single_word not in stop_words:  # stop word removal
					single_word = re.sub(
						'[\\d\\s\\W]', '', single_word)  # char removal
					single_word = single_word.replace('tag', '')
				if tag and single_word:
					tg = tag.group(0).replace('"', '')
					eval_dict[tg].append(single_word.strip().lower())
	
	# print('Classes in training file, by freq')
	# pprint.pprint(class_freq)
	
	# pprint.pprint(eval_dict)
	# pprint.pprint(train_dict)
	
	return train_dict, eval_dict, class_freq


def marginal_class(freq_dict, dic_file, k=0.100):
	# print('\nClasses in dic file')
	# pprint.pprint(dic_file)
	
	# pprint.pprint(dic_file)
	
	mp_by_class = {}
	
	total_occurrences = sum(freq_dict.values())
	
	# for c in dic_file:
	# 	if c not in freq_dict:
	# 		freq_dict[c] = k
	
	for cl in freq_dict:  # smoothing param (add one k)
		mp_by_class[cl] = freq_dict[cl] / total_occurrences
	
	return mp_by_class


def word_prob(train_file, eval_dic, k):
	vocab_freq = {}  # all words in training data with their freq
	freq_by_classes = {}  # for a given class, freq of words
	p_w_class = {}
	
	for cl, word_list in train_file.items():
		freq = {}
		for wrd in word_list:
			if wrd != '':
				if wrd not in vocab_freq:
					vocab_freq[wrd] = 1
				else:
					vocab_freq[wrd] += 1
				if wrd not in freq:
					freq[wrd] = 1
				else:
					freq[wrd] += 1
		freq_by_classes[cl] = freq
	
	"""
	freq_by_classes
	'423123' : {'car':2,'bar':3}
	"""
	
	for clss, freq_dict in freq_by_classes.items():
		for wrd in vocab_freq:
			if wrd not in freq_dict:
				freq_dict.update({wrd: k})
	
	# n = number of words in our class training data
	
	"""
	so now I have
	all the words in our training corpus and it's freq

	all words for a given class given it's freq

	so now I have calc prob for each word given it's class

	for example
	so p('506385'|'against') will be


	freq('506385'|'against') / freq('against') in corpus

	also take care of smoothing. so for that for that

	{
	p_w_class = {'class' : {'p of word in class': xxx , 'p of word that doesn't exist in class but in corpus' : xxx
	}
	"""
	
	# this code adds all unseen words in each class and puts their freq to
	# zero, will help us when smoothing
	
	# so now my freq dict is 'class' : {'word':freq, 'unseen word' : 0}
	
	for klass, frequency_dict_words in freq_by_classes.items():
		p = {}
		n = sum(frequency_dict_words.values())
		for w in frequency_dict_words:
			w_freq = frequency_dict_words[w]
			words_prob = w_freq / n
			p[w] = words_prob
		p_w_class[klass] = p
	
	"""
	vocab = [] that contains all words from all classes and it's frequency
	by_classes = {} it's words plus words in vocab -- smoothed
	"""
	
	return p_w_class, vocab_freq


def model(p_w_class, m_prob, test_file, dic_file, gold_file, train_vo):
	correct = 0
	false = 0
	
	for gold_val, test_words in test_file.items():
		# print(f'curr gold val, test_word_list {gold_val}, {test_words}')
		cx = {}
		for cl, word_p_dict in p_w_class.items():
			p = 0
			for wd in test_words:
				if wd in train_vo:
					x = math.log(word_p_dict[wd])
					p += x
			
			if m_prob[cl] == 0.0:
				m_prob[cl] += 0.01
			p += math.log(m_prob[cl])
			cx[cl] = p
		
		prediction_key = max(cx, key=cx.get)
		prediction = dic_file[prediction_key]
		gold_tag = gold_file[gold_val]
		
		# print(f"prediction : {prediction}, gold tag : {gold_tag}")
		
		if prediction in gold_tag:
			correct += 1
		else:
			false += 1
	
	accuracy = (correct / (correct + false)) * 100
	return accuracy


if __name__ == '__main__':
	
	word = sys.argv[1]
	
	dict_file, train_file_raw, eval_file_raw, gold_file = data_files(word)
	train_file, eval_file, class_freq = files_helper(
		train_file_raw, eval_file_raw)
	marginal_pc = marginal_class(class_freq, dict_file)
	
	p_by_class, train_vocab = word_prob(train_file, eval_file, k=0.100)
	nbc = model(
		p_by_class,
		marginal_pc,
		eval_file,
		dict_file,
		gold_file,
		train_vocab)
	print(f"Accuracy for the word '{word}' is {nbc}%\n")

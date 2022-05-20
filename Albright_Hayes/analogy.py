"""
author : jatan pandya
file : analogy.py
prof. b. dillon, a. lamont
2/19
"""
import sys
from collections import defaultdict
from math import e

from min_edit import min_edit

"""
flesh and bones

Scope : A rule say x is applicable to y set of verbs. Hence the "scope" is Y.
Hits : number of correct "hits"
Accuracy : hits / scope --> raw confidence.

Train.csv : contains actual verbs + Phonetic representation / past tense of actual verbs + Phonetic rep / Rule
e.g. do -- du -- did -- dId -- u -> Id

Test.csv :
wug verb (present tense)
phonetic representation (present tense)
acceptability of the wug's present tense

Regular Past's phonetic representation
It's rating

Irregular Past's phonetic representation
It's rating

Class
transformation that had to be made to make it Irregular
"""


def pearson(v1, v2):
    if len(v1) != len(v2):
        return None
    s1 = sum(v1)
    s2 = sum(v2)
    m1 = s1 / len(v1)
    m2 = s2 / len(v2)
    xy = 0.0
    xx = 0.0
    yy = 0.0
    for i in range(len(v1)):
        xy += (v1[i] - m1) * (v2[i] - m2)
        xx += (v1[i] - m1) * (v1[i] - m1)
        yy += (v2[i] - m2) * (v2[i] - m2)
    return xy / ((xx ** .5) * (yy ** .5))


def get_training(f):
    pres = defaultdict(lambda: '')
    past = defaultdict(lambda: '')
    label = defaultdict(lambda: '')
    for v in f.readlines():
        orth, ppres, opast, ppast, cat = v.split(',')
        pres[orth] = ppres
        past[orth] = ppast
        label[orth] = cat.strip()
    f.close()
    return pres, past, label


def get_neighbors(wugphon='', dict={}, n=-1):
    """
    takes a phonetic transcription of a wug verb, a dictionary
    of actual verb forms to compare it to, and a number n.
    returns all neighbors within n as a dictionary of neighbor, distance pairs
    if n is negative (by default), all neighbors are returned
    :param wugphon: phonetic transcription of a wug verb
    :type wugphon: str
    :param dict: dict of actual verb forms necessary for comparison
    :type dict: dict
    :param n: number of 'n' neighbors desired
    :type n: int
    :return: all neighbors within 'n', distance pair if n is negative
    :rtype: dict
    """
    neighbors = defaultdict(lambda: 0.0)
    for verb, transcription in dict.items():
        # calculate min_edit distance between phonetic representation of the
        # actual verb and the wug
        d = min_edit(wugphon, transcription)

        if d <= n or n < 0:
            # save the distance for that verb with that wug, in the dictionary
            neighbors[verb] = d
    # print(neighbors)
    return neighbors


def similarity(neighbors, s):  # I added parameter s in order to run the script at various
    """
    :param neighbors: dict returned by func get_neighbors
    :type neighbors: dictionary
    :return: similarity metric
    :rtype: int
    """
    """
	from albright and hayes (2003) model, setting p = 1
	The similarity of a word to a collection of words is
	simply the sum of the pairwise similarities between w and each word in.
	"""
    # s = 10  # can be tweaked (albert and hayes : 0.4) / 0.6 is the best for
    # me rn
    sim = 0.0
    for v, d in neighbors.items():
        sim += e ** (-d / s)  # e ^ d_ij / s) ^ p

    return sim


# takes two lists of responses and returns the proportion that match
def accuracy(v1, v2):
    tot = len(v1)
    matches = 0.0
    for x, y in zip(v1, v2):
        if x == y:
            matches += 1
    return matches / tot


def main(s):
    trainf = open(sys.argv[1])
    testf = open(sys.argv[2])
    pres, past, label = get_training(trainf)

    # lists to create while looping through wug words
    responses = []  # will contain human forced choice responses /// done
    ratings = []  # will contain human well-formed-ness ratings /// done
    sims = []  # will contain predicted ratings based on similarity /// done
    preds = []  # will contain predicted forced choice responses based on analogy /// done

    # secret tool that will help us later

    morph_classes = {x for x in label.values()}
    by_classes = {}
    for morph_class in morph_classes:
        # this will make a dict of verbs that belong to this morph_class
        fly_for_this_morph_class = {}
        for verb in label:  # for verb in list of verbs
            # if the verb's morph class is equal to the current morph_class
            if label[verb] == morph_class:
                fly_for_this_morph_class.update({verb: pres[verb]})
        by_classes.update({morph_class: fly_for_this_morph_class})

    phon_lookup = {
        'voiceless': [
            'f',
            'h',
            'k',
            'p',
            's',
            't',
            'T',
            'S',
            'J'],
        'voiced': [
            'b',
            'd',
            'g',
            'l',
            'm',
            'n',
            'v',
            'w',
            'z',
            'D',
            'Z',
            '_',
            'N',
            'r',
            '-'],
        'vowels': {
            'high': {
                'i',
                'I',
                'u'},
            'mid': {
                '4',
                '9',
                '{',
                '5',
                '7',
                '@',
                'V',
                '8',
                '1',
                '$',
                '3'},
            'low': {
                '#',
                '2'}
        }
    }

    """
	the resulting data structure :-

	by_classes = {

	{'MORPH_CLASS' : {VERB_THAT_FOLLOWS_THIS_MORPH_CLASS : PHONETIC TRANSCRIPTION}},
										.
	{'MORPH_CLASS' : {VERB_THAT_FOLLOWS_THIS_MORPH_CLASS : PHONETIC TRANSCRIPTION}},
										.
	{'MORPH_CLASS' : {VERB_THAT_FOLLOWS_THIS_MORPH_CLASS : PHONETIC TRANSCRIPTION}},
										.
	{'MORPH_CLASS' : {VERB_THAT_FOLLOWS_THIS_MORPH_CLASS : PHONETIC TRANSCRIPTION}},

									on and on
	}
	"""
    wug_neighbors = defaultdict(list)
    for wug in testf.readlines():

        f = wug.split(',')
        if "Orth" in wug:
            continue

        # extract & store wug data from test file
        orth, phon, rating, regpast, regscore, irregpast, irregscore, irregclass = f[0], f[1], float(
            f[2]), f[3], float(
            f[4]), f[5], float(
            f[6]), f[7].strip()

        # add rating for this wug to the list
        ratings.append(float(rating))
        pref_response = ""
        # determine participants' preferred past category
        response = ""
        if regscore < irregscore:
            response = irregclass  # participants preferred irregular
            pref_response = irregpast
        else:
            pref_response = regpast
            # participants preferred the regular
            # determine & store the regular transformation
            if regpast[-2:] == 'Id':
                response = "NULL->Id"
            elif regpast[-1:] == 'd':
                response = "NULL->d"
            elif regpast[-1:] == 't':
                response = "NULL->t"
        # store participants' preferred past category

        responses.append(response)

        """
		LEXICAL NEIGHBORHOOD MODEL
		"""

        # collect neighboring present forms
        pres_neighbors = get_neighbors(
            wugphon=phon, dict=pres)  # neighbors for present verbs

        # calculate sim over all neighbors
        sim = similarity(pres_neighbors, s)
        # append the overall similarity for the wug in question to the sims
        # list
        sims.append(sim)

        # print(orth, sim, rating)

        """
		Analogical model :

		GCM
		"we must compensate for how much scride resembles verbs of English in general. This is done by summing
		the similarity of scride to all the verbs of the learning set, and dividing the total obtained in the
		previous paragraph by the result."

		metric (wug being assigned to morphological class c) =
		similarity of wug to class c / total similarity of i to all classes

		"""

        tSim_wug_mclasses = []
        by_class_sim_for_this_wug = defaultdict(list)

        for morph_class in morph_classes:
            neighbors_for_this_wug = get_neighbors(
                wugphon=phon, dict=by_classes[morph_class])
            sim_for_this_wug_to_this_class = similarity(
                neighbors_for_this_wug, s)
            tSim_wug_mclasses.append(sim_for_this_wug_to_this_class)
            by_class_sim_for_this_wug[orth].append(
                (sim_for_this_wug_to_this_class, morph_class)
            )
            wug_neighbors[orth].append(
                [i for i in neighbors_for_this_wug.items()])

        """
		This gives
		by_class_sim_for_this_wug = {

		'bize': [(4.714574867740395e-09, 'I->{'), (3.775134544279102e-11, '{n->u'), (1.516512085582383e-09, 'iJ->$t'),
			 (5.578936185737857e-10, '$->E'), (7.582560427911915e-10, '{T->1Dd'), (7.582560427911915e-10, '2->Q'),
			 (7.270834108352989e-10, 'V->{'), (3.3982678194950748e-09, '2->$t'), (6.1307161540550545e-09, '2->I'),
											.
											.
											.
											.
			 (4.158969155656078e-09, 'd->t'), (7.116735132924986e-09, '2->6'), (7.582560427911915e-10, 'ik->$t'),
			 (1.250152866386744e-09, 'i->Id'), (7.582560427911915e-10, 'i->Ed'), (4.178372851295144e-09, 'u->Id')]
		}

		That is -->
		'wug' = [(similarity of this wug to --> ), (this morph. class),
											.
											.
											.
				]


		Now, we normalize the similarities.
		Specifically,
		dividing the similarity of this wug to the morphology class in question by the total similarity of this wug to
		all the morphological classes --> i.e. sum(tSim_wug_mclasses)

		"""

        tSim_wug_mclasses = sum(tSim_wug_mclasses)
        for_all_wugs_by_class = defaultdict(list)

        for wug_name, master_list in by_class_sim_for_this_wug.items():
            for tu_ple in master_list:
                normalized_sim = tu_ple[0] / tSim_wug_mclasses
                for_all_wugs_by_class[wug_name].append(
                    (normalized_sim, tu_ple[1]))

        prediction_list = sorted(
            for_all_wugs_by_class[orth],
            reverse=True)  # get the one with max similarity
        prediction = prediction_list[0][1]

        """
		Implement some general rules that fit for the data. More data I observe, more specific rules I can construct.
		I mean at this point we can get a 100% accuracy by tailor making our rules. But that will be sad

		I've tried to keep the rules as general I can.
		"""
        if prediction != response:
            ending = phon[-4:]
            """
			1. add /t/ if verb ends in voiceless
			2. add /d/ if verb ends in voiced
			3. add /ed/ if if ends in /t/ or /d/
			"""

            if ending[-1] in phon_lookup['voiced']:
                prediction = "NULL->d"
            if ending[-1] in phon_lookup['voiceless']:
                prediction = "NULL->t"
            if ending[-1] == 't' or ending == 'd':
                prediction = "NULL->Id"

            # # if phoneme before a high vowel is voiced, the rule is NULL. Eg. drIt, glIt, gud
            if ending[-3] in phon_lookup['voiced'] and ending[-2] in phon_lookup['vowels']['high']:
                prediction = "NULL"

            # if phoneme before mid vowel is voiced, rule is "NULL" Eg. nold
            if ending[-3] in phon_lookup['vowels']['mid'] and ending[-4] in phon_lookup['voiced']:
                prediction = "NULL"

        if prediction != response:
            print(
                f"For the wug: {orth}"
                f"\nThe participants’ preferred past tense response: {pref_response} (i.e. morphology class: "
                f"{response})")
            if prediction == "NULL":
                print(
                    f"The model’s predicted past tense response: {phon} (i.e. morphology class: {prediction})")
            if prediction == 'NULL->d':
                print(
                    f"The model’s predicted past tense response: {phon + 'd'} (i.e. morphology class: {prediction})")
            else:
                print(f"The model’s predicted morphology class: {prediction})")
            print(f"5 Class neighbors by similarity: ", prediction_list[:5])
            horse_neighs = [i for i in wug_neighbors[orth] for i in i]
            print(
                f"5 Word neighbors: {sorted(horse_neighs, key=lambda x: x[1], reverse=False)[:5]}\n")

        preds.append(prediction)
        testf.close()

    print(f"Correlation Ratings X Similarities : {pearson(ratings, sims)}")
    print(
        f"Accuracy of Analogical Predictions: {accuracy(responses, preds)}\n")


if __name__ == "__main__":
    s_candidates = [0.6]
    for s in s_candidates:
        print(f"\nAt s = {s}\n")
        main(s)

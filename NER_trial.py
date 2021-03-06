from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize, sent_tokenize
import fileinput


def ner_tagger(filename):
	st = StanfordNERTagger('/Users/avnish/stanford-ner-2017-06-09/classifiers/english.muc.7class.distsim.crf.ser.gz','/Users/avnish/stanford-ner-2017-06-09/stanford-ner.jar',encoding = 'utf-8')

	with open(filename, 'r',encoding = "ISO-8859-1") as f:
		text = f.read()
		tokenize = text.split()
	tagger = st.tag(tokenize)
	return tagger
# return tagger

def get_continuous_chunks(tagged_sent):
    continuous_chunk = []
    current_chunk = []

    for token, tag in tagged_sent:
        if tag != "O":
            current_chunk.append((token, tag))
        else:
            if current_chunk: # if the current chunk is not empty
                continuous_chunk.append(current_chunk)
                current_chunk = []
    # Flush the final current_chunk into the continuous_chunk, if any.
    if current_chunk:
        continuous_chunk.append(current_chunk)
    return continuous_chunk
    # conceal(continuous_chunk)

filename = '/Users/avnish/LearningNewstuff/Data_Analysis/Annonymizer/sample1.txt'
tagger = ner_tagger(filename)
print (tagger)
named_entities = get_continuous_chunks(tagger)

data_str = [" ".join([token for token, tag in ne]) for ne in named_entities]
data_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]

print(data_str)
print
print(data_str_tag)
print
for line in fileinput.input(filename, inplace=True):
	for i in data_str:
		line = line.replace(i, 'XXXXXX')
	#The print() call is a little magic here; the fileinput module temporarily replaces sys.stdout meaning that print() will write to the replacement file rather than your console. The end='' tells print() not to include a newline; that newline is already part of the original line read from the input file.
	print(line, end='')
print(data_str)


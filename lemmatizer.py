from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag.mapping import tagset_mapping
from nltk.corpus import wordnet

class Lemmatizer():
	def __init__(self):
		self.lemmatizer = WordNetLemmatizer()
		self.mapping = tagset_mapping('en-ptb', 'universal')
		self.mapping_wordnet = {
			"NOUN": wordnet.NOUN, 
			"VERB": wordnet.VERB, 
			"ADJ": wordnet.ADJ, 
			"ADV": wordnet.ADV, 
			"ADJ_SAT": wordnet.ADJ_SAT
		}
	def map_tag(self, tag):
		if tag in self.mapping:
			tag = self.mapping[tag]
			if tag in self.mapping_wordnet:
				return self.mapping_wordnet[tag]
		return None
	def lematize(self, word, pos):
		pos = self.map_tag(pos)
		if pos:
			return self.lemmatizer.lemmatize(word=word, pos=pos)
		else:
			return self.lemmatizer.lemmatize(word=word)


from entity import Token, Sentence
import stanza

class Tokenizer:
	def __init__(self):
# 		stanza.download('en', processors='tokenize', package='gum')
		self.nlp = stanza.Pipeline(lang='en', processors={'tokenize': 'gum'}, package=None)
	def tokenize(self, text):
		tokens = []
		doc = self.nlp(text)
		id = 0
		
		for sentence in doc.sentences:
			for token in sentence.tokens:
				id += 1
				tokens.append(Token(id, token.text.replace(' ', '')))
		return Sentence(text, tokens)


class Sentence:
	def __init__(self, text, tokens):
		self.text = text
		self.tokens = tokens
		self.labels = []
		
	def __str__(self):
		return '|'.join(t.text for t in self.tokens)

class Token:
	def __init__(self, id, text):
		self.id = id
		self.text = text
		self.label = None
		self.label_class = None

	def __str__(self):
		return self.text

class Mention:
	def __init__(self):
		pass

class Label:
	def __init__(self, id, phrase, assertion, typ, bone, bone_part):
		self.id = id
		self._phrase = phrase
		self.assertion = assertion.lower()
		to_list = lambda s: [t for t in s.lower().split('|') if t]
		self._typ_list = to_list(typ)
		self._bone_list = to_list(bone)
		self._bone_part_list = to_list(bone_part)
		self.keyword = None
		self.typ = []
		self.bone = []
		self.bone_part = []
	
# 	def __init__(self, id, sentence, keyword):
# 		self.id = id
# 		self.sentence = sentence
# 		self.keyword = keyword
# 		sentence.labels.append(self)

	def is_empty(self):
		return not self._phrase
	
	def bert_string(self):
		lines = []
		for token in self.sentence.tokens:
			text = token.text
			if token.label == self:
				if token == self.keyword:
					text = '**MASK**'
					cls = 'B_' + self.assertion.upper()
				else:
					cls = 'B_' + token.label_class.upper()
			else:
				cls = 'O'
			lines.append('{}\t{}'.format(text, cls))
		return '\n'.join(lines)

	def assign_to(self, sentence):
		if self.is_empty():
			return
		def assign_to_token(token, clas):
			token.label = self
			token.label_class = clas
		
		for token in sentence.tokens:
			if token.label or not token.text:
				continue
			text = token.text.lower()
			if text == self._phrase.lower():
				assign_to_token(token, 'keyword')
				self.keyword = token
				break
		if not self.keyword:
			print('Keyword not found!', sentence, self._phrase)
			return
		
		sentence.labels.append(self)
		self.sentence = sentence
		
		for token in sentence.tokens:
			if token.label or not token.text:
				continue
			text = token.text.lower()
			if text in self._typ_list:
				assign_to_token(token, 'type')
				self.typ.append(token)
				self._typ_list.remove(text)
			elif text in self._bone_list:
				assign_to_token(token, 'bone')
				self.bone.append(token)
				self._bone_list.remove(text)
			elif text in self._bone_part_list:
				assign_to_token(token, 'bone_part')
				self.bone_part.append(token)
				self._bone_part_list.remove(text)
		if self._typ_list:
			print('Type not complete!', sentence, self._typ_list)
		if self._bone_list:
			print('Bone not complete!', sentence, self._bone_list)
		if self._bone_part_list:
			print('Bone part not complete!', sentence, self._bone_part_list)
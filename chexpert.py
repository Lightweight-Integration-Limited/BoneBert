'''
Reference: https://github.com/ncbi-nlp/NegBio
'''
from collections import defaultdict
import re

def split(text):
	s = re.split(r'\W+', text)
	return [a for a in s if a.strip()]

def learn_dictionaries(labels, ignore_words=['the', 'of', 'and']):
	words = defaultdict(dict)
	def count(label, words, get_tokens, cls):
		for token in get_tokens(label):
			text = token.text.lower()
			for word in split(text):
				if cls not in words[word]:
					words[word][cls] = 1
				else:
					words[word][cls] += 1
	for label in labels:
		count(label, words, lambda x: x.typ, 'type')
		count(label, words, lambda x: x.bone, 'bone')
		count(label, words, lambda x: x.bone_part, 'bone_part')
	type_dict = {}
	bone_dict = {}
	bone_part_dict = {}
	for key, value in words.items():
		if key in ignore_words:
			continue
		category = max(value, key=value.get)
		if category == 'type':
			type_dict[key] = value[category]
		elif category == 'bone':
			bone_dict[key] = value[category]
		else:
			bone_part_dict[key] = value[category]
	return type_dict, bone_dict, bone_part_dict, words

import StanfordDependencies

def convert_to_dependencies(tree, label, lemmatizer):
	sd = StanfordDependencies.get_instance(backend='subprocess')
	conversions = sd.convert_tree(tree, representation='CCprocessed', universal=True)
	sentence = label.sentence
	for token in label.sentence.tokens:
		token.dependencies = []
	for node in conversions:
		lemma = lemmatizer.lematize(node.form, node.pos).lower()
		token = label.sentence.tokens[node.index-1]
		# token.form = node.form
		token.pos_tag = node.pos
		token.lemma = lemma
		# token.head = node.head
		# token.dependency = node.deprel
		token.dependencies.append((node.head, node.deprel))


import networkx as nx
from collections import namedtuple

def load_graph_nodes(tokens, graph):
	for token in tokens:
		graph.add_node(token.id, tag=token.pos_tag, text=token.text, lemma=token.lemma)

def load_graph_edges(tokens, graph):
	edge_id = 0
	for token in tokens:
		for (head, deprel) in token.dependencies:
			graph.add_edge(head, token.id, dependency=deprel, id=edge_id)
			edge_id += 1

def load_graph(label):
	graph = nx.DiGraph()
	load_graph_nodes(label.sentence.tokens, graph)
	load_graph_edges(label.sentence.tokens, graph)
	return graph

def has_out_edge(graph, node, dependencies):
	for _, _, d in graph.out_edges(node, data=True):
		if d['dependency'] in dependencies:
			return True
	return False

def has_out_node(graph, node, lemmas):
	for child in graph.successors(node):
		if graph.nodes[child]['lemma'] in lemmas:
			return True
	return False

def has_out(graph, node, lemmas, dependencies):
	return get_out(graph, node, lemmas, dependencies) is not None

def get_out(graph, node, lemmas, dependencies):
	for _, c, d in graph.out_edges(node, data=True):
		if d['dependency'] in dependencies and graph.nodes[c]['lemma'] in lemmas:
			return c
	return None


def propagate_graph(graph):
	Edge = namedtuple('Edge', ['gov', 'dep', 'data'])
	graph = graph.copy()

	for i in range(0, 2):
		edges = []

		for p, c, d in graph.edges(data=True):
			# propagate appos
			if d['dependency'] == 'appos':
				# x > y >appos > z
				for grandpa in graph.predecessors(p):
					edge_dep = graph[grandpa][p]['dependency']
					edges.append(Edge(grandpa, c, edge_dep))
				# x <neg < y >appos > z
				for child in graph.successors(p):
					edge_dep = graph[p][child]['dependency']
					if edge_dep == 'neg':
						edges.append(Edge(c, child, edge_dep))
			# propagate dep
			if d['dependency'] == 'dep' \
					and graph.nodes[p]['tag'].startswith('N') \
					and graph.nodes[c]['tag'].startswith('N'):
				for grandchild in graph.successors(c):
					edge_dep = graph[c][grandchild]['dependency']
					if edge_dep == 'neg':
						edges.append(Edge(p, grandchild, edge_dep))
			# propagate cop conjunction
			if d['dependency'].startswith('conj') \
					and graph.nodes[p]['tag'].startswith('N') \
					and graph.nodes[c]['tag'].startswith('N'):
				for child in graph.successors(p):
					edge_dep = graph[p][child]['dependency']
					if edge_dep in ('aux', 'cop', 'neg', 'amod'):
						edges.append(Edge(c, child, edge_dep))
					if edge_dep in ('dep', 'compound') and graph.nodes[child]['lemma'] == 'no':
						edges.append(Edge(c, child, edge_dep))
					if edge_dep == 'case' and graph.nodes[child]['lemma'] == 'without':
						edges.append(Edge(c, child, edge_dep))

			# propagate area/amount >of XXX
			if d['dependency'] == 'nmod:of' and graph.nodes[p]['lemma'] in ('area', 'amount'):
				for grandpa in graph.predecessors(p):
					edge_dep = graph[grandpa][p]['dependency']
					edges.append(Edge(grandpa, c, edge_dep))
			# propagate combination of XXX
			if d['dependency'] == 'nmod:of' and graph.nodes[p]['lemma'] == 'combination':
				for grandpa in graph.predecessors(p):
					edge_dep = graph[grandpa][p]['dependency']
					edges.append(Edge(grandpa, c, edge_dep))
			if d['dependency'] == 'nmod:of':
				for child in graph.successors(p):
					edge_dep = graph[p][child]['dependency']
					# propagate no <neg x >of XXX
					if edge_dep == 'neg':
						edges.append(Edge(c, child, edge_dep))
					# propagate without <case x >of XXX
					if edge_dep == 'case' and graph.nodes[child] == 'without':
						edges.append(Edge(c, child, edge_dep))
			# parse error
			# no xx and xxx
			if d['dependency'] == 'neg' and has_out_node(graph, p, ['or', 'and']):
				for child in graph.successors(p):
					edge_dep = graph[p][child]['dependency']
					if edge_dep == 'compound' and graph.nodes[child]['tag'].startswith('N'):
						edges.append(Edge(child, c, 'neg'))

		has_more_edges = False
		for e in edges:
			if not graph.has_edge(e.gov, e.dep):
				assert isinstance(e.data, str) or isinstance(e.data, unicode), type(e.data)
				graph.add_edge(e.gov, e.dep, dependency=e.data)
				has_more_edges = True

		if not has_more_edges:
			break
	return graph


from ngrex import compiler

class Detector():
    
	def __init__(self, pre_negation_path, 
				 post_negation_path, negation_path):
		self.pre_negation_patterns = compiler.load_patterns(pre_negation_path)
		self.post_negation_patterns = compiler.load_patterns(post_negation_path)
		self.negation_patterns = compiler.load_patterns(negation_path)
    
	def detect_pre_negation(self, graph, label):
		for pattern in self.pre_negation_patterns:
			for match in pattern.finditer(graph):
				n0 = match.group(0)
				if n0 == label.keyword.id:
					return match
		return None
    
	def detect_negation(self, graph, label):
		for pattern in self.negation_patterns:
			for match in pattern.finditer(graph):
				n0 = match.group(0)
				if n0 == label.keyword.id:
					try:
						key = match.get("key")
						if has_out_edge(graph, key, ['neg']):
							continue
					except:
						pass
					if has_out(graph, n0, ['new'], ['amod']):
						continue
					return match
		return None

	def detect_post_negation(self, graph, label):
		for pattern in self.post_negation_patterns:
			for match in pattern.finditer(graph):
				n0 = match.group(0)
				if n0 == label.keyword.id:
					return match
		return None

	def detect(self, graph, label):
		stages = [
			(self.detect_pre_negation, 'uncertain'), 
			(self.detect_negation, 'negative'),
			(self.detect_post_negation, 'uncertain'), 
		]
		for detect_func, assertion in stages:
			match = detect_func(graph, label)
			if match:
				label.pred_assertion = assertion
				label.pred_pattern = str(match.pattern)
				return
		label.pred_assertion = 'positive'
		label.pred_pattern = ''

def get_dependents(token, sentence, ignore_tokens):
	dependents = set()
	ignore_tokens.append(token)
	for token_ in sentence.tokens:
		if token_ in ignore_tokens:
			continue
		for (head, dependency) in token_.dependencies:
			if head == token.id:
				dependents.add(token_)
				dependents.update(get_dependents(token_, sentence, ignore_tokens))
	return dependents

def get_label_dependents(label):
	ignore_tokens = [l.keyword for l in label.sentence.labels]
	dependents = get_dependents(label.keyword, label.sentence, ignore_tokens)
	dependents = sorted(dependents, key=id)
	return dependents
		
def search_dependents(label, type_dict, bone_dict, bone_part_dict):
	label.pred_typ = []
	label.pred_bone = []
	label.pred_bone_part = []
	
	if len(label.sentence.labels) == 1:
		label.search_range = label.sentence.tokens
	elif label.sentence.labels.index(label) == 0:
		other_labels = [l for l in label.sentence.labels if l != label]
		other_dependents = [t for l in other_labels for t in get_label_dependents(l)]
		label.search_range = [t for t in label.sentence.tokens if t not in other_dependents]
	else:
		label.search_range = get_label_dependents(label)
	
	for token in label.search_range:
		text = token.text.lower()
		for word in split(text):
			if word in type_dict:
				label.pred_typ.append(token)
				break
			elif word in bone_dict:
				label.pred_bone.append(token)
				break
			elif word in bone_part_dict:
				label.pred_bone_part.append(token)
				break
	label.pred_typ = sorted(label.pred_typ, key=lambda x: x.id)
	label.pred_bone = sorted(label.pred_bone, key=lambda x: x.id)
	label.pred_bone_part = sorted(label.pred_bone_part, key=lambda x: x.id)

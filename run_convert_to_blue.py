from tokenizer import Tokenizer
from dataset import read_labels

tokenizer = Tokenizer()

def transform_to_bert_format(dset, tokenizer):
	labels = read_labels('train', tokenizer)
	for label in labels:
	    bert_strings.append(label.bert_string())
	with open('data/'+dset+'.bert', 'w') as f:
	    f.write('\n\n'.join(bert_strings))
	return labels

labels = read_labels('train', tokenizer)
labels = read_labels('val', tokenizer)
labels = read_labels('test', tokenizer)

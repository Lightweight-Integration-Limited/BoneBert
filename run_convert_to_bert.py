from tokenizer import Tokenizer
from dataset import read_labels

tokenizer = Tokenizer()

def transform_to_bert_format(dset, tokenizer):
	labels = read_labels(dset, tokenizer)
	for label in labels:
	    bert_strings.append(label.bert_string())
	with open('data/'+dset+'.bert', 'w') as f:
	    f.write('\n\n'.join(bert_strings))
	return labels

labels = transform_to_bert_format('train', tokenizer)
labels = transform_to_bert_format('val', tokenizer)
labels = transform_to_bert_format('test', tokenizer)

import pandas as pd
from tqdm import tqdm
from entity import Label

def read_labels(dset, tokenizer):
	df = pd.read_csv('data/annotated/'+dset+'.csv', dtype=str)
	df = df[~pd.isna(df['1_ASSERTION'])]
	
	labels = []
	
	for index, row in tqdm(df.iterrows(), total=df.shape[0]):
		sentence = tokenizer.tokenize(row['sentence'])
		replace_na = lambda x: '' if pd.isna(x) else str(x)
		for i in range(1, 4):
			label = Label(i,
						  replace_na(row['%s_PHRASE'%i]),
						  replace_na(row['%s_ASSERTION'%i]),
						  replace_na(row['%s_TYPE'%i]),
						  replace_na(row['%s_BONE'%i]),
						  replace_na(row['%s_BONE_PART'%i]),
						 )
			if label.is_empty():
				continue
			label.assign_to(sentence)
		for label in sentence.labels:
			labels.append(label)
	return labels
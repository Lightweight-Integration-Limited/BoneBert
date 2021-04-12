import pandas as pd
from tqdm import tqdm
from tokenizer import Tokenizer
from bllipparser import RerankingParser
from lemmatizer import Lemmatizer
from dataset import read_labels

from chexpert import learn_dictionaries
from chexpert import Detector
from chexpert import convert_to_dependencies
from chexpert import load_graph
from chexpert import propagate_graph
from chexpert import search_dependents

tokenizer = Tokenizer()
parser = RerankingParser.fetch_and_load('GENIA+PubMed', verbose=True)
lemmatizer = Lemmatizer()

'''
Training - Learn dictionaries for type, bone, and bone part
'''

labels = read_labels('train', tokenizer)
type_dict, bone_dict, bone_part_dict, words = learn_dictionaries(labels)
def print_tops(dic, tops=10):
    for key in sorted(dic, key=dic.get)[::-1][:tops]:
        print(key, words[key])
    print()

print('Type dict:', len(type_dict), list(type_dict.keys()), end='\n\n')
print_tops(type_dict, 20)

print('Bone dict:', len(bone_dict), list(bone_dict.keys()), end='\n\n')
print_tops(bone_dict, 20)

print('Bone part dict:', len(bone_part_dict), list(bone_part_dict.keys()), end='\n\n')
print_tops(bone_part_dict, 20)

'''
Testing
'''

labels = read_labels('test', tokenizer)

detector = Detector(
    pre_negation_path="rules/bonepert_plus/pre_negation_uncertainty.txt", 
    post_negation_path="rules/bonepert_plus/post_negation_uncertainty.txt", 
    negation_path="rules/bonepert_plus/negation.txt"
)


records = []
for label in tqdm(labels):
    tree = parser.simple_parse([t.text for t in label.sentence.tokens])
    convert_to_dependencies(tree, label, lemmatizer)
    graph = load_graph(label)
    label.graph_propagated = propagate_graph(graph)
    detector.detect(label.graph_propagated, label)
    search_dependents(label, type_dict, bone_dict, bone_part_dict)
    
    join = lambda x: '|'.join(t.text for t in x)
    records.append({
        'sentence': label.sentence.text,
        'mention_id': label.sentence.labels.index(label),
        'assertion': label.assertion,
        'type': join(label.typ),
        'bone': join(label.bone),
        'bone_part': join(label.bone_part),
        'pred_assertion': label.pred_assertion,
        'pred_type': join(label.pred_typ),
        'pred_bone': join(label.pred_bone),
        'pred_bone_part': join(label.pred_bone_part),
        'pred_pattern': label.pred_pattern,
    })

# Save results into csv file
df = pd.DataFrame.from_records(records)
df.to_csv('data/bonepert.csv')


from dataset import read_labels

def is_same_mention(label, bert_string):
    lines = bert_string.split('\n')
    if len(label.sentence.tokens) != len(lines):
        return False
    lines = [l.split(' ')[0]+'\t'+l.split(' ')[1] for l in lines]
    bert_string = '\n'.join(lines)
    return bert_string == label.bert_string()
def find_bert_string(label, bert_strings):
    for bert_string in bert_strings:
        if is_same_mention(label, bert_string):
            return bert_string
    print('Bert string not found!', label.sentence)
    return ''

# Read test set.
labels = transform_to_bert_format('test')

# Read BERT output.
with open('output_finetune/test_labels.txt', 'r') as f:
    bert_strings = f.read().split('\n\n')[:-1]
print('Bert output mentions:', len(bert_strings))

records = []
for j, label in enumerate(labels):
    label.pred_assertion = 'positive'
    label.pred_typ = []
    label.pred_bone = []
    label.pred_bone_part = []
    bert_string = find_bert_string(label, bert_strings)
    for i, line in enumerate(bert_string.splitlines()):
        token = line.split(' ')[0]
        pred = line.split(' ')[2]
        if pred in ['B_POSITIVE', 'B_NEGATIVE', 'B_UNCERTAIN', 'B_IGNORED']:
            if i+1 != label.keyword.id:
                print('Wrong assertion!', token, pred)
            else:
                label.pred_assertion = pred.lstrip('B_').lower()
        elif pred == 'B_TYPE':
            label.pred_typ.append(label.sentence.tokens[i])
        elif pred == 'B_BONE':
            label.pred_bone.append(label.sentence.tokens[i])
        elif pred == 'B_BONE_PART':
            label.pred_bone_part.append(label.sentence.tokens[i])
        else:
            assert pred == 'O'
    join = lambda x: '|'.join(t.text for t in x)
    records.append({
        'sentence': label.sentence.text,
        'assertion': label.assertion,
        'type': join(label.typ),
        'bone': join(label.bone),
        'bone_part': join(label.bone_part),
        'pred_assertion': label.pred_assertion,
        'pred_type': join(label.pred_typ),
        'pred_bone': join(label.pred_bone),
        'pred_bone_part': join(label.pred_bone_part)
    })

# Save to csv file.
df = pd.DataFrame.from_records(records)
df.to_csv('output_finetune/test.csv')

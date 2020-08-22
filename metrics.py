def calculate_scores(labels, get_truth, get_pred):
    tp = 0
    fp = 0
    fn = 0
    for label in labels:
        t_words = set(get_truth(label))
        p_words = set(get_pred(label))
        tp += len(t_words & p_words)
        fp += len(p_words - t_words)
        fn += len(t_words - p_words)
#         if t_words - p_words:
#             print(t_words - p_words)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 / (1/recall + 1/precision)
    return tp, fp, fn, precision, recall, f1

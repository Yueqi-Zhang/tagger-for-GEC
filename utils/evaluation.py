import codecs
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='dev input')

    msg = "path or pattern of dev data"
    parser.add_argument("--dev", type=str, help=msg)
    msg = "path or pattern of dev_prediction data"
    parser.add_argument("--dev_pred", type=str, help=msg)

    return parser.parse_args()

def precision_recall_f(pred, tag):
    c_p = 0
    correct_p = 0
    c_r = 0
    correct_r = 0
    for a, b in zip(tag, pred):
        if a == 'i':
            c_r += 1
            if b == a:
                correct_r += 1
        if b == 'i':
            c_p += 1
            if b == a:
                correct_p += 1
    return c_p, correct_p, c_r, correct_r

if __name__ == "__main__":
    args = parse_args()
    tags = []
    with codecs.open(args.dev, 'r') as f:
        for line in f:
            sent, tag = line.split('|||')
            tags.append(tag.split())
    preds = []
    with codecs.open(args.dev_pred, 'r') as f:
        for line in f:
            pred = line.split()
            preds.append(pred)
    c_p = 0
    correct_p = 0
    c_r = 0
    correct_r = 0
    for pred, tag in zip(preds, tags):
        a, b, c, d = precision_recall_f(pred, tag)
        c_p += a
        correct_p += b
        c_r += c
        correct_r += d
    try:
        precision = correct_p/c_p
        recall = correct_r/c_r
        f_measure = (1 + 0.5**2)*precision*recall/(0.5**2*precision + recall)
    except:
        precision = 'nothing'
        recall = 'nothing'
        f_measure = 'nothing'
    print('Precision:\t{}'.format(precision))
    print('Recall:\t{}'.format(recall))
    print('F-value\t{}'.format(f_measure))
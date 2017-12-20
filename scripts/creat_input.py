import codecs

def readdata(filepath):
    data = []
    with codecs.open(filepath, 'r') as f:
        for lines in f:
            data.append(lines.split())
    return data

dataset = readdata("/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/fce-error-detection/tsv/fce-public.test.original.tsv")
sentset = []
labelset = []
sent = []
label = []
for i in range(len(dataset)):
    if dataset[i] == []:
        sentset.append(sent)
        labelset.append(label)
        sent = []
        label = []
    else:
        sent.append(dataset[i][0])
        label.append(dataset[i][1])
output = []
#sentset_str = []
for j in range(len(sentset)):
    sent_str = ["%s" % elem for elem in sentset[j]]
    #sentset_str.append(" ".join(sent_str))
    label_str = ["%s" % elem for elem in labelset[j]]
    total_str = sent_str+["|||"]+label_str
    output.append(" ".join(total_str)+'\n')

with codecs.open("/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/fce-error-detection/tsv/fce_test", 'w') as f:
    for i in output:
        f.write(i)

#with codecs.open("/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/fce-error-detection/tsv/corpus", 'w') as f:
    #f.write(" ".join(sentset_str))


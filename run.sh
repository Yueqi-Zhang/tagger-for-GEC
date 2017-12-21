SRLPATH=/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_datdaset/tsv
TAGGERPATH=/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger
DATAPATH=/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tfrecord

export PERL5LIB="$SRLPATH/lib:$PERL5LIB"
export PATH="$SRLPATH/bin:$PATH"

python $TAGGERPATH/main.py predict --data_path $DATAPATH/fce_dev \
  --model_dir train  --model_name deepatt \
  --vocab_path $DATAPATH/word_dict $DATAPATH/label_dict \
  --device_list 0 \
  --decoding_params="decode_batch_size=512" \
  --model_params="num_hidden_layers=10,feature_size=200,hidden_size=200,filter_size=800"
  --emb_path /Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/glove/glove.6B.200d.txt

python $TAGGERPATH/utils/evaluation.py 
  --dev $DATAPATH/fce_dev
  --dev_pred $TAGGERPATH/fce_dev.deepatt.decodes

# Tagger
This is the code for the paper "[Deep Semantic Role Labeling with Self-Attention](https://arxiv.org/abs/1712.01586)".

## Usage
### Prerequisites
* python2
* A newer version of TensorFlow
* GloVe embeddings and srlconll scripts

### Data
We follow the same procedures described in the [deep_srl](https://github.com/luheng/deep_srl) repository to convert the CoNLL datasets.
The GloVe embeddings and srlconll scripts can also be found in that link.

If you followed these procedures, you can find that the processed data has the following format:
```
2 My cats love hats . ||| B-A0 I-A0 B-V B-A1 O
```

### Vocabulary
You can use the vocabularies provided in the resource directory. If you want to use your own vocabulary, you can use the `build_vocab.py`.
```
python tagger/scripts/build_vocab.py --limit LIMIT --lower TRAIN_FILE OUTPUT_DIR
```
where `LIMIT` specifies the vocabulary size. This command will create two vocabularies named `vocab.txt` and `label.txt` in the `OUTPUT_DIR`.

### Convert data format
The plain text must be converted to tf.Record format first using `input_convert.py.`.
```
python Tagger/scripts/input_converter.py --input_path Tagger/fce-error-detection/tsv/fce_input\
                                         --output_name fce_input_tf      \
                                         --output_dir Tagger/fce-error-detection/tsv\
                                         --vocab Tagger/fce-error-detection/tsv/vocab.txt Tagger/fce-error-detection/tsv/label.txt \
                                         --num_shards 1 \
                                        
```
The above command will create `NUM_SHARDS` files with pattern `NAME-*-of-*` in the `OUTPUT_DIR`.


### Training and Validating
Once you finished the procedures described above, you can start the training stage.
* Preparing the validation script

    An external validation script is required to enable the validation functionality. 
    Here's the validation script we used to train an FFN model on the CoNLL-2005 dataset.
    Please make sure that the validation script can run properly.
```
SRLPATH=/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_datdaset/tsv
TAGGERPATH=/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger
DATAPATH=/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tsv

export PERL5LIB="/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tsv/lib:$PERL5LIB"
export PATH="/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tsv/bin:$PATH"

python /Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/main.py predict --data_path /Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tsv/fce_dev \
  --model_dir train  --model_name deepatt \
  --vocab_path /Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tsv/vocab.txt /Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tsv/label.txt \
  --device_list 0 \
  --decoding_params="decode_batch_size=512" \
  --model_params="num_hidden_layers=10,feature_size=200,hidden_size=200,filter_size=800"
python $TAGGERPATH/scripts/convert_to_conll.py conll05.devel.txt.deepatt.decodes $DATAPATH/conll05.devel.props.gold.txt output
perl $SRLPATH/bin/srl-eval.pl $DATAPATH/conll05.devel.props.* output



predict
--data_path
/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tsv/fce_dev
--model_dir
train
--model_name
deepatt
--vocab_path
/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tsv/vocab.txt
/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tsv/label.txt
--device_list
0
--decoding_params="decode_batch_size=512"
--model_params="num_hidden_layers=10,feature_size=200,hidden_size=200,filter_size=800"
--emb_path
/Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/glove/glove.6B.200d.txt
```
* Training command

    The command below is what we used to train an model on the CoNLL-2005 dataset.
```
python tagger/main.py train \
    --data_path /Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/fce-error-detection/tsv --model_dir train --model_name deepatt \
    --vocab_path /Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/fce-error-detection/tsv/vocab.txt /Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/fce-error-detection/tsv/label.txt --emb_path glove.6B.100d.txt \
    --model_params=feature_size=100,hidden_size=200,filter_size=800,residual_dropout=0.2, \
                   num_hidden_layers=10,attention_dropout=0.1,relu_dropout=0.1 \
    --training_params=batch_size=4096,eval_batch_size=1024,optimizer=Adadelta,initializer=orthogonal, \
                      use_global_initializer=false,initializer_gain=1.0,train_steps=600000, \
                      learning_rate_decay=piecewise_constant,learning_rate_values=[1.0,0.5,0.25], \
                      learning_rate_boundaries=[400000,500000],device_list=[0],clip_grad_norm=1.0 \ 
    --validation_params=script=run.sh
    
    
    
    
    
    train
    --data_path
    /Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tfrecord/
    --model_dir
    train
    --model_name
    deepatt
    --vocab_path
    /Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tsv/vocab.txt
    /Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/tsv/label.txt
    --emb_path
    /Users/yueqizhang/Documents/THUNLP-Intern/errant/Tagger/Tagger/ed_dataset/glove/glove.6B.200d.txt
    --model_params=feature_size=200,hidden_size=200,filter_size=800,residual_dropout=0.2,num_hidden_layers=10,attention_dropout=0.1,relu_dropout=0.1
    --training_params=batch_size=4096,eval_batch_size=1024,optimizer=Adadelta,initializer=orthogonal,use_global_initializer=false,initializer_gain=1.0,train_steps=600000,learning_rate_decay=piecewise_constant,learning_rate_values=[1.0,0.5,0.25],learning_rate_boundaries=[400000,500000],device_list=[0],clip_grad_norm=1.0
    --validation_params=script=run.sh
```


### Decoding
The following is the command used to generate outputs:
```
python tagger/main.py predict \
    --data_path conll05.test.wsj.txt \
    --model_dir train/best --model_name deepatt \ 
    --vocab_path word_dict label_dict \
    --device_list 0 \
    --decoding_params="decode_batch_size=512" \
    --model_params="num_hidden_layers=10,feature_size=100,hidden_size=200,filter_size=800" \
    --emb_path glove.6B.100d.txt
```

### Model Ensemble
The command for model ensemble is similar to the one used in decoding: 
```
python tagger/main.py ensemble \
    --data_path conll05.devel.txt \
    --checkpoints model_1/model.ckpt model_2/model.ckpt \
    --output_name output \
    --vocab_path word_dict1 word_dict2 label_dict \
    --model_params=feature_size=100,hidden_size=200,filter_size=800,num_hidden_layers=10 \ 
    --device_list 0 \
    --model_name deepatt \
    --emb_path glove.6B.100d.txt
```

## Contact
This code is written by Zhixing Tan. If you have any problems, feel free to send an <a href="mailto:playinf@stu.xmu.edu.cn">email</a>.

## LICENSE
BSD

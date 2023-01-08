bert-base-ner-train \
    -data_dir /home/ubuntu/masai/NER-Product-brat/BERT-BiLSTM-CRF-NER-master/data/ \
    -output_dir /home/ubuntu/masai/NER-Product-brat/BERT-BiLSTM-CRF-NER-master/output\
    -init_checkpoint /home/ubuntu/masai/BERT-BiLSTM-CRF-NER-Product/BERT-BiLSTM-CRF-NER-master/chinese_ckpt/bert_model.ckpt\
    -bert_config_file /home/ubuntu/masai/BERT-BiLSTM-CRF-NER-Product/BERT-BiLSTM-CRF-NER-master/chinese_ckpt/bert_config.json\
    -vocab_file /home/ubuntu/masai/BERT-BiLSTM-CRF-NER-Product/BERT-BiLSTM-CRF-NER-master/chinese_ckpt/vocab.txt\
    -max_seq_length 64

FROM nvcr.io/nvidia/tensorflow:20.02-tf1-py3
WORKDIR /bluebert

RUN mkdir /model && cd /model/ \
	&& wget https://ftp.ncbi.nlm.nih.gov/pub/lu/Suppl/NCBI-BERT/NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12.zip \
	&& unzip NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12.zip \
	&& rm NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12.zip

RUN git clone https://github.com/ncbi-nlp/bluebert.git tmp \
	&& mv tmp/* . \
	&& rm -r tmp \
	&& cd /bluebert/bluebert



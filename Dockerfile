FROM nvcr.io/nvidia/tensorflow:20.02-tf1-py3
WORKDIR /bonebert

RUN mkdir /model && cd /model/ \
	&& wget https://ftp.ncbi.nlm.nih.gov/pub/lu/Suppl/NCBI-BERT/NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12.zip \
	&& wget https://ftp.ncbi.nlm.nih.gov/pub/lu/Suppl/NCBI-BERT/NCBI_BERT_pubmed_mimic_uncased_L-24_H-1024_A-16.zip \
	&& wget https://github.com/ncbi-nlp/BLUE_Benchmark/releases/download/0.1/bert_data.zip \
	&& unzip NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12.zip -d NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12 \
	&& unzip NCBI_BERT_pubmed_mimic_uncased_L-24_H-1024_A-16.zip -d NCBI_BERT_pubmed_mimic_uncased_L-24_H-1024_A-16 \
	&& unzip bert_data.zip \
	&& rm NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12.zip \
	&& rm NCBI_BERT_pubmed_mimic_uncased_L-24_H-1024_A-16.zip \
	&& rm bert_data.zip

RUN git clone https://github.com/ncbi-nlp/bluebert.git tmp \
	&& mv tmp/* . \
	&& rm -r tmp

ADD requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
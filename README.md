# Information Extraction for Bone Fracture Diagnosis

Author: Zhihao Dai

Supervisor: Lianghao Han



## Data

Data for training (`train.csv`), validation (`val.csv`) and testing (`test.csv`) should be stored in the directory `data/annotated`. 

Here, [`sample.csv`](sample.csv) gives a few samples from the training set.



## Usage

Run `pip -r requirements.txt` to install all the necessary packages in Python 3.



### CheXpert-based Models: PERT/PERT+

Run `run_chexpert.py`. 

By default, the code uses the manually expanded rule base in PERT+. 

To use PERT's rule base, simply replace `post_negation_uncertainty_plus.txt` with `post_negation_uncertainty.txt` and `negation_plus.txt` with `negation.txt` in the script.



### BERT-based Models: BLUE/BLUE+

Before running the code, please ensure that you have a NVIDIA GPU with at least 8GB memory.

1. Run `convert_to_blue.py` to convert all three sets from `csv` to `bert` format.

2. For BLUE, run `docker-compose up` in the `blue` directory.

3. For BLUE+, collect the extra set and use `run_chexpert.py` to generate labels for the extra set. 

   Then, run `docker-compose up` in the `blueplus` directory to fine-tune the BlueBERT model on the generated set. 

   Later, replace `docker-compose.yml` with `docker-compose.yml.2` and run the previous command again.

4. For both models, run `analyse_blue.py` to convert results in `bert` format back to `csv`.



## Acknowledgments

The code is adapted from [ncbi-nlp/NegBio](https://github.com/ncbi-nlp/NegBio) and [ncbi-nlp/BlueBERT](https://github.com/ncbi-nlp/bluebert).

We are grateful for the authros of NegBio, CheXpert-labeller, and BlueBERT.














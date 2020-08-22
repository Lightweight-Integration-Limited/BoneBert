# Information Extraction for Bone Fracture Diagnosis

Author: Zhihao Dai

Supervisor: Lianghao Han



```
Radiologists make the diagnoses of bone fractures through examining X-ray radiographs and document them in radiology reports.
Applying information extraction techniques on such radiology reports could yield a source of structured data for medical cohort studies, image labelling and decision support concerning bone fractures.
In this research, we demonstrate the applicability of the CheXpert-labeler[1] and CheXbert[2], two popular labellers originally designed for Chest X-ray radiology reports, to information extraction of radiology reports for bone fracture diagnosis.
We implement two kinds of information extraction systems and compare their performances on a dataset of 13,712 X-ray radiology reports and 4,899 annotations.
The BERT-based system, incorporating weak supervision from the CheXpert-labeller-based system, achieves 99.88% F1 score in the Assertion Classification subtask and 92.95% in the Named Entity Recognition subtask.
From a radiology report, the system extracts the assertion, type and location information corresponding to each mention of fracture in a structured format.
```



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



## References

```
[1] Irvin, J., Rajpurkar, P., Ko, M., Yu, Y., Ciurea-Ilcus, S., Chute, C., Mark- lund, H., Haghgoo, B., Ball, R., Shpanskaya, K., Seekins, J., Mong, D. A., Halabi, S. S., Sandberg, J. K., Jones, R., Larson, D. B., Langlotz, C. P., Patel, B. N., Lungren, M. P., and Ng, A. Y. (2019). CheXpert: A Large Chest Radiograph Dataset with Uncertainty Labels and Expert Compari- son. Proceedings of the AAAI Conference on Artificial Intelligence, 33:590– 597.
[2] Peng, Y., Wang, X., Lu, L., Bagheri, M., Summers, R., and Lu, Z. (2018). NegBio: a high-performance tool for negation and uncertainty detection in radiology reports. AMIA Joint Summits on Translational Science pro- ceedings. AMIA Joint Summits on Translational Science, 2017:188–196.
```












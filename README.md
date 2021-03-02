# bert-multilable-patent-classification
Multilabel classification of patents (based on their highest level IPC classification) using BERT



Requirements
------------

Install requirements text classification with pip:

```
pip install numpy pytorch scipy pandas pytorch_pretrained_bert fastai pandas tqdm apex
```
(You can use anaconda or other tools depending on your Python installation.)

Steps
-----------
1. Downloading dataset
2. Parsing the patent file
```
cd codes
python3 parse_patent.py
```
3. Data preprocessing and dataset spilitting:
```
cd codes
python3 data_prepocessing.py
```
5. Downloading pre-trained Bert Model (bert-base-uncased) for pytorch, and unzip it to:
```
/trained_models/bert
```
7. Fine tuning the model and doing the multi-label classification task:
```
cd codes
python3 patent_classification.py
```
8. Fine tuned model will be saved in:
```
/trained_models/bert/fine_tuned_models
```
9. Output of validation and test will be saved in:
```
/Output
```



More details for each step are provided in the following.

Dataset
-----------
You should download one or a group of patent xml files from https://bulkdata.uspto.gov for this project.
The current version of the code works with "ipg210105.xml", that can be downloaded from:
https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2021/
After downloading, you should unzip it and put in "/data" folder.
(Because of its large size it is not included in this repository.)

Experiments
-----------

Run models:

```
cd codes
python3 patent_classification.py
```

This model is fine tuned and tested on one US patent file (ipg210105.zip), but you can download more datasets from https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2021/. 
In that case, you should first parse the patent:

```
cd codes
python3 parse_patent.py
```
(Jupyter notebook version is also available: data/patent_parsing.ipynb)

and then pre-process and split your dataset:
```
cd codes
python3 patent_classification.py
```
(Jupyter notebook version is also available: codes/data_preproc.ipynb)

Because of size limitation of repo, the based pre-trained Bert is not uploaded here. You need to download the BERT model (uncased_L-12_H-768_A-12) for pytorch inadvance, and put in "/train_models/bert" folder before running the model.

Trained Models
-----------

The fine-tuned BERT model for Patent classification can be downloaded from:
```
trained_models/bert/fine_tuned_models
```

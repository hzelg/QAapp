from sklearn.metrics import cohen_kappa_score
from krippendorff import alpha
import pandas as pd
import numpy as np

# Clarity:

df1 = pd.read_csv("./data/annotation.csv")
annotator1 = [int(i) for i in df1["clarity_1"].tolist()]
annotator2 = df1["clarity_2"].tolist()
annotators = [annotator1,annotator2]


kappa = cohen_kappa_score(annotator1, annotator2, weights='quadratic')
print("Cohen' kappa: ", kappa)

# Calculate Fleiss' kappa
kappa = alpha(reliability_data=annotators, level_of_measurement='nominal')
print("Fleiss' kappa:", kappa)


# Pedagogy:

annotator1_p = [str(i).split(",") for i in df1["pedagogy_1"].tolist()]
annotator2_p = [str(i).split(",") for i in df1["pedagogy_2"].tolist()]

# Flatten the annotation lists to get a list of label combinations
kappa_scores = []

for labels1, labels2 in zip(annotator1_p, annotator2_p):
    common_labels = list(set(labels1) & set(labels2))
    agreement = len(common_labels) / max(len(labels1), len(labels2))
    kappa_scores.append(agreement)

# Calculate the average kappa score
average_kappa = sum(kappa_scores) / len(kappa_scores)
print("Average Cohen's kappa:", average_kappa)
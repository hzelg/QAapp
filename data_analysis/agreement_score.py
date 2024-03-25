from sklearn.metrics import cohen_kappa_score

annotator1 = [0, 1, 1, 0, 1]
annotator2 = [0, 1, 0, 0, 1]

kappa = cohen_kappa_score(annotator1, annotator2, weights='linear')

# weights='quadratic'
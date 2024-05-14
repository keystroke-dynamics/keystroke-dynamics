import numpy as np
import tqdm
from sklearn.metrics import roc_curve
from sklearn.mixture import GaussianMixture
import csv

TRAIN_SIZE = 0.5

vectors = []
users = []
with open("keystrokes.csv", "r") as file:
    file.readline()
    reader = csv.reader(file)
    data = list(reader)
    for row in data:
        vector = np.array(row[3:], dtype=float)
        vectors.append(vector)
        users.append(int(row[0].lstrip('s')))
vectors = np.array(vectors)
users = np.array(users)

for n_components in [2]:
    fprs = []
    fnrs = []
    net_eer = 0
    for user in tqdm.tqdm(np.unique(users), unit='user', disable=True):
        user_vectors = vectors[users == user]
        user_train_vectors, user_test_vectors = user_vectors[:int(len(user_vectors)*TRAIN_SIZE), :], user_vectors[int(len(user_vectors)*TRAIN_SIZE):, :]
        
        model = GaussianMixture(n_components=n_components, covariance_type='diag')
        model.fit(user_train_vectors)

        scores = []
        user_is_imposter = []

        neg_user_scores = -model.score_samples(user_test_vectors)
        neg_imposter_scores = -model.score_samples(vectors[users != user])
        scores = np.concatenate([neg_user_scores, neg_imposter_scores])
        user_is_imposter = np.concatenate([np.zeros(len(neg_user_scores)), np.ones(len(neg_imposter_scores))])

        # Imposter = Positive
        # False positive: Falsely identified as imposter <- False rejection rate
        # False negative: Falsely identified as user     <- False acceptance rate
        fpr, tpr, thresholds = roc_curve(user_is_imposter, scores, pos_label=True)
        fnr = 1 - tpr

        differences = np.absolute(fnr - fpr)
        approx_eer = fpr[np.argmin(differences)]
        net_eer += approx_eer

        fprs.append(fpr)
        fnrs.append(fnr)
        
    print(f"Average EER for n_components={n_components}: {net_eer/len(np.unique(users))}")
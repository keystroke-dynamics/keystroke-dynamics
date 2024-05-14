import numpy as np
from scipy.spatial import distance
from sklearn.metrics import roc_curve
import csv

STD_THRESHOLD = 2
TRAIN_SIZE = 0.75

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

net_eer = 0
for user in np.unique(users):
    user_vectors = vectors[users == user]
    user_train_vectors, user_test_vectors = user_vectors[:int(len(user_vectors)*TRAIN_SIZE), :], user_vectors[int(len(user_vectors)*TRAIN_SIZE):, :]
    mean = np.mean(user_train_vectors, axis=0)
    stddev = np.std(user_train_vectors, axis=0)

    filtered_indices = []
    reject = []
    for i, vector in enumerate(user_train_vectors):
        dist = distance.euclidean(mean, vector)
        if np.all(dist > STD_THRESHOLD * stddev):
            reject.append(i)
        else:
            filtered_indices.append(i)

    filtered_vectors = user_train_vectors[filtered_indices]
    filtered_mean = np.mean(filtered_vectors, axis=0)

    mdists = []
    user_is_imposter = []

    # Self test
    for vector in user_test_vectors:
        mdist = distance.cityblock(filtered_mean, vector)
        mdists.append(mdist)
        user_is_imposter.append(False)

    # Imposter test
    for i in range(len(vectors)):
        if users[i] == user:
            continue
        test_vector = vectors[i]
        mdist = distance.cityblock(filtered_mean, test_vector)
        mdists.append(mdist)
        user_is_imposter.append(True)

    # Imposter = Positive
    # False positive: Falsely identified as imposter <- False rejection rate
    # False negative: Falsely identified as user     <- False acceptance rate
    fpr, tpr, thresholds = roc_curve(user_is_imposter, mdists, pos_label=True)
    fnr = 1 - tpr

    differences = np.absolute(fnr - fpr)
    approx_eer = fpr[np.argmin(differences)]
    net_eer += approx_eer

print(f"Average EER: {net_eer/len(np.unique(users))}")
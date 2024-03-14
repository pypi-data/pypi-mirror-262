import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

def train_logistic_ratio_classifier(X_train, X_test):
    combined_X = np.vstack((X_train, X_test))
    labels = np.concatenate((np.ones(len(X_train)), np.zeros(len(X_test))))
    classifier = LogisticRegression(max_iter=1000)
    classifier.fit(combined_X, labels)
    return classifier

def estimate_density_ratio(x, classifier):
    prob_Q1 = classifier.predict_proba(x.reshape(-1, 1))[0, 1]
    return prob_Q1 / (1 - prob_Q1)


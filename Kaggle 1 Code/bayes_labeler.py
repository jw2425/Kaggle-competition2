import numpy as np
from sklearn.naive_bayes import GaussianNB

def label():
    features = np.loadtxt("Extracted_features.csv", delimiter=",")
    similarities_3 = np.loadtxt("similarities_3.csv", delimiter=",")

    clf = GaussianNB()
    clf.fit(features[:6000], similarities_3)

    out = clf.predict(features[6000:])
    out = [(0, int(x)) for x in out]
    for i in range(4000):
        out[i] = (6000+i+1, out[i][1])
    out.insert(0, ("Id","Label"))

    return out

if __name__ == '__main__':
    labels = label()
    np.savetxt("labels.csv", labels, fmt='%s', delimiter=",")


# coding:utf8
import numpy as np


def data_vector_calculator(vectors):
    # gram矩阵
    gram = []
    for i in range(len(vectors)):
        gram.append([])
        for j in range(len(vectors)):
            gram[i].append(np.dot(vectors[i], vectors[j]))

    a = np.mat(gram)

    volume = np.linalg.det(a)
    return volume

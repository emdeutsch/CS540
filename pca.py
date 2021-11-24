from scipy.linalg import eigh
import numpy as np
#import matplotlib.pyplot as plt
import math
import matplotlib

matplotlib.use('Agg')

def load_and_center_dataset(filename):
    loaded = np.load(filename)
    reshaped = np.reshape(loaded, (2000, 784))
    mean = np.mean(reshaped, axis=0)
    centered = reshaped - mean
    return centered

def get_covariance(dataset):
    covariance = np.zeros((len(dataset[0]), len(dataset[0])), float)
    n = len(dataset)
    for i in range(len(dataset)):
        x = np.array(dataset[i])
        x = np.array([x])
        x_t = np.transpose(x)
        covariance += np.dot(x_t, x)
    covariance = covariance/(n-1)
    return covariance

def get_eig(S, m):
    eigenValues, eigenVectors = eigh(S)
    eigenValues, eigenVectors = eigh(S, eigvals=(len(eigenValues) - 1 - (m-1), len(eigenValues) - 1))
    i = eigenValues.argsort()[::-1]
    eigenValues = eigenValues[i]
    eigenVectors = eigenVectors[:, i]
    Lambda = np.zeros((len(eigenValues), len(eigenValues)), float)
    np.fill_diagonal(Lambda, eigenValues)
    return Lambda, eigenVectors
def get_eig_perc(S, perc):
    original_eigenValues, original_eigenVectors = eigh(S)
    j = 1
    slice = False
    final_eigenValues = None
    final_eigenVectors = None
    while not slice:
        eigenValues, eigenVectors = eigh(S, eigvals=(len(original_eigenValues) - 1 - (j - 1), len(original_eigenVectors) - 1))
        i = eigenValues.argsort()[::-1]
        eigenValues = eigenValues[i]
        eigenVectors = eigenVectors[:, i]
        perc_of_variance = eigenValues[-1]/np.sum(original_eigenValues)
        if perc_of_variance <= perc:
            slice = True
        else:
            final_eigenValues = eigenValues
            final_eigenVectors = eigenVectors
        j += 1
    Lambda = np.zeros((len(final_eigenValues), len(final_eigenValues)), float)
    np.fill_diagonal(Lambda, final_eigenValues)
    return Lambda, final_eigenVectors
def project_image(image, U):
    m = len(U[0])
    j = 1
    projection = np.zeros((len(U), 1), float)
    U_t = np.transpose(U)
    image = np.array([image])
    while j <= m:
        x = np.array(U_t[j-1])
        x = np.array([x])
        x_t = np.transpose(x)
        projection += np.dot(np.dot(x_t, image), x_t)
        j += 1
    return projection

def display_image(orig, proj):
    orig = np.reshape(orig, (int(math.sqrt(len(orig))), int(math.sqrt(len(orig)))))
    proj = np.reshape(proj, (int(math.sqrt(len(proj))), int(math.sqrt(len(proj)))))
    matplotlib.pyplot.savefig("test.png")
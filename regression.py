# Evan Deutsch
# CS540
# 11/16/2020
import csv
import numpy as np
from math import sqrt
from math import pow
import random

def get_dataset(filename):
    dataset = []
    file = open(filename, 'r')
    reader = csv.reader(file)
    i = 0
    for row in reader:
        j = 0
        temp_data = []
        if i != 0:
            for data in row:
                if j != 0:
                    temp_data.append(float(data))
                j += 1
            dataset.append(temp_data)
        i += 1
    dataset = np.array(dataset)
    return dataset

def print_stats(dataset, col):
    num_points = len(dataset)
    sum = 0
    for data_point in dataset:
        sum += data_point[col]
    mean = sum/num_points
    variance = 0
    for data_point in dataset:
        variance += pow(data_point[col] - mean, 2)
    variance = variance/(num_points-1)
    sd = sqrt(variance)
    print(num_points)
    print(round(mean*100)/100)
    print(round(sd*100)/100)


def regression(dataset, cols, betas):
    augmented_matrix = []
    for data_point in dataset:
        temp_data = []
        temp_data.append(data_point[0])
        for i in cols:
            temp_data.append(data_point[i])
        augmented_matrix.append(temp_data)
    beta_sum = 0
    for row in augmented_matrix:
        temp_beta_sum = betas[0] - row[0]
        for i in range(len(betas)):
            if i != 0:
                temp_beta_sum += betas[i]*row[i]
        temp_beta_sum = pow(temp_beta_sum, 2)
        beta_sum += temp_beta_sum
    beta_sum = beta_sum/len(dataset)
    return beta_sum

def gradient_descent(dataset, cols, betas):
    gradient_descent_array = []
    augmented_matrix = []
    for data_point in dataset:
        temp_data = []
        temp_data.append(data_point[0])
        for i in cols:
            temp_data.append(data_point[i])
        augmented_matrix.append(temp_data)
    for i in range(len(betas)):
        gradient_sum = 0
        for row in augmented_matrix:
            temp_gradient_sum = betas[0] - row[0]
            for j in range(len(betas)):
                if j != 0:
                    temp_gradient_sum += betas[j] * row[j]
            if i != 0:
                temp_gradient_sum *= row[i]
            gradient_sum += temp_gradient_sum
        gradient_sum = (gradient_sum * 2) / len(dataset)
        gradient_descent_array.append(gradient_sum)

    gradient_descent_array = np.array(gradient_descent_array)
    return gradient_descent_array

def gradient_descent_sgd(dataset, cols, betas, rand_index):
    gradient_descent_array = []
    augmented_matrix = []
    for data_point in dataset:
        temp_data = []
        temp_data.append(data_point[0])
        for i in cols:
            temp_data.append(data_point[i])
        augmented_matrix.append(temp_data)
    for i in range(len(betas)):
        row = augmented_matrix[rand_index]
        gradient_sum = betas[0] - row[0]
        for j in range(len(betas)):
            if j != 0:
                gradient_sum += betas[j] * row[j]
        if i != 0:
            gradient_sum *= row[i]
        gradient_sum = (gradient_sum * 2)
        gradient_descent_array.append(gradient_sum)

    gradient_descent_array = np.array(gradient_descent_array)
    return gradient_descent_array


def iterate_gradient(dataset, cols, betas, T, eta):
    previous_betas = []
    for beta in betas:
        previous_betas.append(beta)
    for i in range(T):
        new_betas = []
        for j in range(len(betas)):
            new_betas.append(previous_betas[j]-eta*gradient_descent(dataset, cols, previous_betas)[j])
        print(str(i+1) + " " + str(round(regression(dataset, cols, new_betas)*100)/100), end=" ")
        previous_betas = []
        for beta in new_betas:
            print(round(beta*100)/100, end=" ")
            previous_betas.append(beta)
        print()

def compute_betas(dataset, cols):
    x = []
    y = []
    for data_point in dataset:
        temp_data = [1]
        y.append(data_point[0])
        for i in cols:
            temp_data.append(data_point[i])
        x.append(temp_data)
    betas = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(x), x)), np.transpose(x)), y)
    output = [regression(dataset, cols, betas)]
    for beta in betas:
        output.append(beta)
    return tuple(output)

def predict(dataset, cols, features):
    computed_betas = compute_betas(dataset, cols)
    predicted_value = computed_betas[1]
    for i in range(len(computed_betas)):
        if i > 1:
            predicted_value += computed_betas[i]*features[i-2]
    return predicted_value

def sgd(dataset, cols, betas, T, eta):
    random.seed(42)
    random_generator = random_index_generator(0, len(dataset))

    previous_betas = []
    for beta in betas:
        previous_betas.append(beta)
    for i in range(T):
        new_betas = []
        rand_int = next(random_generator)
        for j in range(len(betas)):
            new_betas.append(previous_betas[j] - eta * gradient_descent_sgd(dataset, cols, previous_betas, rand_int)[j])
        print(str(i + 1) + " " + str(round(regression(dataset, cols, new_betas)*100)/100), end=" ")
        previous_betas = []
        for beta in new_betas:
            print(round(beta * 100) / 100, end=" ")
            previous_betas.append(beta)
        print()

def random_index_generator(min_val, max_val, seed=42):
    """
    DO NOT MODIFY THIS FUNCTION.
    DO NOT CHANGE THE SEED.
    This generator picks a random value between min_val and max_val,
    seeded by 42.
    """
    random.seed(seed)
    while True:
        yield random.randrange(min_val, max_val)
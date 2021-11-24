# Evan Deutsch
# CS 540
# 11/7/2020

import csv
from math import sqrt
from math import pow
import numpy as np

def load_data(filepath):
    pokemon_dict = []
    file = open(filepath, 'r')
    reader = csv.DictReader(file)
    i = 1
    for pokemon in reader:
        del pokemon['Generation']
        del pokemon['Legendary']
        pokemon_dict.append(pokemon)
        if i == 20:
            break
        i += 1
    return pokemon_dict


def calculate_x_y(stats):
    return (stats['Attack'] + stats['Sp. Atk'] + stats['Speed'], stats['Defense'] + stats['Sp. Def'] + stats['HP'])


def hac(dataset):
    all_clusters = []
    cluster_list = []
    points = []
    hac = []
    for pokemon in dataset:
        point = calculate_x_y(pokemon)
        cluster_list.append([point])
        all_clusters.append([point])
        points.append(point)
    while len(hac) < len(dataset) - 1:
        min_dist = float(100000000000)
        min_index_1 = None
        min_index_2 = None
        for cluster_1 in cluster_list:
            for point_1 in cluster_1:
                for cluster_2 in cluster_list:
                    for point_2 in cluster_2:
                        if point_2 not in cluster_1:
                            euclidean = euclidean_distance(point_1, point_2)
                            tie_break = False
                            if euclidean == min_dist:
                                if min([all_clusters.index(cluster_1), all_clusters.index(cluster_2)]) == all_clusters.index(cluster_list[min_index_1]):
                                    if max([all_clusters.index(cluster_1), all_clusters.index(cluster_2)]) < all_clusters.index(cluster_list[min_index_2]):
                                        tie_break = True
                                if min([all_clusters.index(cluster_1), all_clusters.index(cluster_2)]) < all_clusters.index(cluster_list[min_index_1]):
                                    tie_break = True
                            if euclidean < min_dist or tie_break:
                                min_dist = euclidean
                                min_index_1 = cluster_list.index(cluster_1)
                                min_index_2 = cluster_list.index(cluster_2)
                                if all_clusters.index(cluster_list[min_index_1]) > all_clusters.index(cluster_list[min_index_2]):
                                    temp = min_index_1
                                    min_index_1 = min_index_2
                                    min_index_2 = temp

        all_clusters.append(cluster_list[min_index_1] + cluster_list[min_index_2])
        cluster_list.append(cluster_list[min_index_1] + cluster_list[min_index_2])
        hac.append([all_clusters.index(cluster_list[min_index_1]), all_clusters.index(cluster_list[min_index_2]), min_dist, len(cluster_list[min_index_1]) + len(cluster_list[min_index_2])])
        cluster_list.remove(cluster_list[min_index_1])
        cluster_list.remove(cluster_list[min_index_2 - 1])

    hac = np.array(hac)

    return hac

def euclidean_distance(point_1, point_2):
    return sqrt(pow(float(point_1[0]) - float(point_2[0]), 2) + pow(float(point_1[1]) - float(point_2[1]), 2))

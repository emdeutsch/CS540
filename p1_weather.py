# Evan Deutsch
# CS540
# September 15, 2020
from operator import itemgetter
def manhattan_distance(data_point1, data_point2):
    x1 = float(data_point1["TMAX"])
    x2 = float(data_point2["TMAX"])
    y1 = float(data_point1["PRCP"])
    y2 = float(data_point2["PRCP"])
    z1 = float(data_point1["TMIN"])
    z2 = float(data_point2["TMIN"])
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
def read_dataset(filename):
    weather_file = open(filename, "r")
    weather = weather_file.readlines()
    data = []
    for i in range(len(weather)):
        day = weather[i].split()
        temp_dictionary_day = {
            "DATE": day[0],
            "TMAX": day[2],
            "PRCP": day[1],
            "TMIN": day[3],
            "RAIN": day[4],
        }
        data.append(temp_dictionary_day)
    weather_file.close()
    return data

def majority_vote(nearest_neighbors):
    false_count = 0
    true_count  = 0
    return_value = "TRUE"
    for i in range(len(nearest_neighbors)):
        if nearest_neighbors[i]["RAIN"] == "FALSE":
            false_count += false_count + 1
        else:
            true_count += true_count + 1
    if false_count > true_count:
        return_value = "FALSE"
    return return_value

def k_nearest_neighbors(filename, test_point, k, year_interval):
    data = read_dataset(filename)
    year = int(test_point["DATE"][0:4])
    lower_year = year - year_interval
    higher_year = year + year_interval
    in_range = []
    for i in range(len(data)):
        temp_year = int(data[i]["DATE"][0:4])
        if temp_year > lower_year and temp_year < higher_year:
            in_range.append(data[i])
    if len(in_range) == 0:
        return "TRUE"
    elif len(in_range) <= k:
        return majority_vote(in_range)
    else:
        sorting = []
        for i in range(len(in_range)):
            sorting.append(
                {
                    "INDEX" : i,
                    "MD": manhattan_distance(test_point, in_range[i])
                }
            )
        sorting.sort(key=itemgetter("MD"))
        nearest_neighbors = []
        for i in range(0, k):
            nearest_neighbors.append(in_range[sorting[i]["INDEX"]])
        return majority_vote(nearest_neighbors)





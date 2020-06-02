from collections import Counter
import math

def knn(grid, query_node, k, distance_fn, choice_fn):
    neighbor_distances_and_indices = []
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if( grid[i][j].x == query_node.x and grid[i][j].y == query_node.y):
                pass
            else:
                distance = distance_fn(grid[i][j],query_node)
                neighbor_distances_and_indices.append((distance,i,j))

    
    sorted_neighbor_distances_and_indices = sorted(neighbor_distances_and_indices)
    
    k_nearest_distances_and_indices = sorted_neighbor_distances_and_indices[:k]
    
    k_nearest_labels = [grid[i][j].color for distance, i, j in k_nearest_distances_and_indices]

    return k_nearest_distances_and_indices , choice_fn(k_nearest_labels)

def mean(labels):
    return sum(labels) / len(labels)

def mode(labels):
    return Counter(labels).most_common(1)[0][0]

def euclidean_distance(point1, point2):
    sum_squared_distance = 0
    for i in range(len(point1)):
        sum_squared_distance += math.pow(point1[i] - point2[i], 2)
    return math.sqrt(sum_squared_distance)
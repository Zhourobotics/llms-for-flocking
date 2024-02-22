import math


def calcDistVec(start_pos, end_pos):
    dist_vec = []
    for i in range(len(end_pos)):
        dist_vec.append(end_pos[i] - start_pos[i])
    return dist_vec


def calcDist(start_pos, end_pos):
    return mag(calcDistVec(start_pos, end_pos))


def calcRepelVec(dist_vec, repel_factor):
    # Calculate the factor based on the repel_factor and distance
    distance = mag(dist_vec)
    factor = -repel_factor / distance

    # Multiply each element in dist_vec by the factor
    repel_vec = [d * factor for d in dist_vec]

    return repel_vec


def mag(vector):
    return math.sqrt(sum(comp ** 2 for comp in vector))


def averageVec(vectors):
    if not vectors or len(vectors) == 0:
        # Return a zero vector of a default size or handle this case as needed
        # For example, returning a zero vector of size 3 if that's the expected size
        return [0, 0, 0]

    # Initialize a list to store the sum of each component
    sum_components = [0] * len(vectors[0])

    # Sum up each component of each vector
    for vector in vectors:
        for i, component in enumerate(vector):
            sum_components[i] += component

    # Calculate the average of each component
    num_vectors = len(vectors)
    avg_vector = [sum_comp / num_vectors for sum_comp in sum_components]

    return avg_vector


def weightVec(vec, weight):
    return [component * weight for component in vec]


def sumVec(vectors):
    # Initialize a vector of zeros with the same dimension as the first vector in the list
    sum_vector = [0] * len(vectors[0]) if vectors else []

    for vec in vectors:
        sum_vector = [sum_comp + vec_comp for sum_comp, vec_comp in zip(sum_vector, vec)]

    return sum_vector


def interpVec(initialVec, endVec, interpStrength):
    # Ensure interpStrength is within bounds
    interpStrength = max(0, min(interpStrength, 1))

    # Calculate the interpolated vector
    interpVect = [(1 - interpStrength) * iv + interpStrength * ev for iv, ev in zip(initialVec, endVec)]

    return interpVect


def normalize(vector):
    distance = mag(vector)
    return [component / distance for component in vector]

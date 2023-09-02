import numpy as np
from satellites import *

# returns a list of all times where GPS signals were received
def pseudorange_times(gps_list: list[GPSSatellite]) -> np.ndarray:
    all_times = []

    for i in range(0, len(gps_list)):
        all_times.extend(gps_list[i].times_of_pseudoranges)

    all_times = np.unique(all_times)

    return all_times

# calculate positions from list og GPS signals
def estimate_positions(gps_list: list[GPSSatellite]) -> np.ndarray:
    # iterations for Newton-Raphson method
    iterations = 10

    all_times = pseudorange_times(gps_list)

    # calculate ecef positions of GPS satellites
    ecef_positions = []

    for i in range(0, len(gps_list)):
        ecef_positions.append(gps_list[i].position_ecef())

    # list of all calculated estimated positions
    estimated_positions = []

    # Choose at least 4 satellites at same time
    for i in range(0, len(all_times)):
        svs = []
        ecefs = []
        pseudoranges = []

        for j in range(0, len(gps_list)):
            # get index of pseudorange time measurement
            index = np.where(gps_list[j].times_of_pseudoranges == all_times[i])

            if index[0].size != 0:
                svs.append(gps_list[j].sv)

                ecefs.append(ecef_positions[j][index][0])

                pseudoranges.append(gps_list[j].pseudoranges[index][0])

        if len(svs) >= 4:
            assumed_pos = np.array([0, 0, 0])
            clock_bias = 0

            pseudoranges = np.array(pseudoranges)

            for iteration in range(0, iterations):
                line_of_sight_vectors = []
                unit_vectors = []

                assumed_ranges = []

                # calculate line_of_sight_vectors, assumed_ranges and unit_vectors
                for i in range(0, len(ecefs)):
                    line_of_sight_vector = ecefs[i] - assumed_pos
                    line_of_sight_vectors.append(line_of_sight_vector)

                    assumed_range = np.sqrt(np.dot(line_of_sight_vector, line_of_sight_vector))
                    assumed_ranges.append(assumed_range)

                    unit_vectors.append(line_of_sight_vector / assumed_range)

                line_of_sight_vectors = np.array(line_of_sight_vectors)
                unit_vectors = np.array(unit_vectors)

                assumed_ranges = np.array(assumed_ranges)

                delta_tau = pseudoranges - assumed_ranges - clock_bias

                # construct geometry matrix
                geometry_matrix = []

                for i in range(0, len(unit_vectors)):
                    row = []
                    row.extend(-unit_vectors[i])
                    row.append(1)
                    geometry_matrix.append(row)

                geometry_matrix = np.matrix(geometry_matrix)

                geometry_matrix_pseudo_inverse = np.linalg.pinv(geometry_matrix)

                delta_pos_time = np.copy(np.matmul(geometry_matrix_pseudo_inverse, delta_tau))[0]

                delta_pos = delta_pos_time[0:3]
                delta_time = delta_pos_time[3]

                assumed_pos = assumed_pos + delta_pos
                clock_bias = clock_bias + delta_time

            estimated_positions.append(assumed_pos)

    estimated_positions = np.array(estimated_positions)

    return estimated_positions

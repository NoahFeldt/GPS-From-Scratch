import numpy as np
from Satellites import *

# (Copied from Stack Overflow)
# Find the intersection of three spheres
# P1, P2, P3 are the centers, r1, r2, r3 are the radii
# Implementaton based on Wikipedia Trilateration article.
def trilaterate(P1, P2, P3, r1, r2, r3):
    temp1 = P2 - P1
    e_x = temp1 / np.linalg.norm(temp1)
    temp2 = P3 - P1
    i = np.dot(e_x, temp2)
    temp3 = temp2 - i * e_x
    e_y = temp3 / np.linalg.norm(temp3)
    e_z = np.cross(e_x, e_y)
    d = np.linalg.norm(P2 - P1)
    j = np.dot(e_y,temp2)
    x = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    y = (r1 * r1 - r3 * r3 -2 * i * x + i * i + j * j) / (2 * j)
    temp4 = r1 * r1 - x * x - y * y

    if temp4 < 0:
        # raise Exception("The three spheres do not intersect!")
        return None

    z = np.sqrt(temp4)
    p_12_a = P1 + x * e_x + y * e_y + z * e_z
    p_12_b = P1 + x * e_x + y * e_y - z * e_z

    return p_12_a, p_12_b 

def distance_to_origin(array: np.ndarray):
    return np.linalg.norm(array)

def tri_pos(gps_list: list[GPSSatellite]):
    # create list of all times
    all_times = []

    for i in range(0, len(gps_list)):
        all_times.extend(gps_list[i].times_of_pseudoranges)

    all_times = np.unique(all_times)

    tris = []

    # Choose first at least 3 satellites at same time
    for i in range(0, len(all_times)):
        centers = []
        radii = []

        for j in range(0, len(gps_list)):

            index = np.where(gps_list[j].times_of_pseudoranges == all_times[i])

            if index[0].size != 0:
                centers.append(np.copy(gps_list[j].position()[index])[0])
                radii.append(gps_list[j].pseudoranges[index][0])

            if len(centers) == 3:
                m = max(np.max(centers).any(), max(radii))

                positions = trilaterate(centers[0], centers[1], centers[2], radii[0], radii[1], radii[2])

                # if positions == None:
                #     break

                # dist1 = distance_to_origin(positions[0])
                # dist2 = distance_to_origin(positions[1])

                print(f"centers: {centers / m}")
                print(f"radii  : {radii / m}")
                print(f"ToP    : {gps_list[j].times_of_pseudoranges[index]}")
                print(f"scale f: {m}")
                print(f"{gps_list[j].times_of_pseudoranges[index] % 86400}")
                exit(1)

                if dist1 <= dist2:
                    tris.append(positions[0])
                else:
                    tris.append(positions[1])

                break

    return np.array(tris)

        #     if np.isin(gps_list[0].times_of_pseudoranges, all_times[i]).any():

        #         # print(f"i: {i}, j: {j}, time: {all_times[i]}")

        #         centers.append(np.copy(gps_list[j].position())[i])

def tri_pos1(gps_list: list[GPSSatellite]):
    tris = []

    for i in range(0, len(gps_list[0].pseudoranges)):
        c1 = np.copy(gps_list[0].position())[i]
        c2 = np.copy(gps_list[1].position())[i]
        c3 = np.copy(gps_list[2].position())[i]

        r1 = gps_list[0].pseudoranges[i]
        r2 = gps_list[1].pseudoranges[i]
        r3 = gps_list[2].pseudoranges[i]

        positions = trilaterate(c1, c2, c3, r1, r2, r3)

        dist1 = distance_to_origin(positions[0])
        dist2 = distance_to_origin(positions[1])

        if dist1 <= dist2:
            tris.append(positions[0])
        else:
            tris.append(positions[1])

    return tris

def spherical_coordinates(array):
    r = np.linalg.norm(array)

    theta = np.arctan(array[1] / array[0])                                   # * 360 / (2 * np.pi)
    phi = np.arctan(np.sqrt(array[0] ** 2 + array[1] ** 2) / array[2])       # * 360 / (2 * np.pi)

    # in degrees
    return (r, theta, phi)

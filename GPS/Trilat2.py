import numpy as np
from Satellites import *

# trilateration based on 
def trilat(gps_list: list[GPSSatellite]):

    # create list of all times
    all_times = []

    for i in range(0, len(gps_list)):
        all_times.extend(gps_list[i].times_of_pseudoranges)

    all_times = np.unique(all_times)

    # Choose first at least 3 satellites at same time
    for i in range(0, len(all_times)):
        centers = []
        radii = []

        for j in range(0, len(gps_list)):

            index = np.where(gps_list[j].times_of_pseudoranges == all_times[i])

            if index[0].size != 0:
                centers.append(np.copy(gps_list[j].position_ecef()[index])[0])
                radii.append(gps_list[j].pseudoranges[index][0])

            if len(centers) == 3:
                m = max(np.max(centers).any(), max(radii))

                print(f"centers: \n{centers / m}\n")
                print(f"radii  : \n{radii / m}\n")
                print(f"ToP    : {gps_list[j].times_of_pseudoranges[index]}")
                print(f"scale f: {m}")
                exit(1)

from Parsing import *
from Plotting import *
from os import path
from Trilat2 import *

def run():
    # Path to RTCM data 
    data_path = path.join("Data", "rtcmdata.log")

    # Reads and parses RTCM data
    (messages1002, messages1019) = parse_data(data_path)

    gps_list = sort_gps(messages1002, messages1019)

    # trilat(gps_list)

    plot_pseudoranges([gps_list[4]])
    plot_orbits_eci([gps_list[4]])
    plot_orbits_ecef([gps_list[4]])
    plot_eci_and_ecef(gps_list[4])

if __name__ == "__main__":
    run()

from RTCM import *
from Parsing import *
from Plotting import *

def run():
    # Path to RTCM data 
    data_path = r"Data\rtcmdata.log"

    # Reads and parses RTCM data
    (messages1002, messages1019) = parse_data(data_path)

    gps_list = sort_gps(messages1002, messages1019)

    # plot_pseudoranges(gps_list)

    plot_orbit(gps_list[4])
    # plot_orbit(gps_list[5])
    # plot_orbit(gps_list[6])
    plot_orbits(gps_list)

if __name__ == "__main__":
    run()

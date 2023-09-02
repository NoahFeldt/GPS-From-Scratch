import os

from parsing import *
from plotting import *

def run():
    # Create data directory
    data_path = "data"

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    # List RTCM files in data directory
    data_files = os.listdir("data")

    # Draw plots for every RTCM file
    for file_name in data_files:
        print(f"Processing file: \"{file_name}\"")

        # Path to RTCM data
        data_path = os.path.join("data", file_name)

        # Reads and parses RTCM data
        (messages1002, messages1019) = parse_data(data_path)

        gps_list = sort_gps(messages1002, messages1019)

        plot_everything(gps_list, file_name)

if __name__ == "__main__":
    run()

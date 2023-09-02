import os

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl

from satellites import *
from estimation import *
from spheres import *

# disables offsets in matplotlib
mpl.rcParams['axes.formatter.useoffset'] = False

# sets matplotlib theme
plt.style.use("Solarize_Light2")

# Function to save plots in plots folder
def save_plot(plot_file_name, file_name):
    print(f"Saving plot \"{plot_file_name}\"...")

    # Create folder for plots
    plot_folder_path = "plots"

    if not os.path.exists(plot_folder_path):
        os.mkdir(plot_folder_path)

    save_path = os.path.join(plot_folder_path, file_name)

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # Save plot
    plot_path = os.path.join(save_path, plot_file_name)

    plt.savefig(plot_path, dpi=600)

    plt.close()

# Plots pseudoranges of satellites
def plot_pseudoranges(gps_list: list[GPSSatellite], file_name):
    fig = plt.figure()
    
    ax = plt.axes()
    ax.ticklabel_format(style='plain')

    plt.title("Pseudorange measurements")
    
    plt.xlabel("Time of week (s)")
    plt.ylabel("Pseudorange (km)")

    for sat in gps_list:
        plt.scatter(sat.times_of_pseudoranges, np.array(sat.pseudoranges) / 1000, s=1)

    plot_file_name = "pseudoranges.png"
    save_plot(plot_file_name, file_name)

# Plots the satellite positions in the Earth Centered Inertial (ECI) reference frame
def plot_satellite_positions_eci(gps_list: list[GPSSatellite], file_name):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.ticklabel_format(style='plain')

    plt.title("Satellite positions at measurement in ECI frame")

    ax.set_xlabel("X (km)")
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')

    for i in range(0, len(gps_list)):
        eci = gps_list[i].position_eci() / 1000

        ax.scatter(eci[:, 0], eci[:, 1], eci[:, 2], s = 1)

    plot_file_name = "satellite_positions_eci.png"
    save_plot(plot_file_name, file_name)

# Plots the satellite positions in the Earth Centered Earth Fixed (ECEF) reference frame
def plot_satellite_positions_ecef(gps_list: list[GPSSatellite], file_name):
    fig = plt.figure()

    ax = fig.add_subplot(projection='3d')
    ax.ticklabel_format(style='plain')

    plt.title("Satellite positions at measurement in ECEF frame")

    ax.set_xlabel("X (km)")
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')

    for i in range(0, len(gps_list)):
        eci = gps_list[i].position_ecef() / 1000

        ax.scatter(eci[:, 0], eci[:, 1], eci[:, 2], s=1)

    plot_file_name = "satellite_positions_ecef.png"
    save_plot(plot_file_name, file_name)

# Plots the users position in the ECEF frames
def plot_position_ecef(gps_list: list[GPSSatellite], file_name):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.ticklabel_format(style='plain')

    plt.title("User positions in ECEF frame")

    ax.set_xlabel("X (km)")
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')

    estimated_positions = estimate_positions(gps_list)

    ax.scatter(estimated_positions[:, 0] / 1000, estimated_positions[:, 1] / 1000, estimated_positions[:, 2] / 1000)

    plot_file_name = "position_ecef.png"
    save_plot(plot_file_name, file_name)

# Plots satellite orbits in the ECI frame
def plot_orbits_eci(gps_list: list[GPSSatellite], file_name):
    step_size = 0.01

    mean_anomalies = np.arange(0, 2 * np.pi + step_size, step_size)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.ticklabel_format(style='plain')

    plt.title("Satellite orbits in ECI frame")

    ax.set_xlabel("X (km)")
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')

    for i in range(0, len(gps_list)):
        pqw = gps_list[i].perifocal_reference_coordinates(mean_anomalies) / 1000

        eci = gps_list[i].earth_centered_initial(pqw)

        ax.plot(np.copy(eci[:, 0]), np.copy(eci[:, 1]), np.copy(eci[:, 2]), linewidth=1)

    plot_file_name = "orbits_eci.png"
    save_plot(plot_file_name, file_name)

# Plots the users spherical coordinates on a map
def plot_positions_map(gps_list: list[GPSSatellite], file_name):
    fig = plt.figure()

    m = Basemap(projection='cyl', resolution='l', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)

    plt.title("User spherical coordinates on map")

    m.drawcoastlines(linewidth=0.25)
    m.drawcountries(linewidth=0.25)
    m.fillcontinents(color='green', lake_color='aqua')
    m.drawmapboundary(fill_color='aqua')

    estimated_positions = estimate_positions(gps_list)
    cords = spherical_geo(estimated_positions)
    x, y = m(cords[:, 0], cords[:, 1])

    m.scatter(x, y, marker='o', color='red', s=1)

    plot_file_name = "positions_map.png"
    save_plot(plot_file_name, file_name)

# Plots user estimated user coordinates for each measurement in the ECEF frame
def plot_coordinates_ecef(gps_list: list[GPSSatellite], file_name):
    fig = plt.figure()

    ax = fig.add_subplot()
    ax.ticklabel_format(style='plain')

    plt.title("User ECEF coordinates")

    ax.set_xlabel('Time of week (s)')
    ax.set_ylabel("Coordinates (km)")

    estimated_positions = estimate_positions(gps_list)

    all_times = pseudorange_times(gps_list)

    plt.scatter(x=all_times, y=estimated_positions[:, 0] / 1000, s=1)
    plt.scatter(x=all_times, y=estimated_positions[:, 1] / 1000, s=1)
    plt.scatter(x=all_times, y=estimated_positions[:, 2] / 1000, s=1)

    ax.legend(('x', 'y', 'z'), loc='upper right')

    plot_file_name = "coordinates_ecef.png"
    save_plot(plot_file_name, file_name)

# Tries to saves one of every plot for each rtcm file
def plot_everything(gps_list: list[GPSSatellite], file_name):
    try:
        plot_pseudoranges(gps_list, file_name)
    except:
        print(f"Could not draw plot for file: \"{file_name}\"")

    try:
        plot_satellite_positions_eci(gps_list, file_name)
    except:
        print(f"Could not draw plot for file: \"{file_name}\"")

    try:
        plot_satellite_positions_ecef(gps_list, file_name)
    except:
        print(f"Could not draw plot for file: \"{file_name}\"")

    try:
        plot_orbits_eci(gps_list, file_name)
    except:
        print(f"Could not draw plot for file: \"{file_name}\"")

    try:
        plot_coordinates_ecef(gps_list, file_name)
    except:
        print(f"Could not draw plot for file: \"{file_name}\"")

    try:
        plot_position_ecef(gps_list, file_name)
    except:
        print(f"Could not draw plot for file: \"{file_name}\"")

    try:
        plot_positions_map(gps_list, file_name)
    except:
        print(f"Could not draw plot for file: \"{file_name}\"")

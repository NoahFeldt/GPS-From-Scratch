import matplotlib.pyplot as plt
import numpy as np

from Satellites import *

def plot_pseudorange(sat: GPSSatellite):
    plt.style.use("Solarize_Light2")
    plt.style.library
    ax = plt.axes()

    plt.xlabel("Time of week (s)")
    plt.ylabel("Pseudorange (km)")

    ax.ticklabel_format(style='plain')

    plt.scatter(sat.times_of_pseudoranges, np.array(sat.pseudoranges) / 1000)

    plt.show()

def plot_pseudoranges(sats: list[GPSSatellite]):
    plt.style.use("Solarize_Light2")

    ax = plt.axes()

    plt.xlabel("Time of week (s)")
    plt.ylabel("Pseudorange (km)")

    ax.ticklabel_format(style='plain')

    for sat in sats:
        plt.scatter(sat.times_of_pseudoranges, np.array(sat.pseudoranges) / 1000)

    plt.show()

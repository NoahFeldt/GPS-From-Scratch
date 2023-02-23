import matplotlib.pyplot as plt
import numpy as np

from Satellites import *

plt.style.use("Solarize_Light2")

def plot_pseudorange(sat: GPSSatellite):
    ax = plt.axes()

    plt.xlabel("Time of week (s)")
    plt.ylabel("Pseudorange (km)")

    ax.ticklabel_format(style='plain')

    plt.scatter(sat.times_of_pseudoranges, np.array(sat.pseudoranges) / 1000)

    plt.show()

def plot_pseudoranges(sats: list[GPSSatellite]):
    ax = plt.axes()

    plt.xlabel("Time of week (s)")
    plt.ylabel("Pseudorange (km)")

    ax.ticklabel_format(style='plain')

    for sat in sats:
        plt.scatter(sat.times_of_pseudoranges, np.array(sat.pseudoranges) / 1000)

    plt.show()

def plot_orbit(sats: GPSSatellite):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.ticklabel_format(style='plain')

    ax.set_xlabel("X (km)")
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')

    eci = sats.position() / 1000

    ax.scatter(eci[:, 0], eci[:, 1], eci[:, 2])

    plt.show()

def plot_orbits(sats: list[GPSSatellite]):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.ticklabel_format(style='plain')

    ax.set_xlabel("X (km)")
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')

    for i in range(0, len(sats)):
        eci = sats[i].position_ecef() / 1000
        
        ax.scatter(eci[:, 0], eci[:, 1], eci[:, 2])

    plt.show()

def plot_tris(tris):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.ticklabel_format(style='plain')

    ax.set_xlabel("X (km)")
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')

    tris = np.array(tris) / 1000

    ax.scatter(tris[:, 0], tris[:, 1], tris[:, 2])

    plt.show()

def plot_eci_and_ecef(sat: GPSSatellite):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.ticklabel_format(style='plain')

    ax.set_xlabel("X (km)")
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')

    eci = sat.position_eci() / 1000
    ecef = sat.position_ecef() / 1000

    ax.scatter(eci[:, 0], eci[:, 1], eci[:, 2])
    ax.scatter(ecef[:, 0], ecef[:, 1], ecef[:, 2])

    plt.show()
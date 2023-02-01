import math
import numpy as np

from RTCM import *

earth_mass = 5.9722 * 10 ** 24
gravitational_constant = 6.67430_15 * 10 ** -11

mu = earth_mass * gravitational_constant

# calculates true anomaly of satellite
def true_anomaly(time_difference: float, message: RTCM1019) -> float:
    # calculate mean motion, n (degrees / s)
    mean_motion = math.sqrt(mu / message.semi_major_axis ** 3)

    # calculate new mean anomaly after some time difference
    mean_anomaly = message.mean_anomaly + mean_motion * time_difference

    # true anomaly approximation (https://en.wikipedia.org/wiki/True_anomaly#From_the_eccentric_anomaly)
    true_anomaly = mean_anomaly + (2 * message.eccentricity - 1/4 * message.eccentricity ** 3) * math.sin(mean_anomaly) + 5/4 * message.eccentricity ** 2 * math.sin(2 * mean_anomaly) + 13/12 * message.eccentricity * math.sin(3 * mean_anomaly)

    return true_anomaly

# calculates satellite position coordinates in the perifocal reference system
def perifocal_reference_coordinates(nu: float, message: RTCM1019) -> np.ndarray:
    semi_minor_axis = message.semi_major_axis * math.sqrt(1 - message.eccentricity ** 2)

    # calculate coordinates on ellipse
    p = message.semi_major_axis * math.cos(nu)
    q = semi_minor_axis * math.sin(nu)
    w = 0

    # PQW coordinates
    pqw = np.array([p, q, w])

    return pqw

# converts the perifocal reference coordinates to earth centered inertial coordinates
def earth_centered_initial(pqw: np.ndarray, message: RTCM1019) -> np.ndarray:
    # first rotation matrix around z-axis
    Rz = np.matrix([
        [math.cos(-message.longitude_of_ascending_node), -math.sin(-message.longitude_of_ascending_node), 0],
        [math.sin(-message.longitude_of_ascending_node), math.cos(-message.longitude_of_ascending_node), 0],
        [0, 0, 1]
    ])

    # perform first rotation
    pqw_r1 = np.matmul(pqw, Rz)

    # second rotation matrix around x-axis
    Rx = np.matrix([
        [1, 0, 0],
        [0, math.cos(-message.inclination), -math.sin(-message.inclination)],
        [0, math.sin(-message.inclination), math.cos(-message.inclination)]
    ])

    # perform second rotation
    pqw_r2 = np.matmul(pqw_r1, Rx)

    # third rotation matrix around z-axis
    Rz = np.matrix([
        [math.cos(-message.argument_of_periapsis), -math.sin(-message.argument_of_periapsis), 0],
        [math.sin(-message.argument_of_periapsis), math.cos(-message.argument_of_periapsis), 0],
        [0, 0, 1]
    ])

    # perform third rotation
    pqw_r3 = np.matmul(pqw_r2, Rz)

    return pqw_r3

# converts the centered inertial coordinates to earth centered earth fixed coordinates
def earth_centered_earth_fixed(eci: np.ndarray, theta: float) -> np.ndarray:
    # rotation matrix from vernal equinox to Greenwich
    Rz = np.matrix([
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ])

    # perform rotation to ecef
    ecef = np.matmul(eci, Rz)

    return ecef

# calculates position of satellite from ephemeris information
def sat_position(message: RTCM1019):
    # time since RTCM1019 message was received (technically since i was sent)
    # 1000 seconds
    time_difference = 1000

    # calculate true anomaly
    nu = true_anomaly(time_difference, message)

    # calculate PQW coordinates
    pqw = perifocal_reference_coordinates(nu, message)

    # calculate ECI coordinates
    eci = earth_centered_initial(pqw, message)

    return eci

    # theta = Greenwich sidereal time (angle)
    # theta = 0

    # calculate ECEF coordinates
    # ecef = earth_centered_initial(pqw, message)
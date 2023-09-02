import numpy as np
from constants import *

# Class containing information collected from a specific GPS satellite
class GPSSatellite:
    # Constructor
    def __init__(self, sv, pseudoranges, times_of_pseudoranges, eccentricities, inclinations, mean_anomalies, semi_major_axes, right_ascension_of_ascending_node, arguments_of_periapsis, times_of_ephemeris) -> None:
        # Identification number of satellite
        self.sv: int = sv

        # Distances to receiver (meters)
        self.pseudoranges: np.ndarray = np.array(pseudoranges)

        # Time of pseudorange measurements
        self.times_of_pseudoranges: np.ndarray = np.array(times_of_pseudoranges)

        # Eccentricity of satellite orbit
        self.eccentricities: np.ndarray = np.array(eccentricities)

        # Inclination
        self.inclinations: np.ndarray = np.array(inclinations)

        # Mean anomaly
        self.mean_anomalies: np.ndarray = np.array(mean_anomalies)

        # Semi major axis
        self.semi_major_axes: np.ndarray = np.array(semi_major_axes)

        # Right ascension of ascending nodes
        self.right_ascension_of_ascending_node: np.ndarray = np.array(right_ascension_of_ascending_node)

        # Argument of peripsis
        self.arguments_of_periapsis: np.ndarray = np.array(arguments_of_periapsis)

        # Time of ephemeris measurement
        self.times_of_ephemeris: np.ndarray = np.array(times_of_ephemeris)

    # Calculates true anomaly of satellite
    def true_anomaly(self, time_differences: np.ndarray) -> np.ndarray:
        # calculate mean motion, n (degrees / s)
        mean_motion = np.sqrt(MU / self.semi_major_axes[0] ** 3)

        # calculate new mean anomaly after some time difference
        mean_anomaly = self.mean_anomalies[0] + mean_motion * time_differences

        # true anomaly approximation (https://en.wikipedia.org/wiki/True_anomaly#From_the_eccentric_anomaly)
        true_anomaly = mean_anomaly + (2 * self.eccentricities[0] - 1/4 * self.eccentricities[0] ** 3) * np.sin(mean_anomaly) + 5/4 * self.eccentricities[0] ** 2 * np.sin(2 * mean_anomaly) + 13/12 * self.eccentricities[0] * np.sin(3 * mean_anomaly)

        return true_anomaly

    # Calculates satellite position coordinates in the perifocal reference system
    def perifocal_reference_coordinates(self, true_anomalies: np.ndarray) -> np.ndarray:
        # distance from focal point to satellite
        radius = (self.semi_major_axes[0] * (1 - self.eccentricities[0] ** 2)) / (1 + self.eccentricities[0] * np.cos(true_anomalies))

        # calculate coordinates on ellipse
        p = radius * np.cos(true_anomalies)
        q = radius * np.sin(true_anomalies)
        w = np.zeros(p.shape)

        # PQW coordinates
        pqw = np.dstack([p, q, w])[0]

        return pqw

    # Converts the perifocal reference coordinates to earth centered inertial coordinates
    def earth_centered_initial(self, pqw: np.ndarray) -> np.ndarray:
        # first rotation matrix around z-axis
        Rz = np.matrix([
            [np.cos(-self.arguments_of_periapsis[0]), -np.sin(-self.arguments_of_periapsis[0]), 0],
            [np.sin(-self.arguments_of_periapsis[0]), np.cos(-self.arguments_of_periapsis[0]), 0],
            [0, 0, 1]
        ])

        # perform first rotation
        pqw_r1 = np.matmul(pqw, Rz)

        # second rotation matrix around x-axis
        Rx = np.matrix([
            [1, 0, 0],
            [0, np.cos(-self.inclinations[0]), -np.sin(-self.inclinations[0])],
            [0, np.sin(-self.inclinations[0]), np.cos(-self.inclinations[0])]
        ])

        # perform second rotation
        pqw_r2 = np.matmul(pqw_r1, Rx)

        # third rotation matrix around z-axis
        Rz = np.matrix([
            [np.cos(-self.right_ascension_of_ascending_node[0]), -np.sin(-self.right_ascension_of_ascending_node[0]), 0],
            [np.sin(-self.right_ascension_of_ascending_node[0]), np.cos(-self.right_ascension_of_ascending_node[0]), 0],
            [0, 0, 1]
        ])

        # perform third rotation
        pqw_r3 = np.matmul(pqw_r2, Rz)

        return pqw_r3

    # Converts the centered inertial coordinates to earth centered earth fixed coordinates
    def earth_centered_earth_fixed(self, eci: np.ndarray) -> np.ndarray:
        ecefs = []

        for i in range(0, len(self.times_of_pseudoranges)):
            # calculates angle based on soloar day (not sidirial day) 
            # needs to be fixed in the future
            theta = self.times_of_pseudoranges[i] / 86400 % 1 * 2 * np.pi

            Rz = np.matrix([
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
            ])

            # perform rotation to ecef
            ecef = np.matmul(eci[i], Rz)

            ecefs.append(np.copy(ecef)[0])

        ecefs = np.array(ecefs)

        return ecefs

    # Calculate satellite ECEF position for every pseudorange measurement
    def position_ecef(self):
        eci = self.position_eci()

        ecef = self.earth_centered_earth_fixed(eci)

        return ecef

    # Calculate ECI position
    def position_eci(self):
        time_differences = self.times_of_pseudoranges - self.times_of_ephemeris[0]

        true_anomalies = self.true_anomaly(time_differences)

        pqw = self.perifocal_reference_coordinates(true_anomalies)

        eci = self.earth_centered_initial(pqw)

        return eci
import numpy as np

# Calculate geographical spherical coordinates from ECEF coordinates
def spherical_geo(ecef: np.ndarray):
    r = np.sqrt(ecef[:, 0] ** 2 + ecef[:, 1] ** 2 + ecef[:, 2] ** 2)

    theta = np.arctan2(ecef[:, 1], ecef[:, 0])
    phi = np.arccos(ecef[:, 2] / r)

    theta_deg = theta * 360/(2*np.pi)
    phi_deg = 90 - phi * 360/(2*np.pi)

    cords = np.dstack([theta_deg, phi_deg, r])[0]

    return cords

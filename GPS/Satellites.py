# Class containing information collected from a specific GPS satellite
class GPSSatellite:
    def __init__(self, pseudoranges, times_of_pseudoranges, eccentricities, inclinations, mean_anomalies, semi_major_axes, longitudes_of_ascending_node, arguments_of_periapsis, times_of_ephemeris) -> None:
        self.sv: int

        self.pseudoranges: list[float] = pseudoranges
        self.times_of_pseudoranges: list[float] = times_of_pseudoranges

        self.eccentricities: list[float] = eccentricities
        self.inclinations: list[float] = inclinations
        self.mean_anomalies: list[float] = mean_anomalies
        self.semi_major_axes: list[float] = semi_major_axes
        self.longitudes_of_ascending_node: list[float] = longitudes_of_ascending_node
        self.arguments_of_periapsis: list[float] = arguments_of_periapsis
        self.times_of_ephemeris: list[float] = times_of_ephemeris
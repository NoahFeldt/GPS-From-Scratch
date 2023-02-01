import math
from pyrtcm.rtcmmessage import RTCMMessage

class RTCM1002:
    # Constructs a class for a RTCM1002 message
    def __init__(self, message: RTCMMessage) -> None:
        # number of satellites in message
        self.num_satellites: int = message.DF006

        # list of satellite identification numbers
        self.svs = []

        # list of integer ambiguities (dimensionless)
        self.ambiguities = []

        # list of pseudorange reminders (meters)
        self.reminders = []

        # list of calculated pseudoranges (meters)
        self.pseudoranges = []

        # get satellite identification numbers
        for i in range(1, self.num_satellites + 1):
            # generate sv DF attribute
            if i < 10:
                attribute: str = f"DF009_0{i}"
            elif i >= 10:
                attribute: str = f"DF009_{i}"

            # get sv and append to list
            sv = message.__getattribute__(attribute)
            self.svs.append(sv)

        # get pseudorange reminders
        for i in range(1, self.num_satellites + 1):
            # generate pseudorange reminder DF attribute
            if i < 10:
                attribute: str = f"DF011_0{i}"
            elif i >= 10:
                attribute: str = f"DF011_{i}"

            # get pseudorange reminder and append to list
            reminder = message.__getattribute__(attribute)
            self.reminders.append(reminder)

        # get integer ambiguities
        for i in range(1, self.num_satellites + 1):
            # generate integer ambiguity DF attribute
            if i < 10:
                attribute: str = f"DF014_0{i}"
            elif i >= 10:
                attribute: str = f"DF014_{i}"

            # get integer ambiguity and append to list
            ambiguity = message.__getattribute__(attribute)
            self.ambiguities.append(ambiguity)

        # calculate pseudoranges from ambiguities and reminders
        for i in range(0, self.num_satellites + 0):
            # calculate pseudorange for satellite
            pseudorange = self.ambiguities[i] * 299792.458 + self.reminders[i]

            # add pseudorange to list
            self.pseudoranges.append(pseudorange)

    # print values of message
    def print_values(self):
        print(f"num_sat: {self.num_satellites}")
        print(f"svs: {self.svs}")
        print(f"rem: {self.reminders}")
        print(f"amb: {self.ambiguities}")
        print(f"prs: {self.pseudoranges}")

class RTCM1006:
    def __init__(self, message: RTCMMessage) -> None:
        pass

class RTCM1013:
    def __init__(self, message: RTCMMessage) -> None:
        pass

class RTCM1019:
    # Constructs a class for a RTCM1019 message
    def __init__(self, message: RTCMMessage) -> None:
        # Satellite identification number
        self.sv: int = message.DF009

        # Eccentricity (dimensionless)
        self.eccentricity: float = message.DF090 * 2 ** -33

        # Inclination (radians)
        self.inclination: float = message.DF097 * math.pi

        # Mean anomaly (radians)
        self.mean_anomaly: float = message.DF088 * math.pi

        # Semi major axis (meters)
        self.semi_major_axis: float = message.DF092 ** 2

        # Longitude of Ascending Node (radians)
        self.longitude_of_ascending_node: float = message.DF095 * math.pi

        # Argument of periapsis (radians)
        self.argument_of_periapsis: float = message.DF099 * math.pi

    # prints values of the message for debugging purposes
    def print_values(self) -> None:
        print(f"sv: {self.sv}")
        print(f"e: {self.eccentricity}")
        print(f"i: {self.inclination}")
        print(f"M: {self.mean_anomaly}")
        print(f"a: {self.semi_major_axis}")
        print(f"OMEGA: {self.longitude_of_ascending_node}")
        print(f"omega: {self.argument_of_periapsis}")

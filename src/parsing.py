from pyrtcm import RTCMReader

from rtcm import *
from satellites import *

# Function to parse RTCM data and return lists of RTCM messages
def parse_data(data_path: str) -> tuple[list[RTCM1002], list[RTCM1019]]:
    print("Parsing RTCM data...")

    # lists to contain parsed messages
    messages1002: list[RTCM1002] = []
    messages1019: list[RTCM1019] = []

    # read RTCM data stream from file
    stream = open(data_path, "rb")

    # create reader
    rtr = RTCMReader(stream)

    # parse messages
    for (raw_data, parsed_data) in rtr:
        if parsed_data.identity == "1002":
            message = RTCM1002(parsed_data)
            messages1002.append(message)
        elif parsed_data.identity == "1019":
            message = RTCM1019(parsed_data)
            messages1019.append(message)

    return (messages1002, messages1019)

# Returns time of the first rtcm 1019 message of the week
def get_basis_time(times_of_ephemeris) -> float:
    first = times_of_ephemeris[0][0]
    # index = 1

    for i in range(1, len(times_of_ephemeris)):
        if times_of_ephemeris[i][0] < first:
            first = times_of_ephemeris[i][0]
            # index = i

    return first

# Sorts GPS message data into GPS class objects
def sort_gps(messages1002: list[RTCM1002], messages1019: list[RTCM1019]) -> list[GPSSatellite]:
    print("Sorting GPS satellites...")

    # create a list of all GSP SVs from which we have received a RTCM1019 message
    all_svs: list[int] = []

    for i in range(0, len(messages1019)):
        if all_svs.count(messages1019[i].sv) == 0:
            all_svs.append(messages1019[i].sv)

    # sorts list of SVs
    all_svs.sort()

    # RTCM 1019 values
    svs: list[list[int]] = []

    eccentricities: list[list[float]] = []
    inclinations: list[list[float]] = []
    mean_anomalies: list[list[float]] = []
    semi_major_axes: list[list[float]] = []
    right_ascension_of_ascending_node: list[list[float]] = []
    arguments_of_periapsis: list[list[float]] = []
    times_of_ephemeris: list[list[float]] = []

    for i in range(0, len(all_svs)):
        eccentricities.append([])
        inclinations.append([])
        mean_anomalies.append([])
        semi_major_axes.append([])
        right_ascension_of_ascending_node.append([])
        arguments_of_periapsis.append([])
        times_of_ephemeris.append([])

    for i in range(0, len(messages1019)):
        index: int = all_svs.index(messages1019[i].sv)

        # removes duplicate RTCM 1019 messages
        if times_of_ephemeris[index].count(messages1019[i].time_of_week) < 1:
            eccentricities[index].append(messages1019[i].eccentricity)
            inclinations[index].append(messages1019[i].inclination)
            mean_anomalies[index].append(messages1019[i].mean_anomaly)
            semi_major_axes[index].append(messages1019[i].semi_major_axis)
            right_ascension_of_ascending_node[index].append(messages1019[i].right_ascension_of_ascending_node)
            arguments_of_periapsis[index].append(messages1019[i].argument_of_periapsis)
            times_of_ephemeris[index].append(messages1019[i].time_of_week)

    # RTCM 1002 values
    pseudoranges: list[list[float]] = []
    times_of_pseudoranges: list[list[float]] = []

    for i in range(0, len(all_svs)):
        pseudoranges.append([])
        times_of_pseudoranges.append([])

    for i in range(0, len(messages1002)):
        for j in range(0, len(messages1002[i].svs)):
            if all_svs.count(messages1002[i].svs[j]) > 0:
                index: int = all_svs.index(messages1002[i].svs[j])

                pseudoranges[index].append(messages1002[i].pseudoranges[j])
                times_of_pseudoranges[index].append(messages1002[i].time_of_week)

    # create list og GPSSatellite objects
    gps_list: list[GPSSatellite] = []

    for i in range(0, len(all_svs)):
        gps = GPSSatellite(all_svs[i], pseudoranges[i], times_of_pseudoranges[i], eccentricities[i], inclinations[i], mean_anomalies[i], semi_major_axes[i], right_ascension_of_ascending_node[i], arguments_of_periapsis[i], times_of_ephemeris[i])

        gps_list.append(gps)

    return gps_list

from pyrtcm import RTCMReader

from RTCM import *
from Orbits import *

def run():
    # read RTCM data stream from file
    stream = open(r'Data\rtcmdata.log', 'rb')

    # create reader
    rtr = RTCMReader(stream)

    # parse messages
    for (raw_data, parsed_data) in rtr:
        
        if parsed_data.identity == "1002":
            message = RTCM1002(parsed_data)
            # message.print_values()

        elif parsed_data.identity == "1019":
            message = RTCM1019(parsed_data)
            # message.print_values()

            # pos = sat_position(message)
            # print(pos)
            # input()

if __name__ == "__main__":
    run()

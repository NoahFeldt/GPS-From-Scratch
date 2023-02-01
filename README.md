# GPS

A project that aims to implement satellite navigation from scratch. 

## Prerequisites

The scripts in this project depend on the [pyrtcm](https://github.com/semuconsulting/pyrtcm) library for parsing the RTCM3 messages.

The pyrtcm package can be installed with:

```bash
pip install pyrtcm
```

The project also depends on the [numpy](https://github.com/numpy/numpy) library for vector and matrix operations.

The numpy package can be installed with:

```bash
pip install numpy
```

## Explanation

### GPS signals

This project uses the [RTCM3 protocol](https://en.wikipedia.org/wiki/RTCM_SC-104) to encode the raw GPS-data sent by the GPS system in messages 1002 and 1019.

Message 1002 contains information about the [pseudorange](https://en.wikipedia.org/wiki/Pseudorange), which is the approximate distance from the receiver to the satellites.

Message 1019 contains information about the orbit of the satellites, including the [Keplerian elements](https://en.wikipedia.org/wiki/Orbital_elements#Keplerian_elements), which can be used to calculate the position of the satellite at a given time.


# Smart Air Conditioning using machine learning

(Hey Elon - heard you want to do something similar - would be great if this code can help :)

System that learns how often a room is occupied based on time, movement, air conditioning preferences and learns on historic data. This can have a significant impact on the energy use around a house/building. 

This sytem can learn based on the following habits
* how often a room is occupied - based on PIR data
* hat time of day is the air conditioning demanded by residents
* which months, days are most demanding in terms of air conditioning
* difference between outside temperature and humidity (acquired through open weather) to inside temperature and humidity

This means if somone switches on the air conditioning everday at the same time then after a while the system will automatically start to switch on the AC wihtout any manual intervention.


# Quick Start
|Document|Summary|Link|
|--|--|--|
|Introductory post  | Discusses the idea behind the system  | [Blog Post](https://faisalajmals.wordpress.com/) |
|Quick Start| Minimal setup that walks through getting software aspect of the system up and running quickly | [Wiki](https://github.com/faisalthaheem/machine-learnt-air-conditioning/wiki/Quick-Start) |
|Hardware Setup| Brief introduction to assembling the hardware sensors| [Hardware Sensors](https://github.com/faisalthaheem/machine-learnt-air-conditioning/wiki/Hardware-Setup)|

# Brief Introduction

There are 3 hardware components developed using esp8266 modules, which are

 1. An IR Blaster which relays smart phone app commands to the air
    conditioning thereby allowing the system to learn about the desired
    temperature at any given instance. The blaster uses reversed
    engineered IR codes for a SHARP ac. 
2. A PIR Sensor which senses movement in the area and reports it to the node red app.
3. A DHT-22 sensor which monitors the temperature and humidity in the room, this
    information is used in the machine learning phase.

The following diagrams show the high level system services, which are packaged as docker containers for ease of deployment.
![System Block Diagram](https://cdn.rawgit.com/faisalthaheem/machine-learnt-air-conditioning/c8fef40f/docs/block-diagram.png)

![Services Diagram](https://cdn.rawgit.com/faisalthaheem/machine-learnt-air-conditioning/c8fef40f/docs/services-diagram.png)


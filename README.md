# Usage

external_components:
  - source: https://github.com/rafal83/zmpt101b
    components: [zmpt101b]

sensor:
  - platform: zmpt101b
    name: "Voltage"
    id: voltage
    pin: A0
    frequency: 50
    sensitivity: 941.25
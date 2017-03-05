#!/bin/bash

./rpi_cam_to_stream.py | avconv -f image2pipe -c:v mjpeg -i - -r 15 -map 0 -f mjpeg -an - | streameye

#!/bin/sh -e
#
# 

/sbin/iptables -t mangle -I POSTROUTING 1 -o wlan0 -p udp --dport 123 -j TOS --set-tos 0x00

#this rule let me configure LKV373 interface via wlan remote interface
sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j DNAT --to-destination 192.168.0.2

# This one is for testing
#gst-launch-1.0 -v udpsrc ! decodebin ! omxh264enc target-bitrate=5000000 control-rate=variable ! h264parse ! 'video/x-h264,level=(string)'4.1',profile='main ! queue ! mux. audiotestsrc is$

# This one takes the UDP stream from an LKV373 video HDMI extender and put into a UDP rdp host port 5000 
gst-launch-1.0 udpsrc uri=udp://192.168.0.254:5004 ! udpsink host=192.168.1.241 port=5000 -vv


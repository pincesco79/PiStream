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

#omxh264enc ! 'video/x-h264, streamformat=(string)byte-stream' ! h264parse ! flvmux streamable=true name=mux 
    gst-launch-1.0 videotestsrc is-live=1 ! videoconvert ! 'video/x-raw, format=(string)I420, width=(int)640, height=(int)480, framerate=25/1' ! queue ! omxh264enc ! 'video/x-h264, streamformat=(string)byte-stream' ! h264parse ! flvmux streamable=true name=mux ! rtmpsink location="rtmp://a.rtmp.youtube.com/live2/xxxx-xxxx-xxxx-xxxx" audiotestsrc ! voaacenc bitrate=128000 ! mux.
    gst-launch-1.0 videotestsrc is-live=1 ! videoconvert ! 'video/x-raw, format=(string)I420, width=(int)640, height=(int)480, framerate=25/1' ! queue ! omxh264enc ! 'video/x-h264, streamformat=(string)byte-stream' ! h264parse ! flvmux streamable=true name=mux ! rtmpsink location="rtmp://a.rtmp.youtube.com/live2/gssy-a5pt-j2gr-4v1e" audiotestsrc ! voaacenc bitrate=128000 ! mux.


WARNING: erroneous pipeline: could not link omxh264enc-omxh264enc0 to rtmpsink0
pi@raspberrypi:~ $ gst-launch-1.0 udpsrc uri=udp://192.168.0.254:5004 ! tsdemux ! h264parse ! omxh264dec ! omxh264enc ! rtmpsink location="rtmp://a.rtmp.youtube.com/live2/gssy-a5pt-j2gr-4v1e"

# this one is VIDEOTESTSRC and works with Microsoft STREAM
gst-launch-1.0 videotestsrc ! videoconvert ! 'video/x-raw, width=(int)1280, height=(int)720, framerate=30/1' ! queue ! omxh264enc ! h264parse ! flvmux streamable=true name=mux ! rtmpsink location="rtmp://tcmkcxmdcscpefogo2wc7hjaxa-fa5udrtaio2oezgkopoijthxdd-euwe.channel.media.azure.net:1935/live/f8e8bd1405ed4f48baf242519c65939a/123456" audiotestsrc ! voaacenc bitrate=128000 ! mux.



# from the lkv373 webpage
gst-launch-1.0 -v udpsrc multicast-iface=”eth0″ multicast-group=239.255.42.42 auto-multicast=true port=5004 caps=”video/mpegts, media=(string)video” ! tsdemux ! decodebin ! videoconvert ! autovideosink sync=false
gst-launch-1.0 udpsrc uri=udp://192.168.0.254:5004 caps=”video/mpegts, media=(string)video” ! tsparse ! decodebin name=dec ! queue ! videoconvert ! autovideosink sync=false dec. ! queue ! audioconvert ! autoaudiosink sync=false

WARNING: from element /GstPipeline:pipeline0/GstAutoVideoSink:autovideosink0: Could not initialise Xv output
Additional debug info:
xvimagesink.c(1760): gst_xv_image_sink_open (): /GstXvImageSink:autovideosink0-actual-sink-xvimage:
Could not open display (null)
Setting pipeline to PLAYING ...
New clock: GstSystemClock

# OK FOR ASCII OUTPUT ... DON'T KNOW FOR ALSA .. BUT OK QUEUE
gst-launch-1.0 udpsrc uri=udp://192.168.0.254:5004 caps="video/mpegts, media=(string)video" ! tsparse ! decodebin name=dec ! queue ! videoconvert ! cacasink dec. ! queue ! audioconvert ! alsasink
 gst-launch-1.0 udpsrc uri=udp://192.168.0.254:5004 caps="video/mpegts, media=(string)video" ! tsparse ! decodebin name=dec ! queue ! videoconvert ! VVVVVVVVVVV ! queue ! audioconvert ! AAAAAAAAAAAA
 
 # trying this one
 gst-launch-1.0 udpsrc uri=udp://192.168.0.254:5004 caps="video/mpegts, media=(string)video" ! tsdemux ! 'video/x-h264' !  h264parse ! omxh264dec ! omxh264enc ! flvmux ! rtmpsink location="rtmp://a.rtmp.youtube.com/live2/gssy-a5pt-j2gr-4v1e"

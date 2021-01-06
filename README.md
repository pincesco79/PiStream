# PiStream
This is to show how to stream to an rtmp server like Microsoft Stream with ffmpeg on a Raspberry Pi 3b+ with any HDMI out equipped camera.
Since I  didn't want to buy a HDMI capture card, I ricycled a cheap LKV373a extender TX. I found that someone did it before me, with different goal. It's all described by danman here https://blog.danman.eu/new-version-of-lenkeng-hdmi-over-ip-extender-lkv373a/ 
Extender TX is capable to send a udp encapsulated flv h264 stream on LAN, so my goal is to send this stream on a rtmp nginx local server running on a raspberry Pi.
Nginx server must be compiled with rtmp module!

# New on January 6th, 2021
Added real interface: LCD 16x2, pushbutton and one LED

Support code based on python, ffmpeg-python bindings by kkroening ffmpeg-python https://github.com/kkroening/ffmpeg-python.
Now I can start/stop the streaming pushing a button and I can see the status on the LCD 16x2 and the blinking LED

There's a lot to do. 
- Another button to shutdown the system
- Another button to change the settings (A/V format, rtmp url and others)
...

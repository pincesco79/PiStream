import ffmpeg
import subprocess
import threading 
import time # Import the sleep function from the time module
from time import sleep
import RPi.GPIO as GPIO
import I2C_LCD_driver
import socket
import fcntl
import struct
from gpiozero import LED

video_format = "flv"
server_url = "rtmp://127.0.0.1:1935/live/stream"
btn_pin = 12
streaming = False
stream_stopped = False


class LEDatGPIO():
    def __init__(self,pinnumber):
        self.led = LED(pinnumber)
        self.__loop = True
        self.__threading = threading.Thread(target=self.__blink)

    def on(self,):
        self.__loop = False
        self.maybejoin()
        self.led.on()

    def off(self, ):
        self.__loop = False
        self.maybejoin()
        self.led.off()

    def maybejoin(self,):
        if self.__threading.isAlive():
            self.__threading.join()

    def blink(self, pitch):
        self.__threading = threading.Thread(target=self.__blink, args=(pitch, ))
        self.__threading.start()

    def __blink(self, pitch=.25):
        self.__loop = True
        while self.__loop:
            self.led.toggle()
            time.sleep(pitch/2)
        self.led.off()

class DisplayLCD():
    def __init__(self):
        self.lcd = I2C_LCD_driver.lcd()
        self.__rolling = True
        self.__threading = threading.Thread(target=self.__rolling)
        
    def lcd_display_string(self, text, row):
        self.__rolling = False
        self.maybejoinLCD()
        self.lcd.lcd_display_string(text, row)
               
    #def __lcd_display_string(self, text, row):
    #    self.__rolling = False
    #    self.maybejoinLCD()
    #   self.lcd_display_string = __lcd_display_string
        
    def lcd_clear(self,):
        self.__rolling = False
        self.maybejoinLCD()
        self.lcd.lcd_clear()
        
    def maybejoinLCD(self,):
        if self.__threading.isAlive():
            self.__threading.join() 
            
    def rolling_text(self, text, row):    
        self.__threading = threading.Thread(target=self.__rolling_text, args=(text, row, ))
        self.__threading.start()
        
    def __rolling_text(self, rolling_txt, row):
        self.__rolling = True
        str_pad = " " * 16
        #rolling_txt = text
        rolling_txt = str_pad + rolling_txt
        while self.__rolling:
            for i in range (0, len(rolling_txt)):
                    lcd_text = rolling_txt[i:(i+16)]
                    self.lcd.lcd_display_string(lcd_text,row)
                    sleep(0.1)
                    self.lcd.lcd_display_string(str_pad,row)
        

streamProc = (
    ffmpeg
     .input("udp://192.168.0.254:5004?fifo_size=262144&overrun_nonfatal=1")
     #.drawbox(0,0,0,120,'blue',t=5)
         .output(
             server_url,
                #vcodec = "h264_omx", # use the hardware Rpi encoding
                #video_bitrate=4000,
                #profile="base",
                vcodec = "copy", # use same codecs of the original video
                acodec = "aac",
                audio_bitrate="128k",
                #listen=1, # enables HTTP server
                f=video_format)
            .global_args("-re") # argument to act as a live stream
             #.run_async(pipe_stdout=True)
        .get_args()
    )

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, 
        struct.pack('256s', ifname[:15])
    )[20:24])

def my_callback(btn_pin):
    global streaming
    global process
    global stream_stopped
    # se ho premuto il tasto e mi trovo in streaming, effettuo il toggle sullo stop.....
    
    if streaming is True:
        display.lcd_display_string("                ",2)
        display.lcd_display_string(" Stream stopped ",2)
        #pause(2)
        display.lcd_display_string("Ready  to stream",2)
        
        streamLed.off()
        streaming = False
        
        process.communicate(str.encode("q"))
        #stream_stopped = True
        #display.lcd_clear()
        #display.lcd_display_string("  PI  STREAMER  ", 1)
        
        
        
    # ... altrimenti inizio lo streaming!    
    else:
        streamLed.blink(0.5)
        streaming = True
        process= subprocess.Popen(['ffmpeg']+streamProc, stdin=subprocess.PIPE, stdout=subprocess.PIPE) 
        #display.lcd_display_string("...starting....",2)
        #display.rolling_text("Streaming @ port 1935",2)
        #display.rolling_text("Streaming @ port 1935",2)
        
if __name__ == '__main__':
    # ******** Settings ************************     
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BCM) # Use physical pin numbering
    GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.add_event_detect(btn_pin, GPIO.RISING, callback=my_callback, bouncetime=600)
    display = DisplayLCD()
    streamLed = LEDatGPIO(21)
        
    display.lcd_display_string("  PI  STREAMER  ", 1) 
    display.lcd_display_string("Ready  to stream",2)    
    #display.rolling_text("Streaming @ port 1935",2)
    
    streaming = False
    #stream_stopped = False
    
    if streaming:
        #display.lcd_display_string("                ",2)                 
        display.lcd_display_string("   Streaming    ",2)
        #sleep(2)
        #display.lcd_display_string("                ",2)
        #sleep(1)
        
        try:
            probe = ffmpeg.probe(server_url)
        except ffmpeg._run.Error as e:
            raise SpleeterError(
                'An error occurs with ffprobe (see ffprobe output below)\n\n{}'
                .format(e.stderr.decode()))
        if 'streams' not in probe or len(probe['streams']) == 0:
            raise SpleeterError('No stream was found with ffprobe')

        #probe = ffmpeg.probe(server_url)
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        width = str(int(video_info['width']))
        height = str(int(video_info['height']))
        codec = str(video_info['codec_name'])
        videoinfo = width+"x"+height+" - "+codec
        
        #print videoinfo
        display.lcd_display_string(videoinfo,2)       
        #sleep(2)
      
        #else:
        #    if stream_stopped:
        #        display.lcd_display_string(" Stream Stopped ", 2)
        #        time.sleep(1)
        #        #stream_stopped = False
    else:
        display.lcd_display_string("Ready  to Stream", 2)   
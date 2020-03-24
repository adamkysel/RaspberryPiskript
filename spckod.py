import wiotp.sdk.device
import RPi.GPIO as GPIO
import json
from time import sleep
from datetime import datetime
import Adafruit_DHT
import time
from datetime import datetime
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
GPIO.setmode(GPIO.BCM)
relay_pin = 16
relay_time = 2
#this value affects rotation speed of stepper motor
rotation_speed = 0.001

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create analog pins
chan = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

percentage = 0


#functions
#function for reading commands from IBM IOT platform
def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data["motor1"])
    f = open("motor1.txt", "r")
    state1=f.read()
    print(state1)
    f = open("motor2.txt", "r")
    state2=f.read()
    print(state2)
    f = open("relay.txt", "r")
    state3=f.read()
    print(state3) 
    if cmd.data["motor1"] != state1:
        if cmd.data["motor1"]=="open":
            f = open("motor1.txt", "w")
            f.write("open")
            f.close()
            rotate(100, 27, 17, 22, 18)
        if cmd.data["motor1"]=="close":
            f = open("motor1.txt", "w")
            f.write("close")
            f.close()
            rotate(-100, 27, 17, 22, 18)
    if cmd.data["motor2"] != state2:
        if cmd.data["motor2"]=="open":
            f = open("motor2.txt", "w")
            f.write("open")
            f.close()
            rotate(100, 13, 6, 5, 12)
        if cmd.data["motor2"]=="close":
            f = open("motor2.txt", "w")
            f.write("close")
            f.close()
            rotate(-100, 13, 6, 5, 12)
    if cmd.data["relay"] != state3:
        f = open("relay.txt", "w")
        f.write(cmd.data["relay"])
        f.close()
        GPIO.setup(relay_pin,GPIO.OUT)
        GPIO.output(relay_pin,GPIO.LOW)
        GPIO.output(relay_pin,GPIO.HIGH)
        sleep(relay_time)
        GPIO.output(relay_pin,GPIO.LOW)
        
#function to rotate motor
def rotate(steps, pin1, pin2, pin3, pin4):
    x=steps
    out1 = pin1
    out2 = pin2
    out3 = pin3
    out4 = pin4
    # setup pins for control
    GPIO.setup(out1,GPIO.OUT)
    GPIO.setup(out2,GPIO.OUT)
    GPIO.setup(out3,GPIO.OUT)
    GPIO.setup(out4,GPIO.OUT)

    GPIO.output(out1,GPIO.LOW)
    GPIO.output(out2,GPIO.LOW)
    GPIO.output(out3,GPIO.LOW)
    GPIO.output(out4,GPIO.LOW)
    i=0
    positive=0
    negative=0
    y=0
    if x>0 and x<=400:
          for y in range(x,0,-1):
              if negative==1:
                  if i==7:
                      i=0
                  else:
                      i=i+1
                  y=y+2
                  negative=0
              positive=1
              if i==0:
                  GPIO.output(out1,GPIO.HIGH)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.LOW)
                  time.sleep(rotation_speed)
              elif i==1:
                  GPIO.output(out1,GPIO.HIGH)
                  GPIO.output(out2,GPIO.HIGH)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.LOW)
                  time.sleep(rotation_speed)
              elif i==2:  
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.HIGH)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.LOW)
                  time.sleep(rotation_speed)
              elif i==3:    
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.HIGH)
                  GPIO.output(out3,GPIO.HIGH)
                  GPIO.output(out4,GPIO.LOW)
                  time.sleep(rotation_speed)
              elif i==4:  
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.HIGH)
                  GPIO.output(out4,GPIO.LOW)
                  time.sleep(rotation_speed)
              elif i==5:
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.HIGH)
                  GPIO.output(out4,GPIO.HIGH)
                  time.sleep(rotation_speed)
              elif i==6:    
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.HIGH)
                  time.sleep(rotation_speed)
              elif i==7:    
                  GPIO.output(out1,GPIO.HIGH)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.HIGH)
                  time.sleep(rotation_speed)
              if i==7:
                  i=0
                  continue
              i=i+1
              
    elif x<0 and x>=-400:
          x=x*-1
          for y in range(x,0,-1):
              if positive==1:
                  if i==0:
                      i=7
                  else:
                      i=i-1
                  y=y+3
                  positive=0
              negative=1
              if i==0:
                  GPIO.output(out1,GPIO.HIGH)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.LOW)
                  time.sleep(rotation_speed)
              elif i==1:
                  GPIO.output(out1,GPIO.HIGH)
                  GPIO.output(out2,GPIO.HIGH)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.LOW)
                  time.sleep(rotation_speed)
              elif i==2:  
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.HIGH)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.LOW)
                  time.sleep(rotation_speed)
              elif i==3:    
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.HIGH)
                  GPIO.output(out3,GPIO.HIGH)
                  GPIO.output(out4,GPIO.LOW)
                  time.sleep(rotation_speed)
              elif i==4:  
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.HIGH)
                  GPIO.output(out4,GPIO.LOW)
                  time.sleep(rotation_speed)
              elif i==5:
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.HIGH)
                  GPIO.output(out4,GPIO.HIGH)
                  time.sleep(rotation_speed)
              elif i==6:    
                  GPIO.output(out1,GPIO.LOW)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.HIGH)
                  time.sleep(rotation_speed)
              elif i==7:    
                  GPIO.output(out1,GPIO.HIGH)
                  GPIO.output(out2,GPIO.LOW)
                  GPIO.output(out3,GPIO.LOW)
                  GPIO.output(out4,GPIO.HIGH)
                  time.sleep(rotation_speed)
              if i==0:
                  i=7
                  continue
              i=i-1
              GPIO.output(out1,GPIO.LOW)
              GPIO.output(out2,GPIO.LOW)
              GPIO.output(out3,GPIO.LOW)
              GPIO.output(out4,GPIO.LOW)
#function to get percentage of earth hummidity according to voltage on A/D converter
def get_percentage(vol):
    if vol < 1.47:
        percentage = 100
    elif vol < 1.61:
        percentage = 90
    elif vol < 1.75:
        percentage = 80
    elif vol < 1.89:
        percentage = 70
    elif vol < 2.03:
        percentage = 60
    elif vol < 2.17:
        percentage = 50
    elif vol < 2.31:
        percentage = 40
    elif vol < 2.47:
        percentage = 30
    elif vol < 2.61:
        percentage = 20
    elif vol < 2.8:
        percentage = 10
    elif vol >= 2.8:
        percentage = 0
    return percentage

# Configure
sensor = Adafruit_DHT.DHT11
pin = 10
GPIO.setwarnings(False)
myConfig = wiotp.sdk.device.parseConfigFile("/home/pi/configure.yaml")
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()
while True:

    # get sensor data and prepare them to send to IBM cloud
    hum, temp = Adafruit_DHT.read_retry(sensor, pin)
    vol1 = chan.voltage
    vol2 = chan1.voltage
    vol3 = chan2.voltage
    vol4 = chan3.voltage

    percentage1 = get_percentage(vol1)
    percentage2 = get_percentage(vol2)
    percentage3 = get_percentage(vol3)
    percentage4 = get_percentage(vol4)

    temp1={"te": temp}
    hum1={"hu": hum}
    no=datetime.now()
    now=no.strftime("%d.%m %H:%M")
    print(now)
    #write data to terminal to control if values are ok
    print(percentage1)
    print(percentage2)
    print(percentage3)
    print(percentage4)
    GPIO.setup(relay_pin,GPIO.OUT)
    GPIO.output(relay_pin,GPIO.LOW)
    GPIO.output(relay_pin,GPIO.HIGH)
    sleep(relay_time)
    GPIO.output(relay_pin,GPIO.LOW)

    print(temp)
    print(hum)
    myData = {'datetime':now, 'temperature' : temp, 'humidity' : hum, 'soil1' : percentage1, 'soil2' : percentage2, 'soil3' : percentage3, 'soil4' : percentage4}
    #publish data to IBM cloud
    client.publishEvent(eventId="conditions", msgFormat="json", data=myData, qos=0, onPublish=None)
    #client.publishEvent(eventId="percentage2", msgFormat="json", data=percentage2, qos=0, onPublish=None)
    #client.publishEvent(eventId="percentage3", msgFormat="json", data=percentage3, qos=0, onPublish=None)
    #client.publishEvent(eventId="percentage4", msgFormat="json", data=percentage4, qos=0, onPublish=None)

    #client.publishEvent(eventId="temp", msgFormat="json", data=temp1, qos=0, onPublish=None)
    #client.publishEvent(eventId="hum", msgFormat="json", data=hum1, qos=0, onPublish=None)
    sleep(4)    
    #Read Commands from IBM platform
    client.commandCallback = myCommandCallback

client.loop_forever()
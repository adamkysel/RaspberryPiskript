# import libraries
import wiotp.sdk.device
import RPi.GPIO as GPIO
import json
from time import sleep
from datetime import datetime
import Adafruit_DHT
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Set pinout numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create the I2C bus for ADC convertor
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create analog pins
chan = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

# Def percentage used in soil moisture
percentage = 0

# Configure for DHT sensor
sensor = Adafruit_DHT.DHT22
pin = 27

# Define variables for control green house
rev_door = None
rev_window = None
rev_water = None
openTime1 = ""
closeTime1 = ""
minTemp1 = None
openTime2 = ""
closeTime2 = ""
minTemp2 = None
waterTime = ""
minHum = None
state1 = None
state2 = None
was_water = False

# Connection to IBM watson cloud
myConfig = wiotp.sdk.device.parseConfigFile("/home/pi/configure.yaml")
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

# FUNCTIONS

# Function for reading commands from IBM IOT platform
def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)
    # Do something according commands
    if cmd.data["_id"] == "dowater":
        print("Relay start to water")
        water(20, 23)
        
    print(cmd.data["_id"])
    
    data = cmd.data
    if data["_id"] == "door":
        f = open("motor1.txt", "r")
        state1=f.read()
        print(state1)
        if state1 != data["state"]:
            print("change")
            if data["state"] == "open":
                rotate_servo_motor("clockwise", 2, 17, 18)
                print("open door")
                #rotate_stepper_motor(18, 0.01, 20, 26, 16, 21)
            if data["state"] == "close":
                rotate_servo_motor("anticlockwise", 2, 17, 18)
                print("close door")
                #rotate_stepper_motor(-18, 0.01, 20, 26, 16, 21)
        openTime1 = data["open_time"]
        closeTime1 = data["close_time"]
        minTemp1 = data["min_temp"]
        rev_door = data["_rev"]
        f = open("motor1.txt", "w")
        f.write(data["state"])
        f.close()

        myData = {'_id' : data["_id"], '_rev' : data["_rev"], 'state' : data["state"], 'open_time':openTime1,'close_time':closeTime1,'min_temp':minTemp1}
    
        #publish data to IBM cloud
        client.publishEvent(eventId="door", msgFormat="json", data=myData, qos=0, onPublish=None)
    if data["_id"] == "window":
        f = open("motor2.txt", "r")
        state2=f.read()
        print(state2)
        if state2 != data["state"]:
            if data["state"] == "open":
                #rotate_servo_motor("clockwise", 0.5, 17, 18)
                rotate_stepper_motor(18, 0.01, 6, 12, 13, 5)
                print("open window")
            if data["state"] == "close":
                #rotate_servo_motor("anticlockwise", 0.5, 17, 18)
                rotate_stepper_motor(-18, 0.01, 6, 12, 13, 5)
                print("close window")

        openTime2 = data["open_time"]
        closeTime2 = data["close_time"]
        minTemp2 = data["min_temp"]
        rev_window = data["_rev"]
        f = open("motor2.txt", "w")
        f.write(data["state"])
        f.close()
        myData = {'_id' : data["_id"], '_rev' : data["_rev"], 'state' : data["state"], 'open_time':openTime2,'close_time':closeTime2,'min_temp':minTemp2}
        #publish data to IBM cloud
        client.publishEvent(eventId="window", msgFormat="json", data=myData, qos=0, onPublish=None)
    if data["_id"] == "water":
        waterTime = cmd.data["water_time"]
        minHum = cmd.data["min_hum"]
        rev_water = data["_rev"]
        myData = {'_id' : data["_id"], '_rev' : data["_rev"], 'water_time' : waterTime, 'min_hum' : minHum}
        #publish data to IBM cloud
        client.publishEvent(eventId="water", msgFormat="json", data=myData, qos=0, onPublish=None)
            
#function turn on relay a start water pump
def water(relay_time, relay_pin):
    GPIO.setup(relay_pin,GPIO.OUT)
    GPIO.output(relay_pin,GPIO.LOW)
    GPIO.output(relay_pin,GPIO.HIGH)
    sleep(relay_time)
    GPIO.output(relay_pin,GPIO.LOW)

#function to rotate DC motor
def rotate_servo_motor(direction, rotate_time, in1, in2):
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    if direction == "clockwise":
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        sleep(rotate_time)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
    if direction == "anticlockwise":
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        sleep(rotate_time)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
           
#function to rotate stepper motor
#variable rotation speed defines time to wait between states of pins 
#if value is high rotation speed is slow and vice versa
def rotate_stepper_motor(steps, rotation_speed, pin1, pin2, pin3, pin4):
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
    if x > 0:
        for y in range(x):
            GPIO.output(out1,GPIO.HIGH)
            GPIO.output(out2,GPIO.HIGH)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.LOW)
            time.sleep(rotation_speed)
            
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.HIGH)
            GPIO.output(out3,GPIO.HIGH)
            GPIO.output(out4,GPIO.LOW)
            time.sleep(rotation_speed)
            
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.HIGH)
            GPIO.output(out4,GPIO.HIGH)
            time.sleep(rotation_speed)
            
            GPIO.output(out1,GPIO.HIGH)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.HIGH)
            time.sleep(rotation_speed)
    if x < 0:
        for y in range(-x):
            GPIO.output(out1,GPIO.HIGH)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.HIGH)
            time.sleep(rotation_speed)
            
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.HIGH)
            GPIO.output(out4,GPIO.HIGH)
            time.sleep(rotation_speed)
            
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.HIGH)
            GPIO.output(out3,GPIO.HIGH)
            GPIO.output(out4,GPIO.LOW)
            time.sleep(rotation_speed)
            
            GPIO.output(out1,GPIO.HIGH)
            GPIO.output(out2,GPIO.HIGH)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.LOW)
            time.sleep(rotation_speed)
    #set pins low to avoid overheating of stepper motor
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

    no=datetime.now()
    real_time = no.time()
    now=no.strftime("%d.%m %H:%M")
    
    if no.strftime("%H:%M") == "00:00" and was_water == True:
        was_water = False
    if waterTime != "" and (minHum > percentage1 or minHum > percentage2 or minHum > percentage3 or minHum > percentage4):
        wat = datetime.strptime(waterTime, '%H:%M').time()
        if wat > real_time and was_water == False:
            water(10, 22)
            was_water = True
    if openTime1 != "" and closeTime1 != "":
        ope1 = datetime.strptime(openTime1, '%H:%M').time()
        clo1 = datetime.strptime(closeTime1, '%H:%M').time()
        if real_time > ope1 and real_time < clo1 and temp > minTemp1 and state1 == "close":
            rotate_servo_motor("clockwise", 0.5, 17, 18)
            #rotate_stepper_motor(20, 0.01, 27, 17, 22, 18)
            f = open("motor1.txt", "w")
            f.write("open")
            f.close()
            myData = {'_id' : "door", '_rev' : door_rev, 'state' : "open", 'open_time': openTime1,'close_time':closeTime1,'min_temp':minTemp1}
            #publish data to IBM cloud
            client.publishEvent(eventId="door", msgFormat="json", data=myData, qos=0, onPublish=None)

        if (real_time < ope1 or real_time > clo1) and temp < minTemp1 and state1 == "open":
            rotate_servo_motor("anticlockwise", 0.5, 17, 18)
            #rotate_stepper_motor(-20, 0.01, 27, 17, 22, 18)
            f = open("motor1.txt", "w")
            f.write("close")
            f.close()
            myData = {'_id' : "door", '_rev' : door_rev, 'state' : "close", 'open_time': openTime1,'close_time':closeTime1,'min_temp':minTemp1}
            #publish data to IBM cloud
            client.publishEvent(eventId="door", msgFormat="json", data=myData, qos=0, onPublish=None)


    if openTime2 != "" and closeTime2 != "":
        ope2 = datetime.strptime(openTime2, '%H:%M').time()
        clo2 = datetime.strptime(closeTime2, '%H:%M').time()
        if real_time > ope2 and real_time < clo2 and temp > minTemp2 and state2 == "close":
            #rotate_stepper_motor(20, 0.01, 6, 12, 13, 5)
            f = open("motor2.txt", "w")
            f.write("open")
            f.close()
            myData = {'_id' : "window", '_rev' : window_rev, 'state' : "open", 'open_time': openTime2,'close_time':closeTime2,'min_temp':minTemp2}
            #publish data to IBM cloud
            client.publishEvent(eventId="window", msgFormat="json", data=myData, qos=0, onPublish=None)
    
        if (real_time < ope2 or real_time > clo2) and temp < minTemp2 and state2 == "open":
            #rotate_stepper_motor(20, 0.01, 6, 12, 13, 5)
            f = open("motor2.txt", "w")
            f.write("close")
            f.close()
            myData = {'_id' : "window", '_rev' : window_rev, 'state' : "close", 'open_time': openTime2,'close_time':closeTime2,'min_temp':minTemp2}
            #publish data to IBM cloud
            client.publishEvent(eventId="window", msgFormat="json", data=myData, qos=0, onPublish=None)
    
    #write data to terminal to control if values are ok
    myData = {'datetime':now, 'temperature' : temp, 'humidity' : hum, 'soil1' : percentage1, 'soil2' : percentage2, 'soil3' : percentage3, 'soil4' : percentage4}
    print(myData)
    #publish data to IBM cloud
    client.publishEvent(eventId="conditions", msgFormat="json", data=myData, qos=0, onPublish=None)
    client.commandCallback = myCommandCallback
    sleep(1)
    
#client.loop_forever()

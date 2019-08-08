import threading
import Adafruit_DHT
import time
import requests as r
import RPi.GPIO as GPIO
import string



#///for ultrasonic
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#set GPIO Pins
GPIO_TRIGGER = 38
GPIO_ECHO = 40
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
sensor=Adafruit_DHT.DHT11 
# Set GPIO sensor is connected to
gpio=5
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
#///temperature part ends
 
def print_square(num):
    pir=7
    
    GPIO.setup(pir, GPIO.IN) #PIR
    try:
        time.sleep(2) # to stabilize sensor
        while True:
            if GPIO.input(pir):
                print("Motion Detected...")
                r.post('https://api.thingspeak.com/update?api_key=6PZCGMHF6ZE6A6B6&field1=1')
                time.sleep(2) #to avoid multiple detection
            else:
                r.post('https://api.thingspeak.com/update?api_key=6PZCGMHF6ZE6A6B6&field1=0')
            time.sleep(0.1) #loop delay, should be less than detection delay

    except:
        GPIO.cleanup()


    """ 
    function to print cube of given num 
    """

    
  
def print_cube(num):
    while True:
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        dist=str(distance)
        r.post('https://api.thingspeak.com/update?api_key=BE5OHTE20F808FAJ&field1='+dist)


def print_quad(num):

    while True:
        if humidity is not None and temperature is not None:
          print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
          Temp=str(temperature)
          Humidity=str(humidity)
          r.post('https://api.thingspeak.com/update?api_key=2PE8WC4HPKFDPD43&field1='+Temp+'&field2='+Humidity)
        else:
          print('Failed to get reading. Try again!')

        time.sleep(3)
    pin.cleanup()

    

    
  
if __name__ == "__main__": 
    # creating thread 
    t1 = threading.Thread(target=print_square, args=(10,)) 
    t2 = threading.Thread(target=print_cube, args=(10,))
    t3 = threading.Thread(target=print_quad, args=(10,))
    
    t1.start() 
    
    t2.start()

    t3.start()
    #threads will be joining now
    t1.join() 
     
    t2.join()

    t3.join()
    
    print("Done!") 

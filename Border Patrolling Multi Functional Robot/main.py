from flask import Flask
from flask import render_template, request,Response
import RPi.GPIO as GPIO
from flask import url_for, jsonify
import time
import requests

app = Flask(__name__)

RForward=16
RBackward=18
LForward=13
LBackward=15


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RForward, GPIO.OUT)
GPIO.setup(RBackward, GPIO.OUT)
GPIO.setup(LForward, GPIO.OUT)
GPIO.setup(LBackward, GPIO.OUT)

GPIO.output(RForward, 0)
GPIO.output(RBackward, 0)
GPIO.output(LForward, 0)
GPIO.output(LBackward, 0)
print ("Done")



a=4
@app.route("/")
def index():
    return render_template('index.html')
def crazy_call():
    print("my multi thread program")

@app.route('/left')
def left():
    print("success")
    data1="LEFT"
    GPIO.output(LForward, GPIO.HIGH)
    GPIO.output(RBackward, GPIO.HIGH)
   
    return 'true'

@app.route('/right')
def right():
    data1="RIGHT"
    GPIO.output(RForward,GPIO.HIGH)
    GPIO.output(LBackward,GPIO.HIGH)
    
    return 'true'

@app.route('/forward')
def forward():
    print("moving forward")
    data1="FORWARD"
    GPIO.output(RForward, GPIO.HIGH)
    GPIO.output(LForward, GPIO.HIGH)
    
    return 'true'

@app.route('/reverse')
def reverse():
    data1="BACK"
    GPIO.output(RBackward, GPIO.HIGH)
    GPIO.output(LBackward, GPIO.HIGH)
    return 'true'

@app.route('/stop')
def stop():
    data1="STOP"
    GPIO.output(RForward, 0)
    GPIO.output(RBackward, 0)
    GPIO.output(LForward, 0)
    GPIO.output(LBackward, 0)
    return  'true'

@app.route('/foo', methods=['POST'])
def foo():
    Pir=requests.get('https://api.thingspeak.com/channels/744971/feeds.json?api_key=E19BORKDZFYZJFHK&results=1')
    valPir=Pir.json()
    p=(valPir["feeds"][0]["field1"])
    if int(p)==1:
        motion="Detected"
    else:
        motion="Not Detected"
    print("pir",p)
    print(motion)    

    Ultra = requests.get('https://api.thingspeak.com/channels/745134/feeds.json?api_key=V1O26F1XLTQB0FF6&results=1')
    valUltra=Ultra.json()
    d=(valUltra["feeds"][0]["field1"])
    print("distance",d)
    
    Temperature1 = requests.get('https://api.thingspeak.com/channels/745135/fields/1.json?api_key=XW8T4OK62T15QHJS&results=1')
    valTemp1=Temperature1.json()
    t=(valTemp1["feeds"][0]["field1"])
    print("temperature",t)
    
    Temperature2 = requests.get('https://api.thingspeak.com/channels/745135/fields/2.json?api_key=XW8T4OK62T15QHJS&results=1')
    valTemp1=Temperature2.json()
    h=(valTemp1["feeds"][0]["field2"])
    print("temperature",h)
    
    return jsonify({"Obstacle at distance":d,"Motion": motion, "temperature": t, "humidity":h})


    
if __name__ == "__main__":
 print ("Start")
 crazy_call()
 app.run(host='0.0.0.0',port=5010)
 

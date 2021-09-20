import serial
import time, sys 
import json
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from threading import Thread
from abc import ABCMeta, abstractmethod

class ITopic:
    def getTopic(self):
        return self.mName

    @abstractmethod
    def proc(self, msg):
        pass

class TemperatureTopic(ITopic):
    def __init__(self):
        self.mName = 'Temperature'

    def proc(self, msg):
        print(self.mName, ' : ', msg.payload.decode("utf-8"))
        # TODO: process messages for the topic of Temperature

class HumidityTopic(ITopic):
    def __init__(self):
        self.mName = 'Humidity'
    
    def proc(self, msg):
        print(self.mName, ' : ', msg.payload.decode("utf-8"))
        # TODO: process messages for the topic of Humidity

class LightTopic(ITopic):
    def __init__(self):
        self.mName = 'Light'
    
    def proc(self, msg):
        print(self.mName, ' : ', msg.payload.decode("utf-8"))
        # TODO: process messages for the topic of Light

class MQTTClient:
    def __init__(self, addr, topic):
        self.mClient = mqtt.Client(userdata=self)
        self.mClient.on_connect = self.on_connect
        self.mClient.on_message = self.on_message
        self.mClient.connect(addr, 1883, 60)
        self.mTopic = topic
        time.sleep(1)

    @staticmethod
    def on_connect(client, userdata, flags, rc):                
        print("Connected to MQTT")
        print("Connection returned result: " + str(rc) )
        
        userdata.mClient.subscribe(userdata.mTopic.mName)

    @staticmethod
    def on_message(client, userdata, msg):                     
        #print(msg.topic+" "+str(msg.payload))        
        userdata.mTopic.proc(msg)

    def start(self):
        self.mClient.loop_start()
            
    def stop(self):
        self.mClient.loop_stop(True)

def main():
    client1 = MQTTClient("mqtt.eclipseprojects.io", TemperatureTopic())
    client1.start()

    client2 = MQTTClient("mqtt.eclipseprojects.io", HumidityTopic())
    client2.start()

    client3 = MQTTClient("mqtt.eclipseprojects.io", LightTopic())
    client3.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client1.stop()
        client2.stop()
        client3.stop()
        pass

if __name__ == "__main__":
    main()

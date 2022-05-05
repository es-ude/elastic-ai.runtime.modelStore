import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import threading

nodeId = 1

def deliver(client, userdata, message):
	print("Received Data: "+str(message.payload))

target=publish.single("/service", payload="please load model 1", hostname="broker.hivemq.com")
target=subscribe.callback(deliver, "/"+str(nodeId), hostname="broker.hivemq.com")

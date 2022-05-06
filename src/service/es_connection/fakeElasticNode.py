import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

nodeId = 1

#	$ als Trennzeichen, da es keine Schlüsselbedeutung in MQTT hat
# Struktur: <nodeId>$<wantedModel>

seperator = "$"
wantedModel = "hello_world"
message = str(nodeId)+seperator+wantedModel

def deliver(client, userdata, message):
	print("Received Data: "+str(message.payload))

target=publish.single("/service", payload=message, hostname="broker.hivemq.com")
target=subscribe.callback(deliver, "/"+str(nodeId), hostname="broker.hivemq.com")

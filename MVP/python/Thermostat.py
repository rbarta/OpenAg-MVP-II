# Author: Howard Webb
# Data: 7/25/2017
# Thermostat controller that reads the temperature sensor and adjusts the exhaust fan

# Version 1.1
# Date: 4/14/2017
# Author: Ray barta
# Purpose: Thermostat
# Description: Grabs temperature and humidity from si7021 and sends it to the appropriate mqtt channel
# Input: None

#from Fan import Fan
from env import env
from si7021 import *
from datetime import datetime
from utils import send_message

import pika


#def send_message(queue, routing_key, message):
#    print("In send_message")
#    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#    channel = connection.channel()
#
#    channel.exchange_declare(exchange=queue,
#                             exchange_type='topic')
#
#    channel.basic_publish(exchange=queue,
#                          routing_key=routing_key,
#                          body=message)
#    print(" [x] Sent %r:%r" % (routing_key, message))
#    connection.close()


def Thermostat(test=False):
    indent=2
    name = env['field']['name']
    uuid = env['field']['uuid']
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.utcnow())

    print("\nChecking temperature and humidity of \"%s\"" % (name))
    print("UUID of \"%s\" is %s" % (name, uuid))
    print("Timestamp of %s" % (timestamp))
    si=si7021()
    temp = si.getTempC()
    rhumid = si.getHumidity()
    # Assign MQTT and initial message
#    queue = uuid + "_data"
    queue = "data"
    if not temp == None:
        print('Temp C: %.2f C' %temp)
        # Create routing key and message to send
        routing_key="temp.data"
        message = str(temp) 
    else:
        # Create routing key
        routing_key="temp.err"
        message = "Error no temperature data"
    #send_message(queue, routing_key, timestamp + " " + message)
#    send_message(queue, routing_key, timestamp + " " + message, indent, True)
    send_message(queue, routing_key, message, indent, True)

    if not rhumid == None:
        print('Humidity C: %.2f %%' %rhumid)
        # Create routing key and message to send
#        queue = uuid + "_data"
        queue = "data"
        routing_key="humid.data"
        message = str(rhumid) 
        print('Queue: %s' % (queue))
    else:
        # Create routing key
        routing_key="humid.err"
        message = "Error no humidity data"
    #send_message(queue, routing_key, timestamp + " " + message)
#    send_message(queue, routing_key, timestamp + " " + message, indent, True)
    send_message(queue, routing_key, message, indent, True)
                
def adjustThermostat(temp=None, test=False):
    if temp==None:
        si=si7021()
        temp = si.getTempC()
    fan=Fan()
    fan.adjust(temp, test)        
        

def test():
    print "Test"
    adjustThermostat(40, True)
    print "Adjust Thermostat 40"
    adjustThermostat(20, True)
    print "Adjust Thermostat 20"
    adjustThermostat(None, True)
    print "Adjust Thermostat None"

if __name__=="__main__":
    Thermostat()
    #adjustThermostat()

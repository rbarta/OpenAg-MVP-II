# Author: Howard Webb
# Date: 7/25/2017
# Code for managing the relay switch
#
# Version 1.1
# Date: 3/25/2017
# Author: Ray Barta
# Changed code to accept both python2 and python3
# Modified to use config.py for settings (GPIO)

import RPi.GPIO as GPIO
import time
import re
import json
from config import config, settings

MODULE = 'Relay'

ON = settings['Relay']['RelayOn']
OFF = settings['Relay']['RelayOff']

class Relay(object):

    def __init__(self):

        self.DEBUG = False
        
        if 'Debug' in settings['Relay'] and settings['Relay']['Debug']:
            print("%s : Debug key exists" % MODULE)
            self.DEBUG=True
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        for key in settings['Modules']:
            if self.DEBUG:
                print("%s : Looking for relays in module %s" % (MODULE, key))
            #for k, v in settings[key].iteritems(): # Only for python2 ### Line to be deleted##
            for k, v in settings[key].items():
                if k == 'Relay':
                    if self.DEBUG:
                        print("  settings[%s][%s] = %s" % (key, k, v))
                        print("  Setting up GPIO pins for module %s and pins %s" % (key, v))
                    # Setting up GPIO pins, may need to pass direction in the future ie. GPIO.IN
                    # Will probably pass it through as a value in config.py ie [{32:GPIO.OUT},{33:GPIO.IN}]
                    GPIO.setup(v, GPIO.OUT)
    
    def setStateOLD(self, pin, state, test=False):
        '''Change state if different'''
        if test:
            print("Current ", state, GPIO.input(pin))
        if state==ON and GPIO.input(pin)==OFF: # Some Relays are reversed therefore need to check for off
            self.setOn(pin)
            if test:
                print("Pin: ", pin, " On")
        elif state==OFF and GPIO.input(pin)==ON:
            self.setOff(pin)
            if test:
                print("Pin: ", pin, " Off")
        else:        
            if test:
                print("Pin: ", pin, " No change")

    def setState(self, pin, state, test=False):
        if isinstance(pin, list):
            changes=[]
            for i in range(len(pin)):
                '''Change state if different'''
                if test:
                    print("Current ", state[i], GPIO.input(pin[i]))
                if state[i]==ON and GPIO.input(pin[i])==OFF: # Some Relays are reversed therefore need to check for off
                    self.setOn(pin[i])
                    changes.append("On")
                    if test:
                        print("Pin: ", pin[i], " On")
                elif state[i]==OFF and GPIO.input(pin[i])==ON:
                    self.setOff(pin[i])
                    changes.append("Off")
                    if test:
                        print("Pin: ", pin[i], " Off")
                else:        
                    changes.append("No Change")
                    if test:
                        print("Pin: ", pin[i], " No change")
        else:
            '''Change state if different'''
            if test:
                print("Current ", state, GPIO.input(pin))
            if state==ON and GPIO.input(pin)==OFF: # Some Relays are reversed therefore need to check for off
                self.setOn(pin)
                changes = "On"
                if test:
                    print("Pin: ", pin, " On")
            elif state==OFF and GPIO.input(pin)==ON:
                self.setOff(pin)
                changes = "Off"
                if test:
                    print("Pin: ", pin, " Off")
            else:        
                changes = "No Change"
                if test:
                    print("Pin: ", pin, " No change")
        return changes

    def getState(self, pin):
        if isinstance(pin, list):
            state=[]
            for i in range(len(pin)):
                '''Get the current state of the pin'''
                state.append(GPIO.input(pin[i]))
        else:
            '''Get the current state of the pin'''
            state=GPIO.input(pin)
        return state

    def getStateOLD(self, pin):
        '''Get the current state of the pin'''
        state=GPIO.input(pin)
        return state

    def setOff(self, pin, test=False):
        GPIO.output(pin, OFF)
#            print("Pin ", pin, " Off")

    def setOn(self, pin, test=False):
        GPIO.output(pin, ON)
#            print("Pin ", pin, " On")

    def tests(self, tests=[]):
        if self.DEBUG:
            print("%s : Relay on = %s" % (MODULE, ON))
            print("%s : Relay off = %s" % (MODULE, OFF))
        
        pins = [] # Setup empty array of GPIO pins
        for key in settings['Modules']:
            if self.DEBUG:
                print("\nLooking for relays in module %s" % key)
            #for k, v in settings[key].iteritems():
            for k, v in settings[key].items():
                if k == 'Relay':
                    if self.DEBUG:
                        print("settings[%s][%s] = %s" % (key, k, v))
                    if isinstance(v, list):
                        pins.extend(v)
                    else:
                        pins.append(v)
        print("\nThe GPIO Pins are %s" %pins)
        print("Going to run tests %s" % tests)
        for test in tests:
            print("Running test function %s" % test)
            if test == 1:
                print("  Running test to get state of  all relays")
                self.testRelayStates(pins)
                print("  Done running test to get state of  all relays\n")
            elif test == 2:
                print("  Running test to turn all relays On then Off")
                print("  Will grab state of all relays, store and set to off")
                states=[]
                for pin in pins:
                    states.append(self.getState(pin))
                print("    States of Pins %s are %s" % (pins, states))
                print("  Will turn off all relays in 2 seconds")
                time.sleep(2)
                self.setOff(pins)
                for pin in pins:
                    print("    Testing pin %s" % pin)
                    self.testRelayOnOff(pin)

                print("  Will restore all relays to previous state in 2 seconds")
                time.sleep(2)
                GPIO.output(pins, states)
                print("  Done running test to turn all relays On then Off")
            elif test == 3:
                print("  Running test of all functions in Relay.py")
                print("  Will grab state of all relays before running tests")
                states=[]
                for pin in pins:
                    states.append(self.getState(pin))
                self.testfunctions(pins)
                print("  Will restore all relays to previous state in 2 seconds")
                time.sleep(2)
                GPIO.output(pins, states)
                print("  Done running test of all functions in Relay.py")
            else:
                print("  Test function %s is invalid! Please relook at test functions within Relay.py" % test)
    
    def testRelayStates(self,pins):
        for pin in pins:
            state = self.getState(pin)
            print("    The state of pin %s is %s" % (pin, state))

    def testRelayOnOff(self,pin):
        print("      Pin %s set to On" % pin)
        self.setOn(pin, ON)
        time.sleep(10)
        print("      Pin %s set to Off" % pin)
        self.setOff(pin, OFF)
    
    def testfunctions(self,pins):
        print("   Testing state of all relays")
        self.testRelayStates(pins)
        print("   Test Fan and Lights")
        print("    Turn Fan On - %s" % settings['Fan1']['On'])
        #self.setOn(settings['Fan']['Relay']) # Need to fix to replace RelayOn and RelayOff
        #time.sleep(10) # Need extra time for exhaust fan to spin up
        print("    Turn Light On - %s with settings %s" % (settings['Light']['Relay'], settings['Light']['On']))
        #self.setOn(settings['Light']['Relay']) # Need to fix to replace RelayOn and RelayOff
        #time.sleep(5)
        print("    Turn Fan Off - %s" % settings['Fan1']['Off'])
        #self.setOff(settings['Fan']['Relay']) # Need to fix to replace RelayOn and RelayOff
        #time.sleep(5)        
        print("    Turn Light Off - %s with settings %s" % (settings['Light']['Relay'], settings['Light']['On']))
        #self.setOff(settings['Light']['Relay']) # Need to fix to replace RelayOn and RelayOff
        #time.sleep(5)

        # This needs to be fixed later, somehow check is not right
        # Probably should just loop at top and find first fan and set variable
        if isinstance(settings['Fan1']['Relay'], list):
            fanPin = settings['Fan1']['Relay'] # Pick first Fan
        else:
            fanPin = settings['Fan1']['Relay']

        print("Conditional Turn Fan On")
        self.setState(fanPin, ON, True)
        time.sleep(5)        
        print("Conditional Turn Fan On")
        self.setState(fanPin, ON, True)
        time.sleep(5)
        print("Conditional Turn Fan Off")
        self.setState(fanPin, OFF, True)
        time.sleep(5)        
        print("Conditional Turn Fan Off")
        self.setState(fanPin, OFF, True)


if __name__=="__main__":
    r=Relay()
    r.tests([1,2,3,4]) # Test 4 should fail
    #r.tests([3])

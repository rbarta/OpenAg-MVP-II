# Author: Howard Webb
# Date: 7/25/2017
# Code for managing the relay switch
#
# Version 1.1
# Date: 3/25/2017
# Author: Ray Barta
# Changed code to accept both python2 and python3
# Modified to use config.py for settings (GPIO)
#
# Note if you specify multiple of type Relay in the settings it will just use the last one.
#
import RPi.GPIO as GPIO
import time
import re
import json
from config import Config
from utils import print_indent, check_configuration

MODULE = 'Relay'

#ON = settings['Relay']['RelayOn']
#OFF = settings['Relay']['RelayOff']

class Relay(object):

    def __init__(self):

        self.DEBUG = False
        self.indent = 2
        (warn, err) = self.check_config()
        if True in (warn, err):
            print_indent(("%s : Check config failed with Warning being %s, Error being %s" % (MODULE, warn, err)),self.indent)
            print_indent(("%s : Check types of %s in settings" % (MODULE, MODULE)),self.indent)
            exit()

        for key in Config().settings['Modules']:
            if 'Type' in Config().settings['Modules'][key]:
                if Config().settings['Modules'][key].get('Type') == MODULE:
                    settings = Config().settings['Modules']
                    self.ON = settings['Relay']['RelayOn']
                    self.OFF = settings['Relay']['RelayOff']
        
        if 'Debug' in settings['Relay'] and settings['Relay']['Debug']:
            print_indent(("%s : Debug key exists" % MODULE),self.indent)
            self.DEBUG=True
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        for key in settings:
            if self.DEBUG:
                print_indent(("%s : Looking for relays in module %s" % (MODULE, key)),self.indent)
            self.indent+=2
            for k, v in settings[key].items():
                if k == 'Relay':
                    if self.DEBUG:
                        print_indent(("  settings[%s][%s] = %s" % (key, k, v)),self.indent)
                        print_indent(("  Setting up GPIO pins for module %s and pins %s" % (key, v)),self.indent)
                    # Setting up GPIO pins, may need to pass direction in the future ie. GPIO.IN
                    # Will probably pass it through as a value in config.py ie [{32:GPIO.OUT},{33:GPIO.IN}]
                    GPIO.setup(v, GPIO.OUT)
            self.indent-=2
    
    def check_config(self):
        #
        # Checks contains items to check for and whether they are mandatory or optional
        # It then compares it against what is found of Type MODULE in the config.json file
        #
        # checks.json will have the following fields:
        #   error: Error if missing
        #   warn: Warning if missing
        # Note that the rest item is what to do if it finds something that is neither mandatory or optional
        with open(MODULE + ".json","r") as check_file:
            checks = json.load(check_file)

        for key in Config().settings['Modules']:
            if 'Type' in Config().settings['Modules'][key]:
                if Config().settings['Modules'][key].get('Type') == MODULE:
                    results = check_configuration(checks, Config().settings['Modules'][key],self.indent,self.DEBUG)
            else:
                print_indent(("*** ERROR **** Type does not exist in %s" % key),self.indent)
                return(False, True) # Warning and Error

        return(results)

    def setState(self, pin, state, test=False):
        if isinstance(pin, list):
            changes=[]
            for i in range(len(pin)):
                '''Change state if different'''
                if test:
                    print_indent(("Current ", state[i], GPIO.input(pin[i])),self.indent)
                if state[i]==self.ON and GPIO.input(pin[i])==self.OFF: # Some Relays are reversed therefore need to check for off
                    self.setOn(pin[i])
                    changes.append("On")
                    if test:
                        print_indent(("Pin: ", pin[i], " On"),self.indent)
                elif state[i]==self.OFF and GPIO.input(pin[i])==self.ON:
                    self.setOff(pin[i])
                    changes.append("Off")
                    if test:
                        print_indent(("Pin: ", pin[i], " Off"),self.indent)
                else:        
                    changes.append("No Change")
                    if test:
                        print_indent(("Pin: ", pin[i], " No change"),self.indent)
        else:
            '''Change state if different'''
            if test:
                print_indent(("Current %s %s" % (state, GPIO.input(pin))),self.indent)
            if state==self.ON and GPIO.input(pin)==self.OFF: # Some Relays are reversed therefore need to check for off
                self.setOn(pin)
                changes = "On"
                if test:
                    print_indent(("Pin: %s On" % pin),self.indent)
            elif state==self.OFF and GPIO.input(pin)==self.ON:
                self.setOff(pin)
                changes = "Off"
                if test:
                    print_indent(("Pin: %s Off" % pin),self.indent)
            else:        
                changes = "No Change"
                if test:
                    print_indent(("Pin: %s No change" % pin),self.indent)
        return changes

    def setOff(self, pin, test=False):
        GPIO.output(pin, self.OFF)

    def setOn(self, pin, test=False):
        GPIO.output(pin, self.ON)

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

    def tests(self, tests=[]):
        print_indent(("Running Tests"),self.indent)
        self.indent+=2
        
        settings = Config().settings['Modules']
        if self.DEBUG:
            print_indent(("%s : Relay on = %s" % (MODULE, self.ON)),self.indent)
            print_indent(("%s : Relay off = %s" % (MODULE, self.OFF)),self.indent)
        
        pins = [] # Setup empty array of GPIO pins
        for key in settings:
            if self.DEBUG:
                print_indent(("\nLooking for relays in module %s" % key),self.indent)
            #for k, v in settings[key].iteritems():
            for k, v in settings[key].items():
                if k == 'Relay':
                    if self.DEBUG:
                        print_indent(("settings[%s][%s] = %s" % (key, k, v)),self.indent)
                    if isinstance(v, list):
                        pins.extend(v)
                    else:
                        pins.append(v)
        print_indent(("\nThe GPIO Pins are %s" %pins),self.indent)
        print_indent(("Going to run tests %s" % tests),self.indent)
        for test in tests:
            print_indent(("Running test function %s" % test),self.indent)
            self.indent+=2
            if test == 1:
                print_indent(("Running test to get state of  all relays"),self.indent)
                self.testRelayStates(pins)
                print_indent(("Done running test to get state of  all relays\n"),self.indent)
            elif test == 2:
                print_indent(("Running test to turn all relays On then Off"),self.indent)
                print_indent(("Will grab state of all relays, store and set to off"),self.indent)
                states=[]
                for pin in pins:
                    states.append(self.getState(pin))
                print_indent(("States of Pins %s are %s" % (pins, states)),self.indent+2)
                print_indent(("Will turn off all relays in 2 seconds"),self.indent)
                time.sleep(2)
                self.setOff(pins)
                for pin in pins:
                    print_indent(("Testing pin %s" % pin),self.indent+2)
                    self.testRelayOnOff(pin)

                print_indent(("Will restore all relays to previous state in 2 seconds"),self.indent)
                time.sleep(2)
                GPIO.output(pins, states)
                print_indent(("Done running test to turn all relays On then Off"),self.indent)
            elif test == 3:
                print_indent(("Running test of all functions in Relay.py"),self.indent)
                print_indent(("Will grab state of all relays before running tests"),self.indent)
                states=[]
                for pin in pins:
                    states.append(self.getState(pin))
                self.testfunctions(pins)
                print_indent(("Will restore all relays to previous state in 2 seconds"),self.indent)
                time.sleep(2)
                GPIO.output(pins, states)
                print_indent(("Done running test of all functions in Relay.py"),self.indent)
            else:
                print_indent(("Test function %s is invalid! Please relook at test functions within Relay.py" % test),self.indent)
        self.indent-=4
    
    def testRelayStates(self,pins):
        for pin in pins:
            state = self.getState(pin)
            print_indent(("    The state of pin %s is %s" % (pin, state)),self.indent)

    def testRelayOnOff(self,pin):
        print_indent(("      Pin %s set to On" % pin),self.indent)
        self.setOn(pin, self.ON)
        time.sleep(10)
        print_indent(("      Pin %s set to Off" % pin),self.indent)
        self.setOff(pin, self.OFF)
    
    def testfunctions(self,pins):
        settings = Config().settings['Modules']
        print_indent(("   Testing state of all relays"),self.indent)
        self.testRelayStates(pins)
        print_indent(("   Test Fan and Lights"),self.indent)
        print_indent(("    Turn Fan On - %s" % settings['Fan1']['On']),self.indent)
        #self.setOn(settings['Fan']['Relay']) # Need to fix to replace RelayOn and RelayOff
        #time.sleep(10) # Need extra time for exhaust fan to spin up
        print_indent(("    Turn Light On - %s with settings %s" % (settings['Light']['Relay'], settings['Light']['On'])),self.indent)
        #self.setOn(settings['Light']['Relay']) # Need to fix to replace RelayOn and RelayOff
        #time.sleep(5)
        print_indent(("    Turn Fan Off - %s" % settings['Fan1']['Off']),self.indent)
        #self.setOff(settings['Fan']['Relay']) # Need to fix to replace RelayOn and RelayOff
        #time.sleep(5)        
        print_indent(("    Turn Light Off - %s with settings %s" % (settings['Light']['Relay'], settings['Light']['On'])),self.indent)
        #self.setOff(settings['Light']['Relay']) # Need to fix to replace RelayOn and RelayOff
        #time.sleep(5)

        # This needs to be fixed later, somehow check is not right
        # Probably should just loop at top and find first fan and set variable
        if isinstance(settings['Fan1']['Relay'], list):
            fanPin = settings['Fan1']['Relay'] # Pick first Fan
        else:
            fanPin = settings['Fan1']['Relay']

        print_indent(("Conditional Turn Fan On"),self.indent)
        self.setState(fanPin, self.ON, True)
        time.sleep(5)        
        print_indent(("Conditional Turn Fan On"),self.indent)
        self.setState(fanPin, self.ON, True)
        time.sleep(5)
        print_indent(("Conditional Turn Fan Off"),self.indent)
        self.setState(fanPin, self.OFF, True)
        time.sleep(5)        
        print_indent(("Conditional Turn Fan Off"),self.indent)
        self.setState(fanPin, self.OFF, True)


if __name__=="__main__":
    r=Relay()
    #r.tests([1,2,3,4]) # Test 4 should fail
    r.tests([3])

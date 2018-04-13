# Light Control
# Controls the turning on and turning off of lights
# Lights are wired into Relay #4 (Pin 29)
# Author: Howard Webb
# Date: 2/15/2017
#
# Version 1.1
# Date: 4/2/2017
# Author: Ray Barta
# Changed code to accept both python2 and python3
# Modified to use config.py for settings (GPIO)

#from env import env
from JsonUtil import makeEnvJson
from Relay import *
import CouchDB
from config import Config
import pprint
import time
from utils import print_indent

MODULE = 'Light'

class Light(object):

    def __init__(self, name='None'):

        self.DEBUG = False
        self.indent=2

        if name == 'None':
            print_indent(("%s : You must pass the %s name as an argument" % (MODULE,MODULE)),self.indent)
            return
        
        # Check if Module is in config file (config.py)
        #
        isInConfig=False
        isModule=False
        for key in Config().settings['Modules']:
            if 'Type' in Config().settings['Modules'][key]:
                isInConfig=True
            if Config().settings['Modules'][key].get('Type') == MODULE:
                if key == name:
                    isModule=True
                settings = Config().settings['Modules']

        if not isModule:
            print_indent(("%s : Config %s is not of type %s" % (MODULE, name, MODULE)),self.indent)
            return
        if not isInConfig:
            print_indent(("%s : Module %s does not exist in config" % (MODULE, name)),self.indent)
            return
        
        # Check if Debug is in settings and if Debug is True
        #
        if 'Debug' in settings[name] and settings[name]['Debug']:
            print_indent(("%s : Debug key exists" % MODULE),self.indent)
            pp = pprint.PrettyPrinter(indent=4)
            self.indent+=2
            print_indent(("Settings for %s are:" % name),self.indent)
            print_indent(pp.pformat(settings[name]),self.indent)
            self.indent-=2

            self.DEBUG=True

        (warn, err) = self.check_config(name)
        if True in (warn, err):
            print_indent(("%s : Check config failed with Warning being %s, Error being %s" % (MODULE, warn, err)),self.indent)
            print_indent(("%s : Check types of %s in settings" % (MODULE, MODULE)),self.indent)
            exit()
        
        self.relay=Relay()

        # Check to ensure that the module has the correct minimum number of arguments
        # 
        if not all (k in settings[name] for k in ("Relay","On","Off","Type","Mode")):
            print("%s : settings['%s'] must contain Relay, On, Off, and Type" % (MODULE, name))

        # Set variables to values from config.py
        #
        self.lightRelay=settings[name]['Relay']
        self.lightMode=settings[name]['Mode']
        self.state = {}

        # Note: If Relay is a list so must 'On' and 'Off' there is no check it will just error and skip
        #
        if isinstance(settings[name]['Relay'],list):
            self.state['On'] = []
            self.state['Off'] = []
            for i in range(len(settings[name]['On'])):
               self.state['On'].append(settings['Relay'][settings[name]['On'][i]])
            for i in range(len(settings[name]['Off'])):
               self.state['Off'].append(settings['Relay'][settings[name]['Off'][i]])
        else:
            self.state['On'] = settings['Relay'][settings[name]['On']]   # Lookup value of Relay as some
            self.state['Off'] = settings['Relay'][settings[name]['Off']] # relays are reversed ie On is 0

    def check_config(self, name='None'):
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

        if name == 'None':
            for key in Config().settings['Modules']:
                if 'Type' in Config().settings['Modules'][key]:
                    if Config().settings['Modules'][key].get('Type') == MODULE:
                        results = check_configuration(checks, Config().settings['Modules'][key],self.indent,self.DEBUG)
                else:
                    print_indent(("*** ERROR **** Type does not exist in %s" % key),self.indent)
                    return(False, True) # Warning and Error
        else:
            results = check_configuration(checks, Config().settings['Modules'][name],self.indent,self.DEBUG)

        return(results)

    # Function to turn on an off fan
    #
    def setLight(self, state, test=False):

        # Add indent
        self.indent+=2
        # Get the current state of the relay
        #
        currentState = self.relay.getState(self.lightRelay)
        if test:
            print_indent(("Current state of the Light is %s" % currentState),self.indent)

        # Change the state of the Light Relay and change if required
        #
        if currentState == self.state[state]:
            if test:
                print_indent(("setLight to %s - No change state is already correct" % state),self.indent)
        else:
            if test:
                print_indent(("setLight to %s - Change state of Light from %s to %s" % (state, currentState, self.state[state])),self.indent)

            #
            # If in Check mode do not change state of relay only report
            if not self.lightMode == 'Check':
                print("Here %s %s" % (self.lightRelay, self.state[state]))
                self.relay.setState(self.lightRelay, self.state[state])
            else:
                print_indent(("In \"Check Mode\" therefore no changes will be made"),self.indent+2)

        # Get the current state of the relay and check if change worked
        #
        currentState = self.relay.getState(self.lightRelay)
        if not currentState == self.state[state]:
            if test:
                print_indent(("setLight to %s - Could not change state" % state),self.indent)
        #
        # If in Check mode do not change state of relay only report
        if not self.lightMode == 'Check':
            self.logState(state, test)
        else:
            print_indent(("In \"Check Mode\" therefore no logging to database"),self.indent+2)
        # Reduce indent    
        self.indent-=2

    def logState(self, value, test=False):
        status_qualifier='Success'
        if test:
            status_qualifier='Test'
        jsn=makeEnvJson('State_Change', 'Light', 'Side', 'State', value, 'Light', status_qualifier)
        pp = pprint.PrettyPrinter(indent=4)
        print_indent(("LogState is:"),self.indent)
        print_indent(pp.pformat(jsn),self.indent+2)
        #CouchDB.logEnvObsvJSON(jsn)
        

    def test(self):
        print_indent(("Running Tests"),self.indent)

        print_indent(("Check for non-existant module"),self.indent)
        Light('Light9999')
        time.sleep(2)
        
        print_indent(("Check for wrong Type"),self.indent)
        Light('Fan')
        time.sleep(2)
        print_indent("Done\n",self.indent)

    def test2(self):

        print_indent(("Show settings for Light"),self.indent)
        self.indent+=2
        print_indent(("Light Mode: %s" % self.lightMode),self.indent)
        print_indent(("Light Relay: %s" % self.lightRelay),self.indent)
        print_indent(("Light Relay On: %s" % self.state['On']),self.indent)
        print_indent(("Light Relay Off: %s" % self.state['Off']),self.indent)
        self.indent-=2


        # Assume that if light is not On then it must be Off
        if self.relay.getState(self.lightRelay) == self.state['On']:
            currentState = "On"
        else:
            currentState = "Off"
        print_indent(("Current state of Light is %s (%s)" % (self.lightRelay,self.relay.getState(self.lightRelay))),self.indent)

        print_indent(("Turn Light On"),self.indent)
        self.setLight("On",True)        
        time.sleep(5)

        print_indent(("Turn Light Off"),self.indent)
        self.setLight("Off",True)    
        time.sleep(5)

        print_indent(("Turn Light Off"),self.indent)
        self.setLight("Off",True)    
        time.sleep(5)

        print_indent(("Turn Light On"),self.indent)
        self.setLight("On",True)        
        time.sleep(5)

        print_indent(("Resetting Light to original state (%s)" % currentState),self.indent)
        self.setLight(currentState, True)        

        print("Done\n")


if __name__=="__main__":
    settings = Config().settings['Modules']
    # Change so that it looks up the first available of type Light
    
    print_indent("Running tests for wrong and non-existant modules")
    f = Light()
    f.test()            
    # Loop through to test all of type Light
    # Also find first one type type fan and use that for the negetive test (feed it to test)
    #
    for name in settings:
        print("Name is %s" % (name))
        if isinstance(settings[name],dict) and settings[name].get('Type'):
            if settings[name]['Type'] == MODULE:
                print_indent("%s is of type %s. Running Tests." % (name, MODULE))
                f = Light(name)
                f.test2() 
            else:
                print_indent("%s is not of type %s, skipping tests.\n" % (name, MODULE))
        else:
            print_indent("%s is not of type %s and either, is not a dictionary or doesn't contain 'Type' key, skipping tests.\n" % (name, MODULE))


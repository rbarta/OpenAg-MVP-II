# Author: Howard Webb
# Date: 3/2/2018
# Setup Configuration
#
# Version 1.1
# Date: 3/25/2017
# Author: Ray Barta
# Add a settings configuration for modules in MPV

import RPi.GPIO as GPIO
import pprint
from utils import print_indent, check_configuration

#config={'python_dir':'/home/pi/MVP_Dev/python/', 'image_dir':'/home/pi/MVP/pictures_R/', 'web_dir':'/home/pi/MVP_Dev/web/'}


class Config():

    def __init__(self):
        self.config = {
                'python_dir':'/home/pi/OpenAG-Dev/OpenAg-MVP-II/MVP/python', 
                'image_dir':'/home/pi/MVP/pictures_R/', 
                'web_dir':'/home/pi/MVP_Dev/web/'
            }

        # settings Json
        # Debug: True - Outputs extra debugging.  Any other value won't do debugging
        #
        # Mode: Check - Check mode is just a simulation
        #       Run - Normal
        #
        # Fan: SpeedPin - GPIO pin that controls the speed of the fan, 0 means no control
        #      RpmPin - GPIO pin that it sends the fan RPM to, 0 means no control
        #
        self.settings = {   
                'Debug': False,
                'Modules': {
                    'Relay': {
                        'Debug' : False,
                        'RelayOff': GPIO.HIGH,
                        'RelayOn': GPIO.LOW,
                        'Type': 'Relay'
                    },
                    'Alert' : {
                        'Mode': 'Check',
                        'Transport': 'telegram',
                        'Token': 'put_token_here',
                        'Type': 'Alert'
                    },
                        'AirPump' : {
                        'Mode': 'Check',
                        'Location': 'Side',
                        'Watts': 10,
                        'Type': 'Check'
                    },
                    'Fan1' : {
                        'Debug': False,
                        'Mode': 'Run',
                        'Location': 'Top',
                        'Off': 'RelayOff',
                        'On': 'RelayOn',
                        'Purpose': 'Circulation',
                        'Relay': 16,
                        'Type': 'Fan',
                        'Watts': 10,
                        'SpeedPin': 0,
                        'RpmPin': 0
                    },
                    'Fan2' : {
                        'Mode': 'Check',
                        'Location': 'Side',
                        'Off': 'RelayOff',
                        'On': 'RelayOn',
                        'Purpose': 'Exhaust',
                        'Relay': 18,
                        'Type': 'Fan',
                        'Watts': 10,
                        'SpeedPin': 0,
                        'RpmPin': 0
                    },
                    'Light' : {
                        'Debug': False,
                        'Mode': 'Run',
                        'Location': 'Top',
                        'Off': ['RelayOff', 'RelayOff', 'RelayOff', 'RelayOff'],
                        'On': ['RelayOn', 'RelayOff', 'RelayOn', 'RelayOff'],
                        'Purpose': 'Light',
                        'Relay': [36, 37, 38, 40],
                        'Type': 'Light',
                        'Watts': 10,
                    },
                },
                'Rules': {
                    'TempAlertHigh': {
                        'Channel': 'Temperature', 
                        'Rule': 'Condition',
                        'Condition': '>=',
                        'Value': '26',
                        'Module': 'Fan',
                        'Settings': 'On',
                        'Alert': True,
                        'AlertOnFailure': True,
                    },
                    'TempHigh': {
                        'Channel': 'Temperature',
                        'Rule': 'Condition',
                        'Condition': '>=',
                        'Value': '25',
                        'Module': 'Fan',
                        'Settings': 'On',
                        'Alert': False,
                        'AlertOnFailure': True,
                    },
                    'TempNormal': {
                        'Channel': 'Temperature',
                        'Rule': 'Condition',
                        'Condition': '<',
                        'Value': '25',
                        'Module': 'Fan',
                        'Settings': 'Off',
                        'Alert': False,
                        'AlertOnFailure': True,
                    },
                    'TempAlertLow': {
                        'Channel': 'Temperature',
                        'Rule': 'Condition',
                        'Condition': '<',
                        'Value': '17',
                        'Module': 'Fan',
                        'Settings': 'Off',
                        'Alert': True,
                        'AlertOnFailure': True,
                    },
                    'HumidHigh': {
                        'Channel': 'Humidity',
                        'Rule': 'Condition',
                        'Condition': '<',
                        'Value': '25',
                        'Module': 'None',
                        'Settings': 'None',
                        'Alert': True,
                        'AlertOnFailure': True,
                    },
                    'HumidLow': {
                        'Channel': 'Humidity',
                        'Rule': 'Condition',
                        'Condition': '<',
                        'Value': '17',
                        'Module': 'None',
                        'Settings': 'None',
                        'Alert': True,
                        'AlertOnFailure': True,
                    },
                    'LightOn': {
                        'Channel': 'None',
                        'Rule': 'Cron',
                        'Cron': '0 12,19 * * *',
                        'Value': 'Module',
                        'Module': 'Light',
                        'Settings': 'On',
                        'Alert': False,
                        'AlertOnFailure': True,
                    },
                    'LightOff': {
                        'Channel': 'None',
                        'Rule': 'Cron',
                        'Cron': '0 7,17 * * *',
                        'Value': 'Module',
                        'Module': 'Light',
                        'Settings': 'Off',
                        'Alert': True,
                        'AlertOnFailure': True,
                    },
                    'Camera': {
                        'Channel': 'None',
                        'Rule': 'Cron',
                        'Cron': '1 0-6,12-16,19-23 * * *',
                        'Value': 'Command',
                        'Command': 'webcam.sh',
                        'Retry': 3,
                        'Alert': False,
                        'AlertOnFailure': True,
                    },
                    'CircFanOn': {
                        'Channel': 'None',
                        'Rule': 'Cron',
                        'Cron': '0 0-6,12-16,19-23 * * *',
                        'Value': 'Module',
                        'Module': 'Fan',
                        'Value': 'Off',
                        'Alert': False,
                        'AlertOnFailure': True,
                    },
                    'CircFanOff': {
                        'Channel': 'None',
                        'Rule': 'Cron',
                        'Cron': '2 0-6,12-16,19-23 * * *',
                        'Value': 'Module',
                        'Module': 'Fan',
                        'Value': 'On',
                        'Alert': False,
                        'AlertOnFailure': True,
                    },
                },
            } 

    def check_config(self):
        #
        # Checks contains items to check for and whether they are mandatory or optional
        # They have the following fields:
        #   error: Error if missing
        #   warn: Warning if missing
        # Note that the rest item is what to do if it finds something that is neither mandatory or optional
        checks = { 
                    "mandatory" : { 
                        "check" : ["Modules","Rules"],
                        "type"  : [dict,dict],
                        "error" : True, 
                        "warn"  : False, 
                    }, 
                    "optional": { 
                        "check" : ["Debug"],
                        "type"  : [bool], 
                        "error" : False, 
                        "warn"  : False, 
                    },
                    "rest": { 
                        "error" : False, 
                        "warn"  : True, 
                    }, 
                }
        return(check_configuration(checks,self.settings,2))

if __name__ == "__main__":
     print("------")
     print("config")
     print("------")
     pp = pprint.PrettyPrinter(indent=4)
#     pp.pprint(config)
     print("\n--------")
     print("settings")
     print("--------")
#     pp.pprint(settings)
     print("--------")
     print("check_config")
     c = Config()
     c.check_config()


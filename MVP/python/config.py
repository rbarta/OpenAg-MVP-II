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
                'scripts_dir':'/home/pi/OpenAG-Dev/OpenAg-MVP-II/MVP/scripts', 
                'image_dir':'/home/pi/MVP/pictures/', 
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
                        'Mode': 'Check',
                        'Location': 'Top',
                        'State': {
                            'Off': 'RelayOff',
                            'On': 'RelayOn',
                        },
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
                        'State': {
                            'Off': 'RelayOff',
                            'On': 'RelayOn',
                        },
                        'Purpose': 'Exhaust',
                        'Relay': 18,
                        'Type': 'Fan',
                        'Watts': 10,
                        'SpeedPin': 0,
                        'RpmPin': 0
                    },
                    'Light' : {
                        'Debug': False,
                        'Mode': 'Check',
                        'Location': 'Top',
                        'State': {
                            'Off': ['RelayOff', 'RelayOff', 'RelayOff', 'RelayOff'],
                            'On': ['RelayOn', 'RelayOff', 'RelayOn', 'RelayOff'],
                            'On4': ['RelayOn', 'RelayOff', 'RelayOn', 'RelayOff'],
                        },
                        'Purpose': 'Light',
                        'Relay': [36, 37, 38, 40],
                        'Type': 'Light',
                        'Watts': 10,
                    },
                },
                'Rules': {
                    'Condition': {
                        'TempAlertHigh': {
                            'Channel': 'Temperature', 
                            'Condition': '>=',
                            'Value': '26',
                            'Module': 'Fan2',
                            'State': 'On',
                            'Alert': True,
                            'AlertOnFailure': True,
                        },
                        'TempHigh': {
                            'Channel': 'Temperature',
                            'Condition': '>=',
                            'Value': '25',
                            'Module': 'Fan2',
                            'State': 'On',
                            'Alert': False,
                            'AlertOnFailure': True,
                        },
                        'TempNormal': {
                            'Channel': 'Temperature',
                            'Condition': '<',
                            'Value': '25',
                            'Module': 'Fan2',
                            'State': 'Off',
                            'Alert': False,
                            'AlertOnFailure': True,
                        },
                        'TempAlertLow': {
                            'Channel': 'Temperature',
                            'Condition': '<',
                            'Value': '17',
                            'Module': 'Fan2',
                            'State': 'Off',
                            'Alert': True,
                            'AlertOnFailure': True,
                        },
                        'HumidHigh': {
                            'Channel': 'Humidity',
                            'Condition': '<',
                            'Value': '25',
                            'Alert': True,
                            'AlertOnFailure': True,
                        },
                        'HumidLow': {
                            'Channel': 'Humidity',
                            'Condition': '<',
                            'Value': '17',
                            'Alert': True,
                            'AlertOnFailure': True,
                        },
                    },
                    'Cron': {
                        'LightOn': {
                            'Cron': '0 12,19 * * *',
                            'Value': 'Module',
                            'Module': 'Light',
                            'State': 'On',
                            'Alert': False,
                            'AlertOnFailure': True,
                        },
                        'LightOff': {
                            'Cron': '0 7,17 * * *',
                            'Value': 'Module',
                            'Module': 'Light',
                            'State': 'Off',
                            'Alert': True,
                            'AlertOnFailure': True,
                        },
                        'Camera': {
                            'Cron': '1 0-6,12-16,19-23 * * *',
                            'Value': 'Command',
                            'Command': 'webcam.sh',
                            'Retry': 3,
                            'Alert': False,
                            'AlertOnFailure': True,
                        },
                        'CircFanOn': {
                            'Cron': '0 0-6,12-16,19-23 * * *',
                            'Value': 'Module',
                            'Module': 'Fan1',
                            'State': 'Off',
                            'Alert': False,
                            'AlertOnFailure': True,
                        },
                        'CircFanOff': {
                            'Cron': '2 0-6,12-16,19-23 * * *',
                            'Value': 'Module',
                            'State': 'Fan1',
                            'State': 'On',
                            'Alert': False,
                            'AlertOnFailure': True,
                        },
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


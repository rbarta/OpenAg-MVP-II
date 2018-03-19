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

#config={'python_dir':'/home/pi/MVP_Dev/python/', 'image_dir':'/home/pi/MVP/pictures_R/', 'web_dir':'/home/pi/MVP_Dev/web/'}
config = {
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
settings = {   
        'Modules': ['Alert', 'Relay', 'Fan', 'Light'],
        'Relay': {
            'Debug': True,
            'RelayOff': GPIO.HIGH,
            'RelayOn': GPIO.LOW
        },
        'Alert' : {
            'Mode': 'Check',
            'Transport': 'telegram',
            'Token': 'put_token_here'
        },
        'Fan' : {
            'Mode': 'Check',
            'Location': [ 'Top', 'Side'],
            'Off': ['RelayOff', 'RelayOff'],
            'On': ['RelayOn', 'RelayOn'],
            'Purpose': ['Circulation', 'Exhaust'],
            'Relay': [33, 32],
            'Type': 'Fan',
            'SpeedPin': 0,
            'RpmPin': 0
        },
        'Light' : {
            'Mode': 'Check',
            'Location': 'Top',
            'Off': ['RelayOff', 'RelayOff', 'RelayOff', 'RelayOff'],
            'On': ['RelayOff', 'RelayOn', 'RelayOff', 'RelayOn'],
            'Purpose': 'Light',
            'Relay': [35, 36, 37, 38],
            'Type': 'Light',
        },
    } 
if __name__ == "__main__":
     print("------")
     print("config")
     print("------")
     pp = pprint.PrettyPrinter(indent=4)
     pp.pprint(config)
     print("\n--------")
     print("settings")
     print("--------")
     pp.pprint(settings)

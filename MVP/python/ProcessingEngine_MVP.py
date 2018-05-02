# Version 1.1
# Date: 3/25/2017
# Author: Ray Barta
# Purpose: Process Engine
# Description: This will be the main brain of the MVP, it's purpose is to read in a config file
#       and to utilize it to control the MVP based on the values from the sensors, modules and rules
# Input: config.py
# Output: log

#from env import env
from JsonUtil import makeEnvJson
#import CouchDB
#from config import settings
from config import Config
import pprint
import time
import json
from utils import print_indent, check_configuration
import importlib

MODULE='ProcessingEngine_MVP'

class ProcessingEngine_MVP(object):

    def __init__(self, name='None'):

        self.DEBUG = False
        self.indent=2

        # Check if Debug is in settings and if Debug is True
        #
        if 'Debug' in Config().settings and Config().settings['Debug']:
            print_indent(("%s : Debug key exists" % MODULE),self.indent)
            pp = pprint.PrettyPrinter(indent=4)
            self.indent+=2
            print_indent(("Settings are:" ),self.indent)
            print_indent(pp.pformat(Config().settings),self.indent)
            self.indent-=2

            self.DEBUG=True
        
        # Check to ensure that the module has the correct minimum number of arguments
        # 
        if not all (k in Config().settings for k in ("Modules","Rules")):
            print("%s : settings must contain Modules, and Rules" % (MODULE))

        # Loop through all modules and check for correct settings
        # and exit if any error out.  Note that this will dynamically
        # load the modules into the module variable
        #
        self.module = {} 
        for key in Config().settings['Modules']:
            if 'Type' in Config().settings['Modules'][key]:
                modulename=Config().settings['Modules'][key]['Type']
                print_indent(("\nLoading library: %s and checking module: %s" %(modulename, key)),self.indent)
                self.indent+=2
                # Dynamically load modules and run check_config for each
                self.module[modulename] = getattr(importlib.import_module(modulename),modulename)
                (warn, err) = self.module[modulename](key).check_config()
                if True in (warn, err):
                    print_indent(("%s : Check config failed with Warning being %s, Error being %s" % (MODULE, warn, err)),self.indent)
                    print_indent(("%s : Check types of %s in settings" % (MODULE, MODULE)),self.indent)
                    exit()
                self.indent-=2
                print_indent(("Check complete for module: %s" %(key)),self.indent)

#
# Need a check config to go through and check the Rules maybe a check_rules function
#
#
        print_indent(("\n%s: Running check on rules in config" %(MODULE)),self.indent)
        (warn, err) = self.check_rules()

    def check_rules(self, name='None'):
        #
        # Checks contains items to check for and whether they are mandatory or optional
        # It then compares it against what is found of Type MODULE in the config.json file
        #
        # checks.json will have the following fields:
        #   error: Error if missing
        #   warn: Warning if missing
        # Note that the rest item is what to do if it finds something that is neither mandatory or optional
        self.indent+=4
        # Read json file. Note that there is no check for successful load.  Maybe later
        with open(MODULE + ".json","r") as check_file:
            checks = json.load(check_file)

        self.cron={}
        self.condition={}
        if name == 'None':
            for key in Config().settings['Rules']['Condition']:
                print_indent(("%s : Checking rule" % (key)),self.indent-2)
                (warn, err) = check_configuration(checks['Condition'], Config().settings['Rules']['Condition'][key],self.indent,self.DEBUG)
                if True in (warn, err):
                    print_indent(("%s : Check config failed with Warning being %s, Error being %s" % (MODULE, warn, err)),self.indent)
                    print_indent(("%s : Check types of %s in settings" % (MODULE, MODULE)),self.indent)
                    exit()
                self.check_rule_to_module(Config().settings['Rules']['Condition'][key])
                self.condition[key] = Config().settings['Rules']['Condition'][key]
            for key in Config().settings['Rules']['Cron']:
                print_indent(("%s : Checking rule" % (key)),self.indent-2)
                (warn, err) = check_configuration(checks['Cron'], Config().settings['Rules']['Cron'][key],self.indent,self.DEBUG)
                if True in (warn, err):
                    print_indent(("%s : Check config failed with Warning being %s, Error being %s" % (MODULE, warn, err)),self.indent)
                    print_indent(("%s : Check types of %s in settings" % (MODULE, MODULE)),self.indent)
                    exit()
                self.check_rule_to_module(Config().settings['Rules']['Cron'][key])
                self.cron[key] = Config().settings['Rules']['Cron'][key]
                
        else:
            #
            # Right now this won't do anything.  Need to decide for cron and condition rules if individual
            # check_rules is required.
            #
            print_indent(("%s : Checking rule" % (key)),self.indent-2)
            (warn, err) = check_configuration(checks, Config().settings['Rules'][name],self.indent,self.DEBUG) 
            if True in (warn, err):
                print_indent(("%s : Check config failed with Warning being %s, Error being %s" % (MODULE, warn, err)),self.indent)
                print_indent(("%s : Check types of %s in settings" % (MODULE, MODULE)),self.indent)
                exit()
            self.check_rule_to_module(Config().settings['Rules'][name])
        
        self.indent-=4
        return(warn,err)

    def check_rule_to_module(self, name='None'):
        # Check that uses name['Module'] to get valid states and check against what is being
        # passed in Settings
        #
        # Note: this can get cleaned up by preloading all modules and their setStates in the __init__
        #
        #print("Name is %s" % name)
        if 'Module' in name:
        #    print(name['Module'])
        #    print(name['State'])
            if not name['Module'] in Config().settings['Modules']:
                print("Module does not exist in main configuration file.")
                exit()
            else:
        #        print("Module in Modules")
        #        print(Config().settings['Modules'][name['Module']]['Type'])
        #        print(self.module)
                m = self.module[Config().settings['Modules'][name['Module']]['Type']](name['Module'])
        #        print(m.setState("",True))
                if not name['State'] in m.setState("",True):
                    print("State does not exist in main configuration file for $s" % name['Module'])
                    exit()
        else:
            print("No Module")
        return

    def engine(self):
        #
        # Maybe when checking rules import into Array
        # This can then be used to check the individual rules
        # Each setFunction or getFunction should have display variables when help is passed
        #

        #from Thermostat import Thermostat
        #for i in range(10):
        #    print(i)
        #    Thermostat()
        print(Config().settings['Rules'])

        import pika

        credentials = pika.PlainCredentials('mvp_user', 'mvp')
        parameters = pika.ConnectionParameters(credentials=credentials, 
        				       host='192.168.150.75')
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(exchange='8e89e414-0181-440a-9170-702434c8f400_data',
                                 exchange_type='topic')

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        binding_keys = "#"

        for binding_key in binding_keys:
            channel.queue_bind(exchange='8e89e414-0181-440a-9170-702434c8f400_data',
                               queue=queue_name,
                               routing_key=binding_key)

        print(' [*] Waiting for logs. To exit press CTRL+C')
        channel.basic_consume(self.callback,
                              queue=queue_name,
                              no_ack=True)

        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))
        if method.routing_key == "temp.data":
           (msgdate, msgtime, msgtemp) = body.split(" ")
#           print(msgdate)
#           print(msgtime)
#           print(msgtemp)


        #print("Printing module list items")
        #for key in self.module:
        #    print(key)
        #    method_list = [func for func in dir(self.module[key]) if callable(getattr(self.module[key], func)) and not func.startswith("__")]
        #    print(method_list)
        
        return


    def test(self):
        print_indent(("\nRunning Tests"),self.indent)

        print_indent(("Starting Process Engine"),self.indent)
        
        print_indent(("Cron is: %s" %self.cron),self.indent)
        print_indent(("Condition is: %s" %self.condition),self.indent)

        self.engine()
        
        time.sleep(2)
        print_indent("Done\n",self.indent)

if __name__=="__main__":
    
    f = ProcessingEngine_MVP()
    #f.engine()
    f.test()            


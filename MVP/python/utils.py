from pydoc import locate

def add_space(text, indent=0):
    fstring = ' ' * indent + '{}'
    return ''.join([fstring.format(l) for l in text.splitlines(True)])

def print_indent(text, indent=0):
    print("%s" % add_space(text,indent))
    return indent

def check_configuration(checks,settings,indent,DEBUG=False):
    #
    # Checks contains items to check for and whether they are mandatory or optional
    # They have the following fields:
    #   error: Error if missing
    #   warn: Warning if missing
    # Note that the rest item is what to do if it finds something that is neither mandatory or optional
    # Maybe write check for checks ie look for mandatory error warn check rest
    #
    # This checks for valid high level items in config.py
    checked=[]
    warning = False
    error = False
    if DEBUG:
        print_indent(("Settings are %s " % (settings)),indent)
    for check in ["mandatory","optional"]:
        if DEBUG:
            print_indent(("Checking for %s options in settings" % (check)),indent)
            print_indent(("Looking for %s options in settings" % (checks[check].get('check'))),indent+2)
            indent+=4
        for key in checks[check].get('check'):
            name=key
            checked.append(name)
            if 'list' in checks[check]['check'][name]:
                nametype=locate(checks[check]['check'][name]['list']['type'])
                # Check if the key is in settings and is of the correct type
                #
                if name in settings and all(isinstance(x,nametype) for x in settings[name]):
                    if DEBUG:
                         print_indent(("%s is %s and exists in settings." % (name, check)),indent)
                else:
                    text = "" 
                    if checks[check].get('warn') == 'True':
                        text="*** WARNING *** "
                        warning = True
                    if checks[check].get('error') == 'True':
                        text="*** ERROR *** "
                        error = True
                    if settings.get(name):
                        if not all(isinstance(x,nametype) for x in settings[name]):
                            print_indent(("%s%s not the correct type of %s." % (text, name, nametype)),indent)
                    else:
                        print_indent(("%s%s is %s and does not exists in settings." % (text, name, check)),indent)
            else:
                nametype=locate(checks[check]['check'][name]['type'])
                # Check if the key is in settings and is of the correct type
                #
                if name in settings and isinstance(settings[name],nametype):
                    if DEBUG:
                         print_indent(("%s is %s and exists in settings." % (name, check)),indent)
                else:
                    text = "" 
                    if checks[check].get('warn') == 'True':
                        text="*** WARNING *** "
                        warning = True
                    if checks[check].get('error') == 'True':
                        text="*** ERROR *** "
                        error = True
                    if settings.get(name):
                        if not isinstance(settings[name],nametype):
                            print_indent(("%s%s not the correct type of %s." % (text, name, nametype)),indent)
                    else:
                        print_indent(("%s%s is %s and does not exists in settings." % (text, name, check)),indent)
        if DEBUG:
            indent-=4
    # Note unchecked options don't work for a list type 
    if DEBUG:
        print_indent(("Looking unchecked options in settings" % (checks[check].get('check'))),indent)
        indent+=2
    for name in settings:
        if name in checked:
            if DEBUG:
                 print_indent(("%s was either mandatory or optional" % name),indent)
        else:
            text = "" 
            if checks['rest'].get('warn') == 'True':
                text="*** WARNING *** "
                warning = True
            if checks[check].get('error') == 'True':
                text="*** ERROR *** "
                error = True
            print_indent(("%s%s was not in either mandatory or optional" % (text,name)),indent)
    if DEBUG:
        indent-=2
        print_indent(("Warning is %s and Errors is %s" % (warning, error)),indent)
    return(warning, error)

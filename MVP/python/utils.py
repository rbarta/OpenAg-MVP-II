def add_space(text, indent=0):
    fstring = ' ' * indent + '{}'
    return ''.join([fstring.format(l) for l in text.splitlines(True)])

def print_indent(text, indent=0):
    print("%s" % add_space(text,indent))
    return indent

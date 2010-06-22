"""
State global to the whole package.

"""

import sys, re

from metaconfig.mconf import MetaConfig

_default_metaconfig = MetaConfig()

def get_config(name):
    return _default_metaconfig.get_config(name)

def add_config(name, config_parser):
    return _default_metaconfig.add_config(name, config_parser)

def add_config_file(name, config, ConfigClass=None):
    return _default_metaconfig.add_config_file(name, config, ConfigClass)

def load_argv(argv=sys.argv, remove=True):
    """
    Load the default MetaConfig from arguments on the command line.

    If remove=True remove arguments that metaconfig recognises.

    """

    for arg in argv[1:]:
        mo = re.match(r'--config=(.*):(.*)', arg)
        if mo:
            name, file = mo.groups()
            add_config_file(name, file)
            if remove:
                argv.remove(arg)
            
def clear():
    return _default_metaconfig.clear()
    

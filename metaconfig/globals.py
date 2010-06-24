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

            
def clear():
    return _default_metaconfig.clear()
    

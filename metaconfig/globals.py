# BSD Licence
# Copyright (c) 2010, Science & Technology Facilities Council (STFC)
# All rights reserved.
#
# See the LICENSE file in the source distribution of this software for
# the full license text.

"""
State global to the whole package.

"""

import sys, re, os

from metaconfig.mconf import MetaConfig

_default_metaconfigfile = os.environ.get('METACONFIG_CONF',
                                         os.path.join(
        os.environ.get('HOME', ''), '.metaconfig.conf'))

_default_metaconfig = MetaConfig.from_config_file(_default_metaconfigfile)



def get_config(name):
    return _default_metaconfig.get_config(name)

def add_config(name, config_parser):
    return _default_metaconfig.add_config(name, config_parser)

def add_config_file(name, config, ConfigClass=None):
    return _default_metaconfig.add_config_file(name, config, ConfigClass)

            
def clear():
    return _default_metaconfig.clear()
    

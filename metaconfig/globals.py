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

import logging
log = logging.getLogger(__name__)

def _get_metaconfigfile():
    try_configs = [os.path.join(os.environ.get('HOME', ''), '.metaconfig.conf'),
                   os.path.join(sys.prefix, 'etc', 'metaconfig.conf')]
    if 'METACONFIG_CONF' in os.environ:
        try_configs[0:] = [(os.environ['METACONFIG_CONF'])]

    for config in try_configs:
        if os.path.exists(config):
            log.debug('Selected %s as metaconfig.conf' % config)
            return config
    else:
        return None

def reload():
    global _metaconfig

    _metaconfig_file = _get_metaconfigfile()
    if _metaconfig_file is None:
        _metaconfig = MetaConfig()
    else:
        _metaconfig = MetaConfig.from_config_file(_metaconfig_file)


def get_config(name):
    return _metaconfig.get_config(name)

def add_config(name, config_parser):
    return _metaconfig.add_config(name, config_parser)

def add_config_file(name, config, ConfigClass=None):
    return _metaconfig.add_config_file(name, config, ConfigClass)

            
def clear():
    return _metaconfig.clear()
    

## Bootstrap
reload()

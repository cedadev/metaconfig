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

_metaconfig = None

def _default_search_path():
    search_path = [
        './metaconfig.conf',
        os.path.join(os.environ.get('HOME', ''), '.metaconfig.conf'),
        os.path.join(sys.prefix, 'etc', 'metaconfig.conf')
        ]
    if 'METACONFIG_CONF' in os.environ:
        search_path[0:] = [(os.environ['METACONFIG_CONF'])]

    return search_path

def init_from_config(config):
    global _metaconfig

    if _metaconfig is not None:
        raise Exception("Metaconfig is already initialised")

    _metaconfig = MetaConfig.from_config(config)

def init(search_path=None):
    global _metaconfig

    if _metaconfig is not None:
        raise Exception("Metaconfig is already initialised")

    if search_path is None:
        search_path = _default_search_path()
    for config in search_path:
        if os.path.exists(config):
            log.debug('Selected %s as metaconfig.conf' % config)
            _metaconfig = MetaConfig.from_config_file(config)
            return
    else:
        _metaconfig = MetaConfig()
    

def get_config(name, inherit=True):
    if _metaconfig is None:
        init()

    return _metaconfig.get_config(name, inherit=inherit)

def add_config(name, config_parser):
    if _metaconfig is None:
        init()

    return _metaconfig.add_config(name, config_parser)

def add_config_file(name, config, ConfigClass=None):
    if _metaconfig is None:
        init()

    return _metaconfig.add_config_file(name, config, ConfigClass)


def reset():
    _metaconfig = None

# BSD Licence
# Copyright (c) 2010, Science & Technology Facilities Council (STFC)
# All rights reserved.
#
# See the LICENSE file in the source distribution of this software for
# the full license text.

"""
metaconfig
----------

We want to do:

{{{
import metaconfig

# Config is a ConfigParser instance (or subclass)
# Returns the lowest level config file available (e.g. if __name__ == 'foo.bar.baz' and there is a config 
# defined for 'foo.bar' use that.
config = metaconfig.get_config(__name__)
}}}


These options are bootstraped on entry into Python as:

{{{
import metaconfig

metaconfig.add_config_file(name, path)
metaconfig.add_config(name, configParser)
metaconfig.metaconfig(metaconfig)
metaconfig.metaconfig_file(metaconfig_file)
metaconfig.from_argv()

or something like that
}}}


"""

import sys
import ConfigParser
import re

import logging
log = logging.getLogger(__name__)

class Error(Exception):
    pass

DEFAULT_CONFIG_PARSER = ConfigParser.ConfigParser

class MetaConfig(object):
    def __init__(self):
        self._configs = {}

    def add_config_file(self, name, path, ConfigClass=DEFAULT_CONFIG_PARSER):

        conf = ConfigClass()
        conf.read([path])

        return self.add_config(name, conf)


    def add_config_fh(self, name, fileobj, ConfigClass=DEFAULT_CONFIG_PARSER):

        conf = ConfigClass()
        conf.readfp(fileobj)

        return self.add_config(name, conf)

    def add_config(self, name, config_parser):
        if name in self._configs:
            Error("Config %s already exists" % name)
        else:
            config_parser.__config_name__ = name
            self._configs[name] = config_parser

        return config_parser

    def get_config(self, name, ConfigClass=DEFAULT_CONFIG_PARSER, inherit=True):
        log.debug('Requested config %s, inherit=%s' % (name, inherit))

        if inherit:
            parts = name.split('.')
            while parts:
                name1 = '.'.join(parts)
                log.debug("Looking for config %s" % name1)
                try:
                    config = self._configs[name1]
                    log.debug("Selected config %s" % name1)
                    return config
                except KeyError:
                    parts = parts[:-1]
                    
        if name in self._configs:
            log.debug("Selecting config %s" % name)
            return self._configs[name]
        else:
            config = self.add_config(name, ConfigClass())
            log.debug("New config %s" % name)
            return config
        

    @classmethod
    def from_config(klass, config_parser):
        mf = klass()

        mf._parse_nested_configs(config_parser)
        mf._parse_external_configs(config_parser)

        return mf

    @classmethod
    def from_config_file(klass, config_file):
        cnf = DEFAULT_CONFIG_PARSER()
        cnf.read(config_file)

        return klass.from_config(cnf)

    @classmethod
    def from_config_fh(klass, config_fh):
        cnf = DEFAULT_CONFIG_PARSER()
        cnf.readfp(config_fh)
        
        return klass.from_config(cnf)


        
    def _parse_nested_configs(self, config_parser):
        """
        Parse configs embedded in the metaconfig file.
        """
        if not config_parser.has_option('metaconfig', 'configs'):
            return

        configs = config_parser.get('metaconfig', 'configs').split()
        D = {}
        for section in config_parser.sections():
            mo = re.match(r'(.+?):(.*)', section)
            if not mo:
                continue

            prefix, ssec = mo.groups()
            D.setdefault(prefix, []).append(ssec)

        for config in configs:
            cp = ConfigParser.ConfigParser()
            for ssec in D[config]:
                cp.add_section(ssec)
                sec = '%s:%s' % (config, ssec)
                for option in config_parser.options(sec):
                    cp.set(ssec, option, config_parser.get(sec, option, 
                                                           raw=True))

            self.add_config(config, cp)

    def _parse_external_configs(self, config_parser):
        """
        Parse external config files referenced in metaconfig.conf.
        """
        pass
        #!FIXME: need to name each config.
        #if not config_parser.has_option('metaconfig', 'config-files'):
        #    return
        #
        #config_files = config_parser.get('metaconfig', 'config-files').split()
        #for cf in config_files:
        #    self.add_config_file(cf)

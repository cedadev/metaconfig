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

class Error(Exception):
    pass

class MetaConfig(object):
    def __init__(self):
        self._configs = {}

    def add_config_file(self, name, path, ConfigClass=None):
        if ConfigClass is None:
            ConfigClass = ConfigParser.ConfigParser

        conf = ConfigClass()
        conf.read([path])

        return self.add_config(name, conf)


    def add_config_fh(self, name, fileobj, ConfigClass=None):
        if ConfigClass is None:
            ConfigClass = ConfigParser.ConfigParser

        conf = ConfigClass()
        conf.readfp(fileobj)

        return self.add_config(name, conf)

    def add_config(self, name, config_parser):
        self._configs[name] = config_parser

    def get_config(self, name):
        parts = name.split('.')
        while parts:
            name1 = '.'.join(parts)
            try:
                return self._configs[name1]
            except KeyError:
                parts = parts[:-1]
        raise Error('Config matching %s not found' % name)
            
    def clear(self):
        self._configs = {}

    @classmethod
    def from_config(Class, config_parser):
        mf = Class()

        configs = config_parser.get('metaconfig', 'configs').split()
        D = {}
        for section in config_parser.sections():
            mo = re.match(r'(.*):(.*)', section)
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
                    cp.set(ssec, option, config_parser.get(sec, option))
            mf.add_config(config, cp)

        return mf

    @classmethod
    def from_config_file(Class, config_file):
        raise NotImplementedError

    @classmethod
    def from_config_fh(Class, config_fh):
        raise NotImplementedError


        

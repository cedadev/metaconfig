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

configs can be specified on the command line:
$ python --config=foo.bar:file

Or via a master config file
$ python --metaconfig=file

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
    def from_config(self, config_parser):
        raise NotImplementedError

    @classmethod
    def from_config_file(self, config_file):
        raise NotImplementedError

    @classmethod
    def from_config_fh(self, config_fh):
        raise NotImplementedError


        

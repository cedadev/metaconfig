Package Developer Interface
===========================

Metaconfig has been largely inspired by the ease of use of the
``logging`` module.  When writing code it is trivially easy to enable
module-specific logging using the simple recipe::

  import logging
  log = logging.getLogger(__name__)

This defers all decisions about how logging events are handled until
later and you can proceed to write code using the ``log`` object.

Metaconfig translates this recipe into a mechanism for instantly
retrieving a :mod:`ConfigParser.ConfigParser` object specific to your module::

  >>> import metaconfig
  >>> config = metaconfig.get_config(__name__)

Where that :mod:`ConfigParser.ConfigParser` object comes from is not
the immediate concern of the developer.  The source can be decided at
configuration time.  However, ``get_config()`` will always return the
same :mod:`ConfigParser.ConfigParser` object for any given name.  If
the config doesn't exist an empty one is returned.

  >>> config.sections()
  []

In a similar way to the logging module metaconfig treats config names
as a hierarchal tree of "."-separated keys.  This allows you to map
config keys directly onto your package hierarchy or devise an
alternative hierarchy.  In the example above metaconfig will return
the ConfigParser object relating to ``__name__``

When creating nested packages you will often want to centralise your
configuration at the top-level package.  Therefore by default
:func:`metaconfig.get_config` will traverse up the config-key tree
until a config object is found::

  >>> root_config = metaconfig.get_config('myroot')
  >>> root_config.sections()
  []
  >>> root_config.add_section('sec1')
  >>> root_config.set('sec1', 'x', '42')

  >>> myconfig = metaconfig.get_config('myroot.sub1')
  >>> myconfig.get('sec1', 'x')
  '42'
  >>> myconfig == root_config
  True

If this is not what is desired you can force a config object for the
exact key to be returned.  If a config doesn't exist under that key a
new one will be created::

  >>> myconfig2 = metaconfig.get_config('myroot.sub2', inherit=False)
  >>> myconfig2.sections()
  []

If you need to know exactly where your config has come from use the ``__config_name__`` attribute::

  >>> myconfig.__config_name__
  'myroot'
  >>> myconfig2.__config_name__
  'myroot.sub2'
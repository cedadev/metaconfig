Configuration Management Interface
==================================

So you have a package that can be configured with metaconfig and you
want to start using it right now.  How do you set where your named
configs come from?  The easiest way is to create a `metaconfig file`.
This is a :mod:`ConfigParser.ConfigParser`.  Metaconfig will search
the following locations until it finds the file:

1. The value of the ``METACONFIG_CONF`` environment variable if set.
2. ``metaconfig.conf`` in the current directory.
3. ``$HOME/.metaconfig.conf``
4. ``<sys.prefix>/etc/metaconfig.conf``

These options give you a lot of flexibility about where you define
your master configuration.  If you are developing in a sandbox you may
use #2 or you can set your configuration per-user with #3.  Use option
#4 to set the configuration system-wide or per-virtualenv.  You can
always override the default with #1.

Metaconfig.conf Format
----------------------

The metaconfig configuration must contain the section ``metaconfig``.
Within this the option ``configs`` is a whitespace-separated sequence
of config names.  For each config name the section
``<name>:<section>`` must be defined which corresponds to the section
``<section>`` of config ``<name>``.

We can demonstrate this using the function
:mod:`metaconfig.init_from_string` to initialise metaconfig without
writing the config file.

  >>> import metaconfig
  >>> import tempfile
  >>> metaconfig.reset()
  >>> metaconfig.init_from_string("""
  ... [metaconfig]
  ... configs = foo
  ...
  ... [foo:bar]
  ... a = 42
  ... b = baz
  ... """)

Somewhere else within your python code this configuration can be retrieved.

  >>> config = metaconfig.get_config('foo')
  >>> config.getint('bar', 'a')
  42
  >>> config.get('bar', 'b')
  'baz'


Of course you can define as many configs and sections within
metaconfig as you like.

  >>> metaconfig.reset()
  >>> metaconfig.init_from_string("""
  ... [metaconfig]
  ... configs = foo bar
  ...
  ... [foo:sec1]
  ... a = 42
  ...
  ... [foo:sec2]
  ... a = 101
  ...
  ... [bar:sec1]
  ... a = 999
  ... """)
  >>> foo_config = metaconfig.get_config('foo')
  >>> foo_config.getint('sec1', 'a')
  42
  >>> foo_config.getint('sec2', 'a')
  101
  >>> bar_config = metaconfig.get_config('bar')
  >>> bar_config.getint('sec1', 'a')
  999


Handling of the DEFAULT section
-------------------------------

The DEFAULT section works as you would expect per config.  Notice
options defined in the top-level DEFAULT section will propagate to all
configs defined in that file.

  >>> metaconfig.reset()
  >>> metaconfig.init_from_string("""
  ... [DEFAULT]
  ... c = 99
  ...
  ... [metaconfig]
  ... configs = foo
  ...
  ... [foo:DEFAULT]
  ... a = 1
  ... b = 2
  ...
  ... [foo:bar]
  ... a = 3
  ... """)
  >>> foo_config = metaconfig.get_config('foo')
  >>> foo_config.getint('bar', 'a')
  3
  >>> foo_config.getint('bar', 'b')
  2
  >>> foo_config.getint('bar', 'c')
  99

Referencing external config files
---------------------------------

Individual configs can be referenced in separate files by specifying a section
that maps config names to files.

  >>> metaconfig.reset()
  >>> import tempfile
  >>> conf_fh = tempfile.NamedTemporaryFile()
  >>> conf_fh.write("""
  ... [DEFAULT]
  ... y = default_text
  ... 
  ... [sec_a]
  ... x = 99
  ... y = some_text
  ... 
  ... [sec_b]
  ... x = 22
  ... """)
  >>> conf_fh.flush()
  >>> metaconfig.init_from_string("""
  ... [metaconfig]
  ... config-files = myconfigs
  ... 
  ... [myconfigs]
  ... foo = %s
  ... """ % conf_fh.name)

The config "foo" is now available

  >>> config = metaconfig.get_config('foo')
  >>> config.getint('sec_a', 'x')
  99
  >>> print config.get('sec_a', 'y')
  some_text
  >>> config.getint('sec_b', 'x')
  22
  >>> print config.get('sec_b', 'y')
  default_text
  

Including other metaconfig files
--------------------------------

The root metaconfig file can reference other metaconfign files to be
included.  This is different from referencing external configs as the
metaconfig syntax is applied to the included file.  The semantics
follows the ConfigParser.read method.  The "include" option is a
space-separated list of metaconfig files.


  >>> metaconfig.reset()
  >>> import tempfile
  >>> mconf_fh = tempfile.NamedTemporaryFile()
  >>> mconf_fh.write("""
  ... [metaconfig]
  ... configs = foo
  ...
  ... [foo:bar]
  ... a = 42
  ... b = baz
  ... """)
  >>> mconf_fh.flush()
  >>> metaconfig.init_from_string("""
  ... [metaconfig]
  ... configs = foo
  ... include = %s
  ...
  ... [foo:bar]
  ... a = 99
  ... c = woz
  ... """ % mconf_fh.name)

Included files override the settings

  >>> config = metaconfig.get_config('foo')
  >>> config.getint('bar', 'a')
  42
  >>> print config.get('bar', 'b')
  baz
  >>> print config.get('bar', 'c')
  woz

Configuring logging
-------------------

You can bootstrap your logging configuration from your metaconfig file
using the ``logging`` option.  This option provides the path to a
separate logging configuration file.

For instance create a logging configuration file as documented in the
logging module

  >>> import tempfile
  >>> logging_fh = tempfile.NamedTemporaryFile()
  >>> logging_fh.write("""
  ... [loggers]
  ... keys=root,metaconfig
  ...
  ... [handlers]
  ... keys=hand01
  ... 
  ... [formatters]
  ... keys=form01
  ... 
  ... # No catch-all logging
  ... [logger_root]
  ... handlers=
  ... 
  ... [logger_metaconfig]
  ... qualname=metaconfig
  ... level=DEBUG
  ... handlers=hand01
  ... 
  ... [handler_hand01]
  ... class=StreamHandler
  ... args=(sys.stdout, )
  ... formatter=form01
  ... 
  ... [formatter_form01]
  ... format=[%(levelname)s] %(name)s: %(message)s
  ... """)
  >>> logging_fh.flush()

Now reference the logging file in metaconfig.conf.

  >>> metaconfig.reset()
  >>> metaconfig.init_from_string("""
  ... [metaconfig]
  ... logging = %s
  ... configs = foo
  ...
  ... [foo:bar]
  ... a = 42
  ... b = baz
  ... """ % logging_fh.name) # doctest:+ELLIPSIS
  [INFO] metaconfig.mconf: Logging configuration initialised from /tmp/...
  [INFO] metaconfig.mconf: Config foo added
  >>> conf = metaconfig.get_config('foo')
  [DEBUG] metaconfig.mconf: Requested config foo, inherit=True
  [DEBUG] metaconfig.mconf: Looking for config foo
  [DEBUG] metaconfig.mconf: Selected config foo

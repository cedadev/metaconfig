Using Metaconfig with Python Frameworks
=======================================

Metaconfig is designed to be framework-agnostic and is particularly
suited when you want to develop code that will be used in the context
of multiple frameworks.  Typically each framework includes it's own
configuration system so metaconfig includes some hooks to integrate
with these systems.


Metaconfig with Python Paste
----------------------------

Python Paste and WSGI frameworks that build upon it such as Pylons are
initiated from a single config file.  You can refer to a metaconfig
file by wrapping your WSGI application in the metaconfig app filter.

First some preliminary imports

  >>> import metaconfig
  >>> import tempfile
  >>> from paste.deploy import loadapp
  >>> metaconfig.reset()

Create the metaconfig file that will be referenced from the paste deploy config.

  >>> mconf_fh = tempfile.NamedTemporaryFile()
  >>> mconf_fh.write("""
  ... [metaconfig]
  ... configs = foo
  ...
  ... [foo:bar2]
  ... a = 42
  ... b = baz
  ... """)
  >>> mconf_fh.flush()

We can refer to this metaconfig file using a paste filter that takes
the single option "include".  The filter simply returns the unwrapped
wsgi application object without doing any other manipulation.

  >>> pconf_fh = tempfile.NamedTemporaryFile()
  >>> pconf_fh.write("""
  ... [server:main]
  ... user = egg:Paste#http
  ... host = 127.0.0.1
  ... port = 8001
  ...
  ... [app:main]
  ... use = egg:Paste#urlmap
  ... filter-with = mconf-filter
  ...
  ... [filter:mconf-filter]
  ... use = egg:metaconfig
  ... include = %s
  ... """ % mconf_fh.name)
  >>> pconf_fh.flush()
  >>> wsgi_app = loadapp('config:%s' % pconf_fh.name)

Verify the metaconfig is in place

  >>> config = metaconfig.get_config('foo')
  >>> config.getint('bar2', 'a')
  42
  >>> print config.get('bar2', 'b')
  baz

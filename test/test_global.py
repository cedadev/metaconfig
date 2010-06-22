
import tempfile
import os

from test_metaconfig import _make_test_config
from metaconfig import load_argv, get_config, clear


def setup():
    global config_file

    fd, config_file = tempfile.mkstemp()
    conf = _make_test_config(x='1')
    fh = os.fdopen(fd, 'w')
    conf.write(fh)
    fh.close()

def teardown():
    clear()
    os.remove(config_file)

def test_1():
    argv = ['foo', '--config=p1:%s' % config_file, 'a', 'b']
    load_argv(argv)

    assert argv == ['foo', 'a', 'b']

    conf = get_config('p1')
    assert conf.get('bar', 'x') == '1'

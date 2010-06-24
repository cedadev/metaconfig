
import tempfile
import os

from test_metaconfig import _make_test_config
from metaconfig import get_config, clear


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


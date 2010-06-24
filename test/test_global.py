# BSD Licence
# Copyright (c) 2010, Science & Technology Facilities Council (STFC)
# All rights reserved.
#
# See the LICENSE file in the source distribution of this software for
# the full license text.


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


# Copyright 2016 MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import unittest

import pymongo

from pymodm.connection import connect


PY3 = sys.version_info[0] == 3

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')

CLIENT = pymongo.MongoClient(MONGO_URI)
DB = CLIENT.odm_test

# Get the version of MongoDB.
server_info = pymongo.MongoClient(MONGO_URI).server_info()
MONGO_VERSION = tuple(server_info.get('versionArray', []))


INVALID_MONGO_NAMES = ['$dollar', 'has.dot', 'null\x00character']
VALID_MONGO_NAMES = ['', 'dollar$', 'forty-two']


def connect_to_test_DB(alias=None):
    if alias is None:
        connect(f'{MONGO_URI}/{DB.name}')
    else:
        connect(f'{MONGO_URI}/{DB.name}', alias=alias)


connect_to_test_DB()


class ODMTestCase(unittest.TestCase):

    def tearDown(self):
        CLIENT.drop_database(DB.name)

    if not PY3:
        # assertRaisesRegexp is deprecated in Python 3 but is all we have in
        # Python 2.
        def assertRaisesRegex(self, *args, **kwargs):
            return self.assertRaisesRegexp(*args, **kwargs)

    def assertEqualsModel(self, expected, model_instance):
        """Assert that a Model instance equals the expected document."""
        actual = model_instance.to_son()
        actual.pop('_cls', None)
        self.assertEqual(expected, actual)

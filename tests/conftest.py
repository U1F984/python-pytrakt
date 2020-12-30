# -*- coding: utf-8 -*-
import json
import os
import pytest
import trakt
from copy import deepcopy

MOCK_DATA_DIR = os.path.abspath('tests/mock_data')


MOCK_DATA_FILES = [
    os.path.join(MOCK_DATA_DIR, 'calendars.json'),
    os.path.join(MOCK_DATA_DIR, 'comments.json'),
    os.path.join(MOCK_DATA_DIR, 'genres.json'),
    os.path.join(MOCK_DATA_DIR, 'movies.json'),
    os.path.join(MOCK_DATA_DIR, 'people.json'),
    os.path.join(MOCK_DATA_DIR, 'recommendations.json'),
    os.path.join(MOCK_DATA_DIR, 'scrobble.json'),
    os.path.join(MOCK_DATA_DIR, 'search.json'),
    os.path.join(MOCK_DATA_DIR, 'shows.json'),
    os.path.join(MOCK_DATA_DIR, 'seasons.json'),
    os.path.join(MOCK_DATA_DIR, 'episodes.json'),
    os.path.join(MOCK_DATA_DIR, 'sync.json'),
    os.path.join(MOCK_DATA_DIR, 'users.json'),
]


class MockCore(trakt.core.Core):
    def __init__(self, *args, **kwargs):
        super(MockCore, self).__init__(*args, **kwargs)
        self.mock_data = {}
        for mock_file in MOCK_DATA_FILES:
            with open(mock_file, encoding='utf-8') as f:
                self.mock_data.update(json.load(f))

    def _handle_request(self, method, url, data=None):
        uri = url[len(trakt.core.BASE_URL):]
        if uri.startswith('/'):
            uri = uri[1:]
        # use a deepcopy of the mocked data to ensure clean responses on every
        # request. this prevents rewrites to JSON responses from persisting
        method_responses = deepcopy(self.mock_data).get(uri, {})
        return method_responses.get(method.upper())


"""Override utility functions from trakt.core to use an underlying MockCore
instance
"""
trakt.core.CORE = MockCore()
trakt.core.get = trakt.core.CORE.get
trakt.core.post = trakt.core.CORE.post
trakt.core.delete = trakt.core.CORE.delete
trakt.core.put = trakt.core.CORE.put
trakt.core.CLIENT_ID = 'FOO'
trakt.core.CLIENT_SECRET = 'BAR'

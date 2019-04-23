'''
Searching certificates from as many sources as possible.
'''
import os
import json
from http import HTTPStatus

import unittest
from unittest import mock

from cryptography.x509.oid import NameOID
from crt.search import CertificateSearch, SUPPORTED_SITES


def mock_crtsh(mock_content_path):
    '''
    Mock the JSON response from crt.sh.
    '''
    with open(mock_content_path) as fhandle:
        return fhandle.read().encode()


def mock_get(*args, **kwargs): # pylint: disable=unused-argument
    '''
    Mock the HTTP response instead of trying to get it from external source.
    '''
    class MockResponse: # pylint: disable=missing-docstring
        def __init__(self, content, status_code):
            self.content = content
            self.status_code = status_code

        def ok(self): # pylint: disable=invalid-name
            return self.status_code == HTTPStatus.OK

        def json(self):
            return json.loads(self.content)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    mock_dispatcher = {
        'https://crt.sh/?q=github.com&output=json&exclude=': mock_crtsh('{}/mock/crt.sh_json'.format(dir_path)),
        'https://crt.sh/?d=560083457': mock_crtsh('{}/mock/crt.sh_cert'.format(dir_path)),
    }

    if args[0] not in mock_dispatcher:
        return MockResponse(None, HTTPStatus.NOT_FOUND)

    return MockResponse(mock_dispatcher[args[0]], HTTPStatus.OK)


class SearchTest(unittest.TestCase):
    '''
    Test querying the certificates from various sources.
    '''
    def setUp(self):
        '''
        Setup the client to query all these supported sites.
        '''
        self.engines = {site: CertificateSearch(site=site) for site in SUPPORTED_SITES}

    @mock.patch('requests.get', side_effect=mock_get)
    def test_search(self, _):
        '''
        Looking for some certificates. Note that this test requires network
        connection to remote sites.
        '''
        cases = [
            {
                'query': 'github.com',
                'description': 'Query the certificates of a valid domain',

                'expected': {
                    'common_name': 'github.com',
                    'country_name': 'US',
                    'organization_name': 'GitHub',
                },
            },
        ]

        for _, engine in self.engines.items():
            for case in cases:
                got = [r for r in engine.search(case['query'])]

                # Sort by their expiration time
                got.sort(key=lambda x: x.not_after, reverse=True)

                if case['expected']:
                    self.assertTrue(len(got), case['description'])

                # Just download an check the latest record
                record = got[0]
                pem = record.pem

                self.assertIsNotNone(pem, case['description'])

                common_name = pem.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
                self.assertRegex(common_name, case['expected']['common_name'])

                country_name = pem.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value
                self.assertEqual(country_name, case['expected']['country_name'])

                organization_name = pem.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
                self.assertRegex(organization_name, case['expected']['organization_name'])

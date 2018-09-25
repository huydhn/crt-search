'''
Searching certificates from as many sources as possible.
'''
import unittest

from cryptography.x509.oid import NameOID
from crt.search import CertificateSearch, SUPPORTED_SITES


class SearchTest(unittest.TestCase):
    '''
    Test querying the certificates from various sources.
    '''
    def setUp(self):
        '''
        Setup the client to query all these supported sites.
        '''
        self.engines = {site: CertificateSearch(site=site) for site in SUPPORTED_SITES}

    def test_search(self):
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

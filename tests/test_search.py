'''
Searching certificates from as many sources as possible.
'''
import unittest
from crt.search import CertificateSearch, SUPPORTED_SITES


class SearchTest(unittest.TestCase):
    '''
    Test querying the certificates from various sources.
    '''
    def setUp(self):
        '''
        Setup the client to query all these supported sites.
        '''
        self.engines = [(site, CertificateSearch(site=site)) for site in SUPPORTED_SITES]

    def test_search(self):
        '''
        Looking for some certificates.
        '''
        cases = [
            {
                'query': 'github.com',
                'description': 'Query a valid domain'
            },
        ]

        for _, engine in self.engines.items():
            for case in cases:
                for rec in engine.search(case['query']):
                    self.assertTrue(rec.not_before, case['description'])

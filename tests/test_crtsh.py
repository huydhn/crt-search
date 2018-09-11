'''
Test crt.sh
'''

try:
    import unittest2 as unittest
# pylint: disable=bare-except
except:
    import unittest

from crt.search import CertificateSearch


class SiteTest(unittest.TestCase):
    '''
    Test querying crt.sh in various ways.
    '''
    def setUp(self):
        '''
        Setup the client to query crt.sh.
        '''
        self.engine = CertificateSearch(site='crt.sh')

    def test_normal_query(self):
        '''
        Send a query search query to crt.sh.
        '''
        cases = [
            {
                'query': 'github.com',
                'description': 'Query a valid domain'
            },
        ]

        for case in cases:
            got = [r for r in self.engine.search(case['query'])]

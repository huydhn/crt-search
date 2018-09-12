'''
Test querying various kinds of data from crt.sh.
'''
import random
import unittest
from crt.sites.crtsh import Engine


class SiteTest(unittest.TestCase):
    '''
    Test crt.sh specifically.
    '''
    def test_search(self):
        '''
        Looking for some certificates from crt.sh.
        '''
        cases = [
            {
                'query': 'github.com',
                'description': 'Query certificates of a valid domain'
            },
        ]

        for case in cases:
            got = [r for r in Engine.search(case['query'])]

            for rec in got:
                self.assertTrue(rec.not_before, case['description'])

            rec = random.choice(got)

            pem = Engine.get(rec.cert_id)
            self.assertIsNotNone(pem, case['description'])

            rec.pem = pem
            # pylint: disable=protected-access
            self.assertIsNotNone(rec._decoded_pem, case['description'])

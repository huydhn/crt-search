'''
Test querying various kinds of data from crt.sh.
'''
import os
import unittest

from cryptography.x509.oid import NameOID, ExtensionOID
from cryptography.x509.general_name import DNSName

from crt.sites.crtsh import decode_pem


class CertificateTest(unittest.TestCase):
    '''
    Test the way a certificate is handled internally.
    '''
    def test_parse(self):
        '''
        Parse some sample certificates.
        '''
        cases = [
            {
                'pem': 'samples/github.crt',
                'description': 'Parse a valid certificate',

                'expected': {
                    'common_name': '*.github.com',
                    'country_name': 'US',
                    'locality_name': 'San Francisco',
                    'organization_name': 'GitHub, Inc.',
                    'state_name': 'California',
                    'san_names': [
                        '*.github.com',
                        'github.com',
                    ],
                },
            },
        ]

        current_dir = os.path.dirname(os.path.realpath(__file__))

        for case in cases:
            with open(os.path.join(current_dir, case['pem'])) as fhandle:
                content = fhandle.read()

            pem = decode_pem(content.encode())
            self.assertIsNotNone(pem, case['description'])

            common_name = pem.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
            self.assertEqual(common_name, case['expected']['common_name'])

            country_name = pem.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value
            self.assertEqual(country_name, case['expected']['country_name'])

            locality_name = pem.subject.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value
            self.assertEqual(locality_name, case['expected']['locality_name'])

            organization_name = pem.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
            self.assertEqual(organization_name, case['expected']['organization_name'])

            state_name = pem.subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value
            self.assertEqual(state_name, case['expected']['state_name'])

            san = pem.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
            san_names = san.value.get_values_for_type(DNSName)

            self.assertListEqual(san_names, case['expected']['san_names'])

'''
Query crt.sh for the domain certificates. This site monitors the certificate
logs from various source, e.g. Google, Cloudflare, DigiCert and makes the log
searchable to the public.
'''
import json
import re

from datetime import datetime
import requests

from cryptography import x509
from cryptography.hazmat.backends import default_backend


def decode_pem(pem):
    '''
    Decode the x509 certificate and extract all the fields.
    '''
    return x509.load_pem_x509_certificate(pem, default_backend())


# pylint: disable=too-many-instance-attributes,invalid-name
class Certificate():
    '''
    A X509 certificate from crt.sh.
    '''
    def __init__(self):
        '''
        Initialize an empty certificate.
        '''
        self._id = None
        self._issuer = None
        self._not_before = 0
        self._not_after = 0

        self._pem = None

    @property
    def id(self):
        '''
        Just return the ID from crt.sh.
        '''
        return self._id

    @id.setter
    def id(self, certificate_id):
        '''
        This ID can be used to download the actual certificate later on.
        '''
        self._id = certificate_id

    @property
    def issuer(self):
        '''
        Just return the issuer from crt.sh.
        '''
        return self._issuer

    @issuer.setter
    def issuer(self, issuer):
        '''
        The issuer from crt.sh. It will need to be parsed.
        '''
        self._issuer = issuer

    @property
    def not_before(self):
        '''
        Just return the epoch timestamps from crt.sh.
        '''
        return self._not_before

    @not_before.setter
    def not_before(self, not_before):
        '''
        The epoch timestamps from crt.sh.
        '''
        self._not_before = not_before

    @property
    def not_after(self):
        '''
        Just return the epoch timestamps from crt.sh.
        '''
        return self._not_after

    @not_after.setter
    def not_after(self, not_after):
        '''
        The epoch timestamps from crt.sh.
        '''
        self._not_after = not_after

    @property
    def pem(self):
        '''
        Just return the raw certificate.
        '''
        if self._pem:
            return self._pem

        # Download the PEM ceritificate, may be the downloaded content
        # will need to be verified somehow
        content = Engine.get(self.id)

        if not content:
            return None

        self._pem = decode_pem(content)
        return self._pem


class Engine():
    '''
    This is an unofficial scraper of crt.sh till there is an official API.
    '''
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/60.0'

    # This is how crt.sh accepts a search query
    CRTSH_SEARCH = 'https://crt.sh/?q={}&output=json&exclude={}'
    # and this is how to download the certificate
    CRTSH_DOWNLOAD = 'https://crt.sh/?d={}'

    @staticmethod
    def search(domain, exclude_expired=False):
        '''
        Query the certificate log from crt.sh and return the search result. If
        excluded_expired flag is set, only active certificates are returns.
        '''
        if not domain:
            return None

        # crt.sh has the option to exlude all expired records
        expired = 'expired' if exclude_expired else ''

        result = requests.get(Engine.CRTSH_SEARCH.format(domain, expired),
                              headers={'User-Agent': Engine.USER_AGENT})

        if result.ok:
            # The site returns broken JSON so we need to fix it
            content = result.content.decode('utf-8')
            # by adding comma separator
            content = re.sub(r'}\s*{', '},{', content)
            # and turning it in to a JSON array
            content = '[{}]'.format(content)

            for record in json.loads(content):
                # The record from crt.sh has the following format:
                #
                # {
                #   'issuer_ca_id': 1397,
                #   'issuer_name': 'C=C, O=O, OU=OU, CN=CN',
                #   'name_value': 'github.com',
                #   'min_cert_id': 560083457,
                #   'min_entry_timestamp': '2018-06-29T14:20:38.527',
                #   'not_before': '2018-06-27T00:00:00',
                #   'not_after': '2020-06-20T12:00:00'
                # }
                #
                crt = Certificate()
                # Set all the available data from crt.sh. Note that the certificate
                # itself can be downloaded later
                crt.id = record['min_cert_id']
                crt.issuer = record['issuer_name']

                # Need to convert the timestamps into epoch
                tmp = datetime.strptime(record['not_before'], '%Y-%m-%dT%H:%M:%S').timestamp()
                crt.not_before = int(tmp)

                tmp = datetime.strptime(record['not_after'], '%Y-%m-%dT%H:%M:%S').timestamp()
                crt.not_after = int(tmp)

                yield crt

        return None

    @staticmethod
    def get(certificate_id):
        '''
        Download the cert with the provided ID.
        '''
        if not certificate_id:
            return None

        result = requests.get(Engine.CRTSH_DOWNLOAD.format(certificate_id),
                              headers={'User-Agent': Engine.USER_AGENT})

        if result.ok:
            return result.content

        return None

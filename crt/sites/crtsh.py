'''
Query crt.sh for the domain certificates. This site monitors the certificate
logs from various source, e.g. Google, Cloudflare, DigiCert and makes the log
searchable to the public.
'''
import json
import re
import requests


# pylint: disable=too-few-public-methods
class Engine():
    '''
    This is an unofficial scraper of crt.sh till there is an official API.
    '''
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/60.0'

    # This is how crt.sh accepts a search query
    CRTSH_URL = 'https://crt.sh/?q={}&output=json'

    # pylint: disable=no-self-use
    def search(self, domain):
        '''
        Query the certificate log from crt.sh.
        '''
        if not domain:
            return None

        result = requests.get(Engine.CRTSH_URL.format(domain),
                              headers={'User-Agent': Engine.USER_AGENT})

        if result.ok:
            # The site returns broken JSON so we need to fix it
            content = result.content.decode('utf-8')
            # by adding comma separator
            content = re.sub(r'}\s*{', '},{', content)
            # and turning it in to a JSON array
            content = '[{}]'.format(content)

            for record in json.loads(content):
                yield record

        return None

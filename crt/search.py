'''
A generic module to query information from the certificate transparency log.
More details can be found at https://www.certificate-transparency.org/.
'''
import importlib

SUPPORTED_SITES = {
    'crt.sh': lambda: importlib.import_module('.sites.crtsh', 'crt')
}


# pylint: disable=too-few-public-methods
class CertificateSearch():
    '''
    This class is a wrapper that queries issued HTTPS certificates of domains
    from various sources. It currently supports only crt.sh.
    '''

    def __init__(self, site='crt.sh'):
        '''
        Initialize the search engine.

        site: The domain where the certificate data comes from, e.g. crt.sh.
            The certificate log is being monitored there and made available to
            the public.
        '''
        if site not in SUPPORTED_SITES:
            msg = '{} is not supported. Valid sites are {}'.format(site, SUPPORTED_SITES)
            raise NotImplementedError(msg)

        self.site = site
        self._load_module()

    def _load_module(self):
        '''
        Dynamically load the required module that contains the implementation
        on how to query the target site.
        '''
        self.module = SUPPORTED_SITES[self.site]()

    def search(self, domain):
        '''
        Look for the certificates of a specific domain.
        '''
        return self.module.Engine.search(domain)

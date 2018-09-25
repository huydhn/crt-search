Certificate Search
------------------

[![Build Status](https://travis-ci.org/huydhn/crt-search.svg?branch=master)](https://travis-ci.org/huydhn/crt-search)
[![codecov.io](https://codecov.io/gh/huydhn/crt-search/master.svg)](http://codecov.io/gh/huydhn/crt-search?branch=master)

An unofficial wrapper to query [crt.sh](https://crt.sh/).

Installation
------------

The package can be installed from
[PyPI](https://pypi.org/project/crt-search)

```
pip install certificate-search
```

Usage
-----

```python
import json

from cryptography.x509.oid import NameOID, ExtensionOID
from cryptography.x509.general_name import DNSName

from crt.search import CertificateSearch, SUPPORTED_SITES

# Print the list of all supported sites
print(json.dumps(SUPPORTED_SITES))

engines = CertificateSearch()

domains = [
    'github.com',
    'facebook.com',
]

for domain in domains:
    for cert in engine.search(domain=domain):
        not_before = cert.not_before
        not_after = cert.not_after

        pem = cert.pem
        # An x509 certificate
        common_name = pem.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        country_name = pem.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value
        organization_name = pem.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value

        # All SAN records
        san = pem.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        san_names = san.value.get_values_for_type(DNSName)
```

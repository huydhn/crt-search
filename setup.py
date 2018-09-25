'''
Standard Python setup script.
'''

from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='certificate-search',
    version='0.1',
    description='Certificate Transparency search',
    url='https://github.com/huydhn/crt-search',
    author='Huy Do',
    author_email='huydhn@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests', 'cryptography'],
    tests_require=['unittest2', 'coverage', 'nose', 'pytest-pep8', 'codecov'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

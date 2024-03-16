import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from codecs import open

with open('sharepoint4py/version.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(
    name='sharepoint4py',
    version=version,
    description='Python SharePoint Library',
    long_description=open('README.rst').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dianasoares/sharepoint4py',
    author='Diana Soares',
    author_email='soaresd32@hotmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Office/Business',
    ],
    keywords=['SharePoint'],
    packages=['sharepoint4py'],
    install_requires=['lxml', 'requests', 'requests-ntlm', 'requests-toolbelt'],
)

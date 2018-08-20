import sys
from setuptools import setup, find_packages
from setuptools_behave import behave_test

requires = [
    'requests>=2.18.4',
    'tqdm>=3.8.0',
    'urllib3>=1.22'
]

if sys.version_info < (3, 2):
    requires.append('futures==2.2')
    requires.append('configparser')

setup(
    name='instagram-scraper',
    version='1.5.38',
    description=("instagram-scraper is a command-line application written in Python"
                 " that scrapes and downloads an instagram user\'s photos and videos. Use responsibly."),
    url='https://github.com/rarcega/instagram-scraper',
    download_url='https://github.com/rarcega/instagram-scraper/tarball/1.5.38',
    author='Richard Arcega',
    author_email='hello@richardarcega.com',
    license='Public domain',
    packages=find_packages(exclude=['tests']),
    install_requires=requires,
    entry_points={
        'console_scripts': ['instagram-scraper=instagram_scraper.app:main'],
    },
    tests_require=[
        'behave>=1.2.6',
        'mock>=2.0.0',
        'pyhamcrest>=1.9.0',
        'six>=1.11'
    ],
    cmdclass={
        'behave_test': behave_test,
    },
    zip_safe=False,
    keywords=['instagram', 'scraper', 'download', 'media', 'photos', 'videos']
)

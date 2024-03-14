from setuptools import setup, find_packages

setup(
    name='pygeckodexapi',
    version='0.1.2',
    packages=find_packages(),
    install_requires=['requests'],
    url='https://github.com/labfunny/py-gecko-dex-api',
    license='MIT',
    author='Max',
    description='Unofficial SDK for working with the GeckoTerminal API',
    classifiers = ['Programming Language :: Python :: 3.6']
)
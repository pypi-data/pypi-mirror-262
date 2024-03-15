from setuptools import find_packages, setup

VERSION = '0.1.4'

setup(
    name='ludfor-utils',
    packages=find_packages(),
    version=VERSION,
    description='Funções para utilização em Scripts',
    author='Ludfor Desenvolvimento',
    install_requires=['psycopg2', 'smtplib', 'datetime', 'email', 'typing', 'email', 'io']
)
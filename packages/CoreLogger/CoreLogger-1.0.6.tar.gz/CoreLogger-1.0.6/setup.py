from setuptools import setup, find_packages

setup(

    name='CoreLogger',

    version='1.0.6',
    
    author='Ahmet Kıpkıp',

    author_email='ahmtkipkip@gmail.com',

    description='A simple logger for sending logs to a Loki server for Internal use at IZBB.',
    install_requires=["python-logging-loki"],
    packages=find_packages(),
)
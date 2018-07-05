from setuptools import setup, find_packages
#import os

#ROOT = os.path.dirname(os.path.realpath(__file__))

setup(
    name = 'tgram',
    version = '0.0.1',
    description = 'Set of utils to build telegram python bots',
    #long_description = open(os.path.join(ROOT, 'README.rst')).read(),
    author = 'Gregory Petukhov',
    author_email = 'lorien@lorien.name',
    packages = find_packages(exclude=['test']),
    license = "MIT",
    #install_requires = ['six'],
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
)

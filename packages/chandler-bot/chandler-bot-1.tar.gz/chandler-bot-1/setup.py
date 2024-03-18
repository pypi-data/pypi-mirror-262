from setuptools import setup
from setuptools import setup, find_namespace_packages

with open("README.md", "r") as f:
    logn_desc = f.read()
setup(
    name='chandler-bot',
    version='1',
    description='You personal assistant',
    long_description=logn_desc,
    url='https://github.com/MKuzich/bot',
    author='MKuzich',
    author_email='chandler-bot@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['markdown'],
    entry_points={'console_scripts': ['chandler = main:main']}
)

from setuptools import setup

setup(
    name = 'nplot',
    version = '0.2',
    author = 'Nathan Dunfield',
    author_email = 'nathan@dunfield.info',
    description = "Nathan's personal plotting tools",
    license = 'GPLv2+',
    keywords = 'plotting',
    packages=['nplot'],
    package_dir = {'nplot':'src'},
    zip_safe = False,
    install_requires = ['matplotlib>=1.5', 'pandas']
)

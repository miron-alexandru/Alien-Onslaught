from setuptools import setup, find_packages

setup(
    name='Alien-Onslaught',
    version='3.1',
    author='Miron Alexandru',
    author_email='quality_xqs@yahoo.com',
    description='Alien Onslaught, an action-packed game that will test your shooting skills and reflexes',
    packages=find_packages(exclude=['src.test_alien.py']),
    package_data={
        'game_assets': ['images/**/*', 'sounds/**/*'],
    },
    install_requires=[
        'pygame',
        'dataclasses'
    ],
    classifiers=[
        'Development Status :: - Production',
        'Intended Audience :: Developers, Users',
        'License :: MIT License ',
        'Programming Language :: Python :: 3.11',
    ],
)

from setuptools import setup, find_packages

setup(
    name="alien onslaught",
    version="3.3",
    author="Miron Alexandru",
    author_email="quality_xqs@yahoo.com",
    description="Alien Onslaught: An action-packed arcade space shooter game.",
    packages=find_packages(),
    package_data={
        "game_assets": ["images/**/*", "sounds/**/*"],
    },
    install_requires=["pygame"],
    classifiers=[
        "Development Status :: - Production",
        "Intended Audience :: Developers, Users",
        "License :: MIT License ",
        "Programming Language :: Python :: 3.11",
    ],
)

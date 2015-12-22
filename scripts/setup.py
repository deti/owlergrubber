import os
from setuptools import setup, find_packages

install_requires = [
    "requests",
    "metayaml",
    "attrdict",
    "sqlitedict",
    "selenium",
]

owlergrubber_dependencies = [
    "PyYAML",
]
install_requires.extend(owlergrubber_dependencies)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

packages = find_packages(".")
setup(
    name="owlergrubber",
    version="0.0.1",
    author="deti",
    author_email="detijazzz@gmail.com",
    description="Owler.com grubber",
    license="Public",
    url="",
    packages=packages,
    package_data={
        '': ['*.sh', '*.ini', '*.pem', '*.txt'],
        'configs': ['*.yaml']},
    install_requires=install_requires,
    entry_points={
        'console_scripts':
        [
            'owlergrubber = owlergrubber:main',
            'owlergrubber.py = owlergrubber:main',
            'collect_profiles.py = owlergrubber:collect_profiles',
            'search_for_words.py = owlergrubber:search_for_words',
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "License :: Other/Proprietary License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
        "Topic :: Multimedia :: Video :: Display",
    ],
)

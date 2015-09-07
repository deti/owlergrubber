import os
from setuptools import setup, find_packages

install_requires = [
    "requests",
    "metayaml",
    "attrdict",
    "sqlitedict",
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
    version="0.0.1",  # TODO read from version
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

from setuptools import setup, find_packages


setup(
    name="fogLedgerIndy",
    version="1.0.0",
    description='Plugin to build DLTs Indy in Fogbed.',
    long_description='Plugin to build DLT Indy in Fogbed\
        The FogLedger is a plugin for [Fogbed](https://github.com/larsid/fogbed). It allows you to emulate a fog network with distributed ledgers. \
        Currently, FogLedger has suport for Hyperledger Indy. It is a distributed ledger, purpose-built for decentralized identity. \
        It provides tools, libraries, and reusable components for creating and using independent digital identities rooted on blockchains or other distributed ledgers so that they are interoperable across administrative domains, applications, and any other silo. \
        Indy is interoperable with other blockchains or can be used standalone powering the decentralization of identity. \
        With FogLedger you can create a network of nodes running Hyperledger Indy. A emulation can have multiple networks of nodes running different distributed ledgers. \
        FogLedger is a plugin for Fogbed, so you can use all the features of Fogbed to emulate your fog network, such as in the Figure below.',
    keywords=['networking', 'emulator', 'protocol', 'Internet', 'dlt', 'indy', 'fog'],
    url='https://github.com/MatheusNascimentoti99/FogLedger-Indy/tree/v2.0.0',
    author='Matheus Nascimento',
    author_email='matheusnascimentoti99@gmail.com',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Emulators"

    ],
    install_requires = [
        'numpy>=1.24.2',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    package_data={'fogledgerIndy': ['iota/data/*.sh', 'iota/data/*.json']}
)

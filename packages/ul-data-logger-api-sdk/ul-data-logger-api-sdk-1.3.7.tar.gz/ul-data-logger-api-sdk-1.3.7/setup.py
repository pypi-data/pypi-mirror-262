import sys
from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if sys.argv:
    if 'broker_sdk' in set(sys.argv):
        sys.argv.remove("broker_sdk")
        setup(
            name='ul-data-logger-sdk',
            version='2.1.10',
            description='Data logger sdk',
            author='Unic-lab',
            long_description=long_description,
            long_description_content_type="text/markdown",
            packages=find_packages(include=['data_logger_sdk*']),
            include_package_data=True,
            package_data={
                '': ['*.yml', 'py.typed'],
                'data_logger_sdk': ['py.typed'],
            },
            license="MIT",
            classifiers=[
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Operating System :: OS Independent",
            ],
            platforms='any',
            install_requires=[
                "unipipeline>=1.4.5",
                # "ul-data-aggregator-sdk==8.12.0,
                # "ul-py-tool==1.15.42",
                # "ul-api-utils==7.4.6",
                # "ul-db-utils==2.11.0",
                # "ul-data-gateway-sdk==0.4.5",
            ],
        )
    elif 'api_sdk' in set(sys.argv):
        sys.argv.remove("api_sdk")
        setup(
            name='ul-data-logger-api-sdk',
            version='1.3.7',
            description='Data logger API sdk',
            author='Unic-lab',
            long_description=long_description,
            long_description_content_type="text/markdown",
            packages=find_packages(include=['data_logger_api_sdk*']),
            include_package_data=True,
            package_data={
                '': ['*.yml', 'py.typed'],
                'data_logger_api_sdk': ['py.typed'],
            },
            license="MIT",
            classifiers=[
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Programming Language :: Python",
                "Programming Language :: Python :: 3.6",
                "Programming Language :: Python :: 3.7",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Operating System :: OS Independent",
            ],
            platforms='any',
            install_requires=[
                "unipipeline>=1.4.5",
                "tqdm==4.66.1",
                # "ul-data-aggregator-sdk>=8.13.2",
                # "ul-py-tool==1.15.42",
                # "ul-api-utils==7.7.1",
                # "ul-db-utils==3.2.3",
                # "ul-data-gateway-sdk==0.4.13",
            ],
        )

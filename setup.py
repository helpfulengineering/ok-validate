#!/usr/bin/env python
from setuptools import setup, find_packages

readme = open('README.md', encoding='utf-8').read()
license = open('LICENSE', encoding='utf-8').read()

setup(
    name='okv',
    version='0.0.1',
    description='A schema and validator for OK* YAML files.',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "okv": ["schemas/*.yaml"],
    },
    install_requires=['yamale'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['okv=okv.okv:main'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4'
    ]
)
# setup.py

from setuptools import setup, find_packages

setup(
    name='fastapi-error-logger',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'sqlalchemy'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    project_urls={
        'Source': 'https://github.com/omkardarves/fastapi-error-logger',
    },
    license='MIT',
)
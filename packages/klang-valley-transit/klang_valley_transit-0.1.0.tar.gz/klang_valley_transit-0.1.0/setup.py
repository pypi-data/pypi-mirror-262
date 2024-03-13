from setuptools import setup, find_packages
from os import environ
setup(
    name='klang_valley_transit',
    version='0.1.0',
    description='Graph, Graph Algorithm, and Klang Valley Transit Routing',
    author='Chin Yan',
    author_email='cy.python.91@gmail.com',
    license='MIT',
    packages= find_packages(), 
    package_data={'': ['**/*.json', '**/*.py','*.json', '*.py']},
    install_requires=[
        'numpy', 
        'pydantic', 
    ],
    scripts=['bin/test.py'],
    zip_safe=False,
    long_description=open("README.MD").read(),
    long_description_content_type="text/markdown",
)
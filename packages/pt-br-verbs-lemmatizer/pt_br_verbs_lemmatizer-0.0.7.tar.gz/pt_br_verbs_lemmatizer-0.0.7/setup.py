from setuptools import setup, find_packages
import os


with open(r'README.md','r',encoding='utf-8') as f:
    descricao_longa = f.read()

setup(
    name='pt_br_verbs_lemmatizer',
    version='0.0.7',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"pt_br_verbs_lemmatizer": ["*.msgpack"]},
    install_requires = ['msgpack==1.0.7'],
    description='Program designed to lemmatize the various verbal inflections present in the Brazilian Portuguese language quickly and efficiently.',
    long_description=descricao_longa,
    long_description_content_type="text/markdown",
    author='Igor Caetano de Souza',
    project_urls={
        "GitHub Repository":"https://github.com/IgorCaetano/portuguese_br_verbs_lemmatizer"
    },    
)
from setuptools import setup, find_packages

setup(
    name='dict-toolkit',
    version='0.0.4',
    packages=find_packages(),
    package_data={
        'dict_toolkit': ['data/dict/split/*.csv'],
    },
    include_package_data=True,
    install_requires=[],
)


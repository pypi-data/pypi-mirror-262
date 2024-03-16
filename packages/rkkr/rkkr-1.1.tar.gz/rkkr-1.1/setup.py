from setuptools import setup, find_packages

setup(
    name='rkkr',
    version='1.1',
    packages=find_packages(),
    install_requires=[

    ],
    entry_point={
        "console_scripts":[
            "rkkr = rkkr:welcome",
        ],
    }

)
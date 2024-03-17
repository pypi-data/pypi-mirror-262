from setuptools import setup, find_packages

setup(
    name='rkkr',
    version='2.1.2',
    packages=find_packages(),
    install_requires=[
        'keras',
        'keras-tuner',
        'pandas',
        'numpy',
        'scikit-learn',
        'plotly'
    ],
    entry_point={
        "console_scripts":[
            "rkkr = rkkr:welcome",
        ],
    },

)
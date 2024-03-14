# latex_generator/setup.py

from setuptools import setup, find_packages

setup(
    name='latex_generator',
    version='0.3',
    packages=find_packages(include=['latex_generator', 'latex_generator.*']),
    install_requires=["Pillow"],
    entry_points={
        'console_scripts': [
            'latex-generator=latex_generator.latex_generator:main',
        ],
    },
)

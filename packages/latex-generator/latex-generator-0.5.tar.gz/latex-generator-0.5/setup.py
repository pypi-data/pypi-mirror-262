# latex_generator/setup.py

from setuptools import setup, find_packages

setup(
    name="latex-generator",
    version="0.5",
    packages=find_packages(),
    install_requires=["Pillow"],
    entry_points={
        'console_scripts': [
            'latex-generator=latex_generator.latex_generator:main',
        ],
    },
)

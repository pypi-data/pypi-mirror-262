from setuptools import setup, find_packages

setup(
    name='lineagekit',
    version='0.0.2',
    description='A python library with genealogy methods',
    author='Simon Gravel, Andrii Serdiuk, César Miguel Valdez Córdova',
    author_email='simon.gravel@mcgill.ca',
    packages=find_packages(exclude=['validation']),
    install_requires=[
        'tskit>=0.5.6',
        'networkx>=3.2.1',
        'matplotlib>=3.8.3',
        'pytest>=8.0.2',
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
    ],
)

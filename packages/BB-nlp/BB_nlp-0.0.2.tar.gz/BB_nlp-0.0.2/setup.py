from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Tree Bank Map'

# Setting up
setup(
    name="BB_nlp",
    version=VERSION,
    author="Mohab",
    author_email="a.mohab148@gmail.com",
    description=DESCRIPTION,
    long_description="TempTemp",
    packages=find_packages(),
    install_requires=['nltk'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)

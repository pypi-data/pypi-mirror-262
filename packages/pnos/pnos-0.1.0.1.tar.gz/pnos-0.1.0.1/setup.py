from setuptools import setup, find_packages

VERSION = '0.1.0.1' 
DESCRIPTION = 'Niosem PnOS package library'
LONG_DESCRIPTION = 'Niosem PnOS Package imports and libraries - used for PnOS Dev and Rel builds'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="pnos", 
        version=VERSION,
        author="StNiosem",
        author_email="niosem@hldrive.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['network'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'Niosem PnOS', 'PnOS'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
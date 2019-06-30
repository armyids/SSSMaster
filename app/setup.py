#!/usr/bin/python


########## HERE IS THE INITIAL SECTION OF SETUP SF CLASS ##########
# Install program modules, packages and dependencies
# Before starting SF, user should fulfill the dependencies by running the script.
# Activate the script below if your Python have no needed modules (PyFiglet, NumPy, and Pandas).
# Here is a function to install python and the needed packages.
  
  # Installing PyFiglet, NumPy, and Pandas

  # It's recommended to rollback the version of pip3 using this command paste into your terminal
  # python3 -m pip install --user --upgrade pip==9.0.3

import pip
def install(package1, package2, package3, package4, package5):
    pip.main(['install', package1, package2, package3, package4, package5])

if __name__ == '__main__':
    install('pyfiglet','pandas','numpy','setuptools','wheel')
########## HERE IS THE LAST SECTION OF SETUP SF CLASS ##########
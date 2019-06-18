#!/usr/bin/python

# PROGRAM TITLE
  # Slope Stability Scanner

# PROGRAM DESCRIPTION
  # SSS is an open-source program that built to analyze the safety factor of a slope based on strength stress and shear stress.
  # This program has been tested and should work on almost all Python 3.6 compilers.

# IMPORT MODULE

import os
import pyfiglet
import csv
import numpy as np
import pandas as pd

# SHOW HEADER
  # Header is used for giving information about title and the version of the program.

pyfiglet.print_figlet("SSS",font="lean",justify="center")
pyfiglet.print_figlet("Slope Stability Scanner",font="digital",justify="center")
version = " Version 0.0.3 ";
print("{1:^75}".format(" ",version))
print(" ")

# PATHS

data_input = "input/"
data_output = "../output/"

  # Change working directory into "input" folder

os.chdir(data_input)

# INPUT DATA

  # Function to open file and save each column contents into dictionary

  # "var" is variable, "file" is your filename, while "n" is numbers of your columns plus 1

def open_myfile(var,file,n):
	with open(file, mode='r') as infile:
		var = {}
		reader = csv.reader(infile)
		next(reader, None)  # Skip the headers
		mydict = {rows[0]:(rows[1:n]) for rows in reader}
		var.update(mydict)
		return var

  # Open and read data of data_long_lat.csv and data_beta.csv

cpa = open_myfile("cphialpha","data_long_lat.csv",6)
b = open_myfile("beta","data_beta.csv",3)

  # Determine the constant number of specific weight (gamma) in kg/m3 or corresponding units

gamma = 1000

# PROCESS DATA

  # Build matrix structure to make calculation process easier

cpa_matrix = pd.DataFrame(cpa.values()) # Convert dictionary into Pandas data frame
cpab_matrix = cpa_matrix.rename({0: 'long', 1: 'lat', 2: 'c', 3: 'phi', 4: 'alpha'}, axis = 'columns') # Rename the spesific columns with certain names
b_matrix = pd.DataFrame(b.values()) # Create data frame using Pandas for beta matrix
cpab_matrix['beta'] = b_matrix # Insert beta matrix to data frame

    # Prefered to begin index at 1
n = 0
m = []
while n < len(cpab_matrix.index):
	n += 1
	m.append(n)
cpab_matrix.index = m

    # Prefered to round up / down to 4 decimal for longitude and latitude data

def fourdec_longlat(coor, coordination):
	coor = np.array(cpab_matrix[coordination].astype(float))
	cpab_matrix[coordination] = np.around(coor,4)

twoabbr_coor = ['lg', 'lt']
fourabbr_coor = ['long', 'lat']

for twoc, fourc in zip(twoabbr_coor, fourabbr_coor):
	fourdec_longlat(twoc, fourc)

  # Grid size calculation

    # The assumption here is longitude changes every 10 data

gz = (float(cpab_matrix['long'][1]) - float(cpab_matrix['long'][11])) * 111.12 # Unit is kilometer, should be converted to other units? waiting for sample data

  # Moving area calculation

    # Convert data frame into numpy array for alpha and beta

alpha = np.deg2rad(np.array(cpab_matrix['alpha']).astype(float))
beta = np.deg2rad(np.array(cpab_matrix['beta']).astype(float))

    # Estimate tangent for each alpha and beta also subtracted, save them into 'deg' variable

tan_alpha = np.tan(alpha)
tan_beta = np.tan(beta)
deg = tan_alpha - tan_beta

    # Estimate moving area of slope for each grid

A = 0.5 * gz**2 * deg

    # Submit the result of moving area into main data frame

cpab_matrix['moving_area'] = np.around(A, 2)

  # Soil weight calculation

W = A * gamma
    
    # Submit the result of soil weight into main data frame

cpab_matrix['soil_weight'] = np.around(W, 2)

  # Normal stress calculation 

cos_beta = np.cos(beta)

    # Estimate normal stress for each grid

z = (W * cos_beta) / A

    # Submit the result of normal stress into main data frame

cpab_matrix['normal_stress'] = np.around(z, 2)

  # Strength stress calculation 

    # Convert data frame into numpy array for c and phi

cohesive = np.array(cpab_matrix['c']).astype(float)
phi = np.deg2rad(np.array(cpab_matrix['phi']).astype(float))

    # Estimate tangent for phi and save them into 'tan_phi' variable

tan_phi = np.tan(phi)

    # Estimate strength stress of the slope for each grid

tr = cohesive + (z * tan_phi)

    # Submit the result of strength stress into main data frame

cpab_matrix['strength_stress'] = np.around(tr, 2)

  # Shear stress calculation 

    # Estimate sinus for beta and save them into 'sin_beta' variable

sin_beta = np.sin(beta)

    # Estimate shear stress of the slope for each grid

td = (W * sin_beta) / A

    # Submit the result of shear stress into main data frame

cpab_matrix['shear_stress'] = np.around(td, 2)

  # Safety factor calculation

sf = tr / td

    # Submit the result of shear stress into main data frame

cpab_matrix['safety_factor'] = np.around(sf, 2)

# OUTPUT DATA

print(cpab_matrix)
os.chdir(data_output)
cpab_matrix.to_csv("sss_output.csv", sep='\t')
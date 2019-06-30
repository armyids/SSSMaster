#!/usr/bin/python

# PROGRAM TITLE
  
  # Slope Stability Scanner

# PROGRAM DESCRIPTION
  
  # SSS is an open-source program that built to analyze the safety factor of a slope based on strength stress and shear stress.
  # This program has been tested and should work on almost all Python 3.6 compilers.

# IMPORT MODULE

import os # Operating System module for 'directory walking', 'directory list', 'directory change' and etc.
import pyfiglet # Optional package that used to print the header as the program title and program version.
import csv # Module to open csv files without using complex / complicated function.
import numpy as np # Python module to build numeric structure for matrix operation.
import pandas as pd # Module to build data frame.

# PATHS

data_input = "input/"
data_output = "output/"

# FLUSH OUTPUT FOLDER
  
  # Flush and clean up the contents of output folder to make sure there is no files inside

for dirpath, dirnames, filenames in os.walk(data_output):
    # Remove regular files and ignore directories
    for filename in filenames:
        os.unlink(os.path.join(dirpath, filename))

# SHOW HEADER

  # Header is used for giving information about title and the version of the program.

pyfiglet.print_figlet("SSS",font="lean",justify="center")
pyfiglet.print_figlet("Slope Stability Scanner",font="digital",justify="center")
version = " Version 0.1.1 ";
print("{1:^75}".format(" ",version))
print(" ")

# INPUT DATA

  # Change working directory into "input" folder

os.chdir(data_input)

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

    # Convert values of 'cpa' dictionary into Pandas data frame

cpa_matrix = pd.DataFrame(cpa.values())

    # Rename the headers with the certain names

cpa_matrix = cpa_matrix.rename({0: 'long', 1: 'lat', 2: 'c', 3: 'phi', 4: 'alpha'}, axis = 'columns')
beta_matrix = b.values()

    # Prefered to begin index of cpa_matrix at 1

n = 0
m = []
while n < len(cpa_matrix.index):
	n += 1
	m.append(n)
cpa_matrix.index = m

    # Function to convert data frame (longitude & latitude) into numpy array and round up / down to 4 decimals

def fourdec_longlat(coor, coordination):
	coor = np.array(cpa_matrix[coordination].astype(float))
	cpa_matrix[coordination] = np.around(coor,4)

twoabbr_coor = ['lg', 'lt']
fourabbr_coor = ['long', 'lat']

for twoc, fourc in zip(twoabbr_coor, fourabbr_coor):
	fourdec_longlat(twoc, fourc)

  # Grid size calculation

    # The assumption here is longitude changes every grid

gz = (float(cpa_matrix['long'][1]) - float(cpa_matrix['long'][2])) * 111.12 # Unit is kilometer, should be converted to other units? waiting for sample data

  # Moving area calculation

    # Convert alpha and beta data frame into numpy array

alpha = np.deg2rad(np.array(cpa_matrix['alpha']).astype(float))
betas = np.deg2rad(np.array(pd.DataFrame(beta_matrix)[0].astype(float)))

    # Estimate tangent for each alpha

tan_alpha = np.tan(alpha)

    # Estimate moving area of slope for each beta

MA = []
for beta in betas:
	A = 0.5 * gz**2 * (tan_alpha - np.tan(beta))
	MA.append(A)
MA = pd.DataFrame(MA)

  # Soil weight calculation

W = MA * gamma

  # Normal stress calculation 

    # Estimate cosinus for each beta

cos_b = np.cos(betas)

    # Estimate ormal stress

Z = []
for cos_beta, w, ma in zip(cos_b, np.array(W), np.array(MA)):
	np_cos_beta  = np.array(cos_beta)
	z = (w * np_cos_beta) / ma
	Z.append(z)

  # Strength stress calculation 

    # Convert data frame into numpy array for c and phi

cohesive = np.array(cpa_matrix['c']).astype(float)
phi = np.deg2rad(np.array(cpa_matrix['phi']).astype(float))

    # Estimate tangent for phi and save them into 'tan_phi' numpy array variable

tan_phi = np.array(np.tan(phi))

    # Estimate strength stress of the slope for each grid

TR = []
for z in Z:
	tr = cohesive + (z * tan_phi)
	TR.append(tr)

  # Shear stress calculation 

    # Estimate sinus for beta and save them into 'sin_beta' numpy array variable

sin_b = np.sin(betas)

    # Estimate shear stress of the slope for each grid

TD = []
for w, sin_beta, ma in zip(np.array(W), sin_b, np.array(MA)):
	np_sin_beta = np.array(sin_beta)
	td = (w * np_sin_beta) / ma
	TD.append(td)

  # Safety factor calculation

SF = []
for tr, td in zip(np.array(TR), np.array(TD)):
	sf = tr / td
	SF.append(sf)
print(100*SF)
# OUTPUT DATA

print("Calculation done!\nPlease check the output folder\n")
os.chdir("../"+data_output)
for sf,l,le in zip(SF, pd.DataFrame(beta_matrix)[0], range(1,len(betas)+1)):
	cpa_matrix["safety_factor"] = np.around(sf, 2)
	scpa_matrix = cpa_matrix.sort_values('safety_factor')
	scpa_matrix.to_csv((str(le)+"_"+"beta_"+str(l)+".csv"), sep=',', index = False)
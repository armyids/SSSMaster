import os

########## HERE IS THE INITIAL SECTION OF FLUSH OUPUT FOLDER CLASS ##########
# FLUSH OUTPUT FOLDER
  # Flush and clean up the contents of output folder to make sure there is no files inside

output_directory = 'output/'
for dirpath, dirnames, filenames in os.walk(output_directory):
    # Remove regular files and ignore directories
    for filename in filenames:
        os.unlink(os.path.join(dirpath, filename))
########## HERE IS THE LAST SECTION OF FLUSH OUPUT FOLDER CLASS ##########
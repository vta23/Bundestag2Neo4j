import dbutils
import glob, os


# Loading Data Module

# specify directory to read Drucksachen ( os.getcwd() for working directory)
directory = '/miniconda3/workingfolder/btdata/18testdata'



# specify file pattern (** for any)
filepattern = '*xml'

# specify if subfolders should be included (yes / no), and which pattern should be looked for (** for any)
subfolders = 'no'
subfolderpattern = 'drs*'


dbutils.loadDrucksachenFolder(directory, filepattern, subfolders, subfolderpattern)








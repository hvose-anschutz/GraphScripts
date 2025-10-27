#!/usr/bin/env python3

"""
This script generates a heatmap based on a provided .csv formatted dataset. This version of the script does NOT rely on the
GraphScripts file structure, and can be run as a standalone script. 

Required pip install libraries are seaborn pandas, and matplotlib.

Updated 10/7/2025
"""

# NECESSARY IMPORTS
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
import re
import math
import sys

#FUNCTION DEFINITION (you can ignore this for the most part)

def my_output_file(filename: str, plot_type: str ="Plot", extension: str="svg") -> str:
    """Creates a regex to rename the output file based on the original .csv file. The plot type adds the name of
       the plot to the filename, and the extension specifies what file format to save (svg, png, jpeg, or pdf)."""
    try:
        if extension in ["svg", "png", "pdf", "jpeg", "jpg"]:
            just_name = filename.split("/")
            new_name = re.sub(".csv$","_Image" + plot_type + "." + extension, just_name[::-1][0],1)
            return os.getcwd() + "/" + new_name
        else:
            return filename
    except AttributeError:
        print("ERROR: Could not process filename. Double check that passed filename object is a string.")
        sys.exit(1)

# SET BASIC THEME PARAMETERS
sns.set_theme()

# OPEN FILES AND GENERATE PATH NAMES
myCSV = "Data.csv"      # your data filename goes here (if your file is not in the same folder you MUST specify the whole path)
myOutput = my_output_file(myCSV, plot_type="HeatMap",extension="svg")   #generates the output filename automatically.

# READ IN THE DATA
DataSet = pd.read_csv(myCSV)       # reads in CSV as dataset

print(DataSet.columns.values)

# DATA PROCESSING (if your csv has all of your data in two columns)
# NOTE: You need to make sure "Well Positions" and "LogCopies" matches your columns names EXACTLY in order for this to work.
# This also assumes that your wells are labeled "A1", "B2", "C3", etc... (letter followed by number)
DataSet["row"] = DataSet["Well Positions"].str.extract("([A-Za-z]+)")
DataSet["column"] = DataSet["Well Positions"].str.extract("(\d+)").astype(int)

vmax_val = math.ceil(DataSet["LogCopies"].max())    #determine max colormap saturation value

heatmap_data = DataSet.pivot(index="row",columns="column",values="LogCopies")  #generate the "fixed" dataset used in plotting

# SET AESTHETICS
Pal = sns.light_palette("#bb334c", as_cmap=True) #Sets color palette to be in the range from White to a Saturated Color

# GENERATE THE HEATMAP
g = sns.heatmap(heatmap_data,
			cmap = Pal,       #Determines the colormap based on a provided palette (see above)
			vmin = 0,         #Sets the minimum value for the lowest saturation of the color bar
			vmax = vmax_val,  #Sets the maximum value for the highest saturation of the color bar
            linewidths=.5,    #Sets line width of plot
            xticklabels=True, #shows all X axis tick labels
            yticklabels=True  #shows all Y axis tick labels
)

# OUTPUT AND SAVE THE PLOT
#g.ax_row_dendrogram.remove()    #removes the dendrogram from the plot (if needed)
plt.setp(g.get_yticklabels(), rotation=0)   #makes sure that the Y axis tick labels are horizontal
plt.tight_layout()               #ensures that all labels won't get cut off
plt.title("Well Position test")  #YOUR TITLE GOES HERE
plt.show()                       #shows a preview before saving
fig = g.figure
print("saving to " + myOutput)
fig.savefig(myOutput)
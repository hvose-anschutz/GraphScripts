#!/usr/bin/env python3

"""Creates a Line Plot from a provided dataset."""

# NECESSARY MODULE IMPORTS
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import re
import functions.parameters.all_file_funcs as myfunc

# OPEN FILES AND GENERATE PATH NAMES
myCSV = myfunc.get_file_from_cmd()
#myCSV = myfunc.get_data_path("your_file_goes_here") #your file goes here if only running this script
OutputFile = myfunc.my_output_file(myCSV, plot_type="LinePlot", extension="svg")

####################################################################################################
# PUT ALL VARIABLES FROM YOUR DATASET HERE! THERE IS NO NEED TO EDIT THE CODE BELOW #

#Your Filename
filename = "datasets/KN_fixed_results.csv"
format_based_on_filename = False
alternate_title = "MHVY_fixed_heatmap"

#quality control and formatting
well_positions = False #if you only have well positions and want the heatmap plotted per well
q_filtering = True #filter cell values based on quantile thresholing
q_val = 0.95 #if q filtering, the threshold to set the filter to
debug_show_plot = False #set to True if you want to view the plot locally. May break plot save.

#The order of tissues to plot on the graph (these must match the names in your file EXACTLY)
TissueOrder = ["mLN","PeyersPatch","Colon"]
#Treatment/Infection Order (these must match the secondary names in your file EXACTLY)
TreatmentOrder = ["ControlDiet","HiFiDiet"]

#Color Customization (sets the max value for the heatmap and generates a colormap)
Pal = sns.light_palette("#bb334c", as_cmap=True) 

#x and y axis data (these must match your column names EXACTLY)
x_val = "Time"
y_val = "Copies"

#plot formatting
title = "MHV-Y"
rotate = 0

####################################################################################################

# SET BASIC THEME PARAMETERS
sns.set_theme()

# FUNCTION DEFINITIONS
def my_output_file(filename: str, plot_type: str ="Plot", extension: str="svg", csv:bool=True) -> str:
    """Creates a regex to rename the output file based on the original .csv file. The plot type adds the name of
       the plot to the filename, and the extension specifies what file format to save (svg, png, jpeg, or pdf)."""
    try:
        if extension in ["svg", "png", "pdf", "jpeg", "jpg"]:
            just_name = filename.split("/")
            if csv == True:
                new_name = re.sub(".csv$","_Image" + plot_type + "." + extension, just_name[::-1][0],1)
            else:
                new_name = filename + "_Image" + plot_type + "." + extension
            return os.getcwd() + "/generated_images/" + new_name
    except AttributeError:
        print("_io.TextIOWrapper object has no attribute 'split'. Double check that the filename passed is a string.")
        sys.exit(1)

# OPEN FILES AND GENERATE PATH NAMES
myCSV = filename            # use this if you have access to this script directly

if format_based_on_filename == True:
    mySVGOut = my_output_file(filename, plot_type="LinePlot",extension="svg")  #Generates a regular expression to automate the output filename
else:
    mySVGOut = my_output_file(alternate_title, plot_type="LinePlot",extension="svg",csv=False)


# READ IN THE DATA SET
DataSet = pd.read_csv(myCSV,index_col = 0)

# GENERATE THE LINE PLOT
g = sns.lineplot(
    data=DataSet,
    x=x_val,         # x axis data
    y=y_val,       # y axis data
    hue="Condition",  # grouping variable (what the color change will be based on)
    markers=True,     # draws default markers
    dashes=False,     # draws solid lines for data
    ci = 68           # size of the confidence interval
)

# GENERATE THE SCATTERPLOT
sns.scatterplot(
    data=DataSet,     # dataset to use
    x=x_val,         # x axis data
    y=y_val,       # y axis data
    hue="Condition",  # grouping variable (what the color change will be based upon)
)

g.set(xticks = [8, 16, 24, 48])		#Sets where the ticks are on the X axis is

# SHOW AND SAVE THE PLOT
#plt.show()                         #creates a preview of the plot
plt.savefig(OutputFile, dpi=300)
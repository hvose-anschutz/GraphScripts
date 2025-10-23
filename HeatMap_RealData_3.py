#!/usr/bin/env python3

"""Creates a HeatMap based on a provided dataset."""

# NECESSARY IMPORTS
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
import re
import sys

####################################################################################################
# PUT ALL VARIABLES FROM YOUR DATASET HERE! THERE IS NO NEED TO EDIT THE CODE BELOW #

#Your Filename
filename = "datasets/KN_results.csv"
format_based_on_filename = False
alternate_title = "CCR3_plot"

#quality control and formatting
well_positions = False #if you only have well positions and want the heatmap plotted per well
q_filtering = True #filter cell values based on quantile thresholing
q_val = 0.95 #if q filtering, the threshold to set the filter to

#The order of tissues to plot on the graph (these must match the names in your file EXACTLY)
TissueOrder = ["Adipose Tissue","Cecum","Distal Colon","Liver","mLN","Omentum","PP","Proximal Colon","SI Zone A","SI Zone B","SI Zone C","SI Zone D","SI Zone E","Spleen"]	

#Treatment/Infection Order (these must match the secondary names in your file EXACTLY)
TreatmentOrder = ["Uninfected","MHV-Y","yHV68","yHV68 + MHV-Y"]

#Color Customization (sets the max value for the heatmap and generates a colormap)
Pal = sns.light_palette("#bb334c", as_cmap=True) 

#x and y axis data (these must match your column names EXACTLY)
x_val = "Sample Name"
heat_val = "CCR3"
y_val = "Infection"

#plot formatting
title = "CCR3"
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
myOutput = my_output_file(title, plot_type="HeatMap")

# READ IN THE DATA
DataSet = pd.read_csv(myCSV)

if well_positions == True:
    if q_filtering == True:
        q = DataSet[heat_val].quantile(q_val)
        DataSet = DataSet[DataSet[heat_val] < q]
    DataSet["row"] = DataSet["Well Positions"].str.extract("([A-Za-z]+)")
    DataSet["column"] = DataSet["Well Positions"].str.extract("(\d+)").astype(int)

    vmax_val = math.ceil(DataSet[heat_val].max())
    heatmap_data = DataSet.pivot(index="row",columns="column",values=heat_val)
else:
    if q_filtering == True:
        q = DataSet[heat_val].quantile(q_val)
        DataSet = DataSet[DataSet[heat_val] < q]
    
    vmax_val = DataSet[heat_val].max()
    means = DataSet.groupby([x_val,y_val]).mean().reset_index()
    heatmap_data = means.pivot(index=x_val,columns=y_val,values=heat_val)


# SET AESTHETICS
#lut = dict(zip(TnType.unique(), "rbg"))
#row_col = TnType.map(lut)
#Sets color palette to be in the range from White to a Saturated Color, should be set to the color of the year

# GENERATE THE HEATMAP
g = sns.heatmap(heatmap_data,
			cmap = Pal, #Determines the colormap based on a provided palette (see above)
			vmin = 0,  #Sets the minimum value for the lowest saturation of the color bar
			vmax = vmax_val,  #Sets the maximum value for the highest saturation of the color bar
            linewidths=.5,
            xticklabels=True,
            yticklabels=True
)

# OUTPUT AND SAVE THE PLOT
#g.ax_row_dendrogram.remove()    #removes the dendrogram from the plot (if needed)
plt.setp(g.get_yticklabels(), rotation=rotate)
plt.tight_layout()
plt.title(title)
plt.show()
#fig = g.figure
#fig.savefig(myOutput)
#!/usr/bin/env python3

"""Generates a Violin Plot based off of an inputted file"""

# NECESSARY IMPORTS
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys
import os

####################################################################################################
# PUT ALL VARIABLES FROM YOUR DATASET HERE! THERE IS NO NEED TO EDIT THE CODE BELOW #

filename = "../datasets/my_file.csv"

debug_show_plot = False

TissueOrder = ["mLN","PeyersPatch","Colon"]	
TreatmentOrder = ["MHV-Y", "MHV-Y_dHE"]  

x_val = "Tissue"
y_val = "Log_Copies"
hue_val = "Treatment"

white_overlay = "Treatment"
custom_colors = ["#AE3899","#CF92DD","#009933","#EDAB21"]

####################################################################################################

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
                new_name = filename + "_" + plot_type + "." + extension
            return os.getcwd() + "/" + new_name
    except AttributeError:
        print("_io.TextIOWrapper object has no attribute 'split'. Double check that the filename passed is a string.")
        sys.exit(1)


# READ IN THE DATA
DataSet = pd.read_csv(filename,index_col = 0)
mySVGOut = my_output_file(filename, plot_type="Violin",extension="svg")  #regex to generate a new filename based on the .csv filename


# GET COLORS AND DEFINTE AESTHETIC PARAMETERS
sns.set_theme(rc={'figure.figsize':(5,2)}) #sets the global parameters for graphing objects
WhiteWheel = ["#FFFFFF"] * len(list(set(DataSet[white_overlay])))

# MAKE THE VIOLIN PLOT
g = sns.violinplot(data=DataSet, #data: data object being plotted
	x=x_val,                  #x: x-axis label
	y=y_val,              #y: y-axis label
	hue=hue_val,	         #hue: defines how the bars will be split
	cut = 1,                     #cut: defines how far the density extends past the data point extremes (0 limits to inside the points)
	order = TissueOrder,	     #order: defines the order of the tissues on the x axis
	hue_order = TreatmentOrder,  #hue_order: defines the order of the treatment on the X axis
	palette= custom_colors,         #palette: controls the colors on the graph, must be a hash Treatment value to Hex code
	saturation = 1,              #saturation: defines how saturated the color will be (0 is black and white, 1 is fully colored)
#	height=1,		             #height: controls the height of the graph
	inner = None,                #inner: can specify a smaller graph type behind the data (i.e. "box", "stick", etc...)
	density_norm = 'width',      #density_norm: conforms all plots to the same parameter (width = they all have the same width)
#	aspect = 1, #3 Categories    #aspect: controls the width/height ratio of the graph, relevant to how many graphs there are
#	aspect = .7, #2 Categories
	linewidth = 1,               #linewidth: defines the line thickness around the bar
	edgecolor = "black"	         #edgecolor: defines the line color around the bar
)
plt.ylim(0,7)                    #plt.ylim(min, max): limits the range on the y-axis 
#sns.set_axis_labels("", "")
#g.legend.set_title("")


# MAKE THE SWARM PLOT TO SHOW OBSERVATIONS
ax = sns.swarmplot(data=DataSet,                #data object being graphed
					x=x_val,                 #x-axis label
					y=y_val,             #y-axis label
					hue=hue_val,            #defines how the points will be split
					order = TissueOrder,	    #defines the order of the tissues on the x axis
					dodge = "true",	            #makes sure the dots are not plotted in the same column
					hue_order = TreatmentOrder, #defines the order of the treatment on the X axis
					palette = WhiteWheel,       #defines color palette to make sure every dot is white
					edgecolor = "black",        #colors the edge of the points
					size = 5,	                #defines size of dot
					linewidth = .75, #defines the line thickness around the white dot
)
#ax.set(ylim=(0, 6))
#sns.despine(top = True)
ax.legend_.remove()       #removes the legend from the graph

#SHOW AND SAVE THE PLOT
g = g.figure              #creates a figure object

if debug_show_plot == True:
	plt.show()                #shows a preview output
g.savefig(mySVGOut)      #saves the file to a .svg format with the regex filename from earlier
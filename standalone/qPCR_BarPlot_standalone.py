#!/usr/bin/env python3

"""Generates a barplot with categorical swarmplot overlayed."""

# NECESSARY IMPORTS
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import re

####################################################################################################
# PUT ALL VARIABLES FROM YOUR DATASET HERE! THERE IS NO NEED TO EDIT THE CODE BELOW #

# Your Filename
filename = "../datasets/Rep2_LOD.csv"
format_based_on_filename = False
alternate_title = "MHVY_Rep2_Threshold"

# q_filtering
q_filtering = True
q = 0.95

# formatting and debugging
debug_show_plot = (
    False  # Set to True if you want to view the plot locally. May break saved file.
)

# The order of tissues to plot on the graph (these must match the names in your file EXACTLY)
TissueOrder = [
    "Cecum",
    "Distal Colon",
    "Liver",
    "mLN",
    "PP",
    "Proximal Colon",
    "SI Zone A",
    "SI Zone B",
    "SI Zone C",
    "SI Zone D",
    "SI Zone E",
    "Spleen",
]

# Treatment/Infection Order (these must match the secondary names in your file EXACTLY)
TreatmentOrder = ["Uninfected", "MHV-Y", "yHV68", "yHV68 + MHV-Y"]

# Color Customization (the white_overlay_palette should match the bar_split)
custom_colors = ["#AE3899", "#CF92DD", "#009933", "#EDAB21"]
white_overlay_palette = "Tissue"

# x and y axis data (these must match your column names EXACTLY)
x_vals = "Tissue"
y_vals = "MHV-Y"
bar_split = "Infection"

# plot formatting
axis_rotate = 90
title = "MHVY Threshold"

####################################################################################################


# FUNCTION DEFINITIONS
def my_output_file(
    filename: str, plot_type: str = "Plot", extension: str = "svg", csv: bool = True
) -> str:
    """Creates a regex to rename the output file based on the original .csv file. The plot type adds the name of
    the plot to the filename, and the extension specifies what file format to save (svg, png, jpeg, or pdf).
    """
    try:
        if extension in ["svg", "png", "pdf", "jpeg", "jpg"]:
            just_name = filename.split("/")
            if csv == True:
                new_name = re.sub(
                    ".csv$",
                    "_Image" + plot_type + "." + extension,
                    just_name[::-1][0],
                    1,
                )
            else:
                new_name = filename + "_Image" + plot_type + "." + extension
            return os.getcwd() + "/" + new_name
    except AttributeError:
        print(
            "_io.TextIOWrapper object has no attribute 'split'. Double check that the filename passed is a string."
        )
        sys.exit(1)


# PROCESS THE FILE
# FileCSV = myfunc.get_file_from_cmd()
# FileCSV = "qPCR_test.csv"
if format_based_on_filename == True:
    mySVGOut = my_output_file(
        filename, plot_type="Bar", extension="svg"
    )  # Generates a regular expression to automate the output filename
else:
    mySVGOut = my_output_file(
        alternate_title, plot_type="Bar", extension="svg", csv=False
    )

# READ IN THE DATA
DataSet = pd.read_csv(filename, header=0)  # Creates a 2D editable table

# DataSet[(np.abs(stats.zscore(DataSet)) < 3).all(axis=1)]

# ATTEMPT TO REMOVE OUTLIERS
if q_filtering == True:
    q_val = DataSet[y_vals].quantile(q)

    final_df = DataSet[DataSet[y_vals] < q_val]
else:
    final_df = DataSet

# separate out the relative sample distinctions (need them to be separate for labeling purposes)
# DataSet[['Mouse', 'Tissue']] = DataSet['Tissue & Sample ID'].str.split(' - ', n=1, expand=True)

# print(DataSet.head())

# FIRST VARIABLE
# TissueOrder = ["Colon"]	                       #Must edit for new dataset, a list of labels

# SECOND (OPTIONAL) VARIABLE
# TreatmentOrder = ["MHV-Y", "MHV-Y_dHE"]            #A list of labels
# TreatmentOrder = ["SPF", "GF"]
# TreatmentOrder = ["WT", "CD64-creSTING-flox"]

# GENERATE COLOR WHEELS

WhiteWheel = ["#FFFFFF"] * len(list(set(DataSet[white_overlay_palette])))

# GENERATE THE BARPLOT
### Note: The x, y, and hue axes should be the same for both the catplot and the swarmplot, as this allows seaborn to map the dots correctly to each bar.
### The palette for the swarmplot should be the WhiteWheel generated above, as it will force all dots to be the same color.

g = sns.catplot(
    data=final_df,
    kind="bar",  # specifies the kind of categorical plot
    # row = "Tissue",            #determines the faceting of the grid, creates separate plots
    x=x_vals,  # x axis data
    y=y_vals,  # y axis data
    hue=bar_split,  # defines how the bars will be split
    order=TissueOrder,  # defines the order of the tissues on the x axis
    # hue_order = TreatmentOrder, #defines the order of the treatment on the X axis
    errorbar="sd",  # specifies whether using an error bar or a confidence interval
    err_kws={"linewidth": 0.75},  # line width of the error bar
    capsize=0.1,  # controls the cap of the stdev whisker
    palette=custom_colors,  # controls the colors on the graph, each value of Treatment must have a hex code
    saturation=1,  # controls the saturation of the color (1 is full, 0 is black and white)
    height=6,  # controls the height of the graph
    aspect=1.2,  # controls the aspect ratio of the output graph, 4 Categories
    #    aspect = 1, #3 Categories
    #    aspect = .7, #2 Categories
    linewidth=1,  # defines the line thickness around the bar
    edgecolor="black",  # defines the line color around the bar
)
# g.despine(left=True)
g.set_axis_labels("", "")  # sets labels to be empty, default will pull from the data
g.set_xlabels("")
g.set_ylabels("")
g.legend.set_title(
    ""
)  # sets the plot title to be empty, default will pull from the data

# DRAW CATEGORICAL SWARMPLOT TO SHOW OBSERVATIONS

ax = sns.swarmplot(
    data=final_df,
    x=x_vals,  # x axis data
    y=y_vals,  # y axis data
    hue=bar_split,  # category separating the data by color
    dodge=True,  # Makes ure the dots are not plotted in the same column
    order=TissueOrder,  # specifies the order of data on the plot
    # hue_order = TreatmentOrder, #defines the order of the second variable on the X axis
    palette=WhiteWheel,  # defines color palette to make sure every dot is white
    edgecolor="black",  # defines the edge color of the dots
    size=3,  # defines size of dot
    linewidth=0.75,  # defines the line thickness around the white dot
    legend=False,
)

ax.set(ylim=(0, None))  # limits the y axis range
ax.set_xticklabels(ax.get_xticklabels(), rotation=axis_rotate)
ax.set_title(title)
# g._legend.remove()             #removes the legend from the plot

# SHOW / SAVE THE PLOT

g.set_xlabels("")
g.set_ylabels("")

if debug_show_plot == True:
    plt.show()
plt.savefig(
    mySVGOut, bbox_inches="tight"
)  # saves the file to the generated_images folder

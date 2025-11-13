#!/usr/bin/env python3

"""Creates a HeatMap based on a provided dataset, with editable functions."""

# NECESSARY IMPORTS
import os
import re
import sys
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

####################################################################################################
# PUT ALL VARIABLES FROM YOUR DATASET HERE! THERE IS NO NEED TO EDIT THE CODE BELOW #

# Your Filename
FILENAME = "../datasets/combined_qPCR_kn.csv"
FORMAT_BASED_FILENAME = False
ALT_TITLE = "MHVY_combined_reps"

# quality control and formatting
WELL_POSITIONS = (
    False  # if you only have well positions and want the heatmap plotted per well
)

STAT_FILTER = True

SAVE_FIGURE = True

# Treatment/Infection Order (these must match the secondary names in your file EXACTLY)
IGNORE_VALUES = ["yHV68"]

# Color Customization (sets the max value for the heatmap and generates a colormap)
THRESHOLDING = (
    False  # determines if all values under a certain threshold should be the same color
)
THRESHOLD = 1.32
TOP_COLOR = "#bb334c"

# x and y axis data (these must match your column names EXACTLY)
X_VAL = "Tissue"
HEAT_VAL = "MHV-Y"
Y_VAL = "Infection"

# plot formatting
ROTATE_X = 90
ROTATE_Y = 0

####################################################################################################

# SET BASIC THEME PARAMETERS
sns.set_theme()

# FUNCTION DEFINITIONS
def my_output_file(
    filename: str, plot_type: str = "Plot", extension: str = "svg", csv: bool = True
) -> str|None:
    """
    Creates a regex to rename the output file based on the original .csv file. 
    The plot type adds the name of the plot to the filename, and the extension specifies what file 
    format to save (svg, png, jpeg, or pdf).
    """
    try:
        if extension in ["svg", "png", "pdf", "jpeg", "jpg"]:
            just_name = filename.split("/")
            if csv:
                new_name = re.sub(
                    r".csv$",
                    "_Image" + plot_type + "." + extension,
                    just_name[::-1][0],
                    1,
                )
            else:
                new_name = filename + "_Image" + plot_type + "." + extension
            return os.getcwd() + "/" + new_name
        return None
    except AttributeError:
        print(
            "_io.TextIOWrapper object has no attribute 'split'. " \
            "Double check that the filename passed is a string."
        )
        sys.exit(1)
    return None

# OPEN FILES AND GENERATE PATH NAMES

if FORMAT_BASED_FILENAME:
    mySVGOut = my_output_file(
        FILENAME, plot_type="Heatmap", extension="svg"
    )  # Generates a regular expression to automate the output filename
else:
    mySVGOut = my_output_file(
        ALT_TITLE, plot_type="Heatmap", extension="svg", csv=False
    )

####################################################################################################

heatmap_df = pd.read_csv(FILENAME)

#print(heatmap_df.head())

if STAT_FILTER:
    Q1 = heatmap_df[HEAT_VAL].quantile(0.25)
    Q3 = heatmap_df[HEAT_VAL].quantile(0.75)
    IQR = Q3 - Q1

    low_bound = Q1 - (1.5 * IQR)
    high_bound = Q3 + (1.5 * IQR)
    filtered_df = heatmap_df[(heatmap_df[HEAT_VAL] >= low_bound) &
                             (heatmap_df[HEAT_VAL] <= high_bound)]
else:
    filtered_df = heatmap_df

if len(IGNORE_VALUES) > 0:
    for rem in IGNORE_VALUES:
        filtered_df = filtered_df[filtered_df[Y_VAL] != rem]

print(filtered_df.head())
#print(qPCR_df.shape[0])

###################################################################################################

if WELL_POSITIONS:
    filtered_df["row"] = filtered_df["Well Positions"].str.extract(r"([A-Za-z]+)")
    filtered_df["column"] = filtered_df["Well Positions"].str.extract(r"(\d+)").astype(int)
    vmax_val = filtered_df[HEAT_VAL].max()
    heatmap_data = filtered_df.pivot(index="row", columns="column", values=HEAT_VAL)
else:
    vmax_val = filtered_df[HEAT_VAL].max()
    means = filtered_df.groupby([X_VAL, Y_VAL])[HEAT_VAL].mean().reset_index()
    heatmap_data = means.pivot(index=X_VAL, columns=Y_VAL, values=HEAT_VAL)

# SET AESTHETICS
Pal = sns.light_palette(TOP_COLOR, as_cmap=True)

if not THRESHOLDING:
    vmin_val = 0
else:
    vmin_val = THRESHOLD
    Pal.set_under(color="#ffffff")


# lut = dict(zip(TnType.unique(), "rbg"))
# row_col = TnType.map(lut)
# Sets color palette to be in the range from White to a Saturated Color,
# should be set to the color of the year

# GENERATE THE HEATMAP
g = sns.heatmap(
    heatmap_data,
    cmap=Pal,  # Determines the colormap based on a provided palette (see above)
    vmin=vmin_val,  # Sets the minimum value for the lowest saturation of the color bar
    vmax=vmax_val,  # Sets the maximum value for the highest saturation of the color bar
    linewidths=0.5,
    xticklabels=True,
    yticklabels=True,
)

# OUTPUT AND SAVE THE PLOT
# g.ax_row_dendrogram.remove()    #removes the dendrogram from the plot (if needed)
plt.setp(g.get_xticklabels(), rotation=ROTATE_X)
plt.setp(g.get_yticklabels(), rotation=ROTATE_Y)
plt.tight_layout()

if SAVE_FIGURE:
    fig = g.figure
    fig.savefig(mySVGOut, bbox_inches="tight")
plt.show()

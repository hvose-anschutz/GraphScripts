#!/usr/bin/env python3

"""Creates a Line Plot from a provided dataset."""

# NECESSARY MODULE IMPORTS
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
import functions.parameters.all_file_funcs as myfunc

# OPEN FILES AND GENERATE PATH NAMES
myCSV = myfunc.get_file_from_cmd()
#myCSV = myfunc.get_data_path("your_file_goes_here") #your file goes here if only running this script
OutputFile = myfunc.my_output_file(myCSV, plot_type="LinePlot", extension="svg")

# READ IN THE DATA SET
DataSet = pd.read_csv(myCSV,index_col = 0)
TissueOrder = ["mLN","PeyersPatch","Colon"]
TreatmentOrder = ["ControlDiet","HiFiDiet"]

# GET THE COLOR SCHEMES FOR THE DATASET
my_color_wheel = myfunc.get_default_wheel()
white_wheel = myfunc.get_white_wheel(DataSet, "Treatment")

# GENERATE THE LINE PLOT
g = sns.lineplot(
    data=DataSet,
    x="Time",         # x axis data
    y="Copies",       # y axis data
    hue="Condition",  # grouping variable (what the color change will be based on)
    markers=True,     # draws default markers
    dashes=False,     # draws solid lines for data
    ci = 68           # size of the confidence interval
)

# GENERATE THE SCATTERPLOT
sns.scatterplot(
    data=DataSet,     # dataset to use
    x="Time",         # x axis data
    y="Copies",       # y axis data
    hue="Condition",  # grouping variable (what the color change will be based upon)
)

g.set(xticks = [8, 16, 24, 48])		#Sets where the ticks are on the X axis is

# SHOW AND SAVE THE PLOT
#plt.show()                         #creates a preview of the plot
plt.savefig(OutputFile, dpi=300)
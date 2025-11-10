#!/usr/bin/env python3

"""Generates a Facet Grid plot from a dataset."""

# NECESSARY IMPORTS
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import functions.parameters.all_file_funcs as myfunc

# READ IN THE FILES AND GENERATE PATH NAMES
FileCSV = myfunc.get_file_from_cmd()
# FileCSV = myfunc.get_data_path("your_file_goes_here")
mySVGOut = myfunc.my_output_file(FileCSV, plot_type="FacetGrid", extension="svg")

# READ IN THE DATA
DataSet = pd.read_csv(FileCSV, index_col=0)

# TissueOrder = ["Colon"]	#Must edit for new dataset
TissueOrder = ["mLN", "PeyersPatch", "Colon"]  # Must edit for new dataset

# TreatmentOrder = ["ControlDiet","HiFiDiet"]
# TreatmentOrder = ["Control","Amp","Vanc"]		#Must edit for new dataset
# TreatmentOrder = ["Control_Starch", "Control_AcStarch", "Amp_Starch", "Amp_AcStarch"]
# TreatmentOrder = ["SPF", "GF"]
# TreatmentOrder = ["WT", "CD64-creSTING-flox"]
TreatmentOrder = ["Control", "Amp", "AmpHydroxybutyrate", "AmpTributyrin"]

# GENERATE COLOR WHEELS
Colors = myfunc.get_default_wheel()
WhiteWheel = myfunc.get_white_wheel(DataSet, "Treatment")

# PLOT FACET GRID
g = sns.FacetGrid(
    DataSet,
    col="Tissue",
    hue="Treatment",  # defines how the bars will be split
    col_order=TissueOrder,  # defines the order of the tissues on the x axis
    hue_order=TreatmentOrder,  # defines the order of the treatment on the X axis
    palette=Colors.colors,  # This controls the colors on the graph, must be a hash Treatment value to Hex code
    ylim=(0, 6),
    col_wrap=3,
    height=2,  # This controls the height of the graph
    aspect=1,  # 4 Categories
    #    aspect = 1, #3 Categories
    #    aspect = .7, #2 Categories
)

# GENERATE THE BAR PLOT
g.map(
    sns.barplot,
    "Treatment",
    "Log_Copies",
    order=TreatmentOrder,
    inner=None,
    scale="width",
    edgecolor="black",
)

# GENERATE THE SWARM PLOT
g.map(
    sns.swarmplot,
    "Treatment",
    "Log_Copies",
    order=TreatmentOrder,
    palette=WhiteWheel,
    edgecolor="black",
    size=5,  # defines size of dot
    linewidth=0.75,  # defines the line thickness around the white dot
)
# sns.set_axis_labels("", "")
# g.legend.set_title("")


# SHOW AND SAVE THE PLOT
# plt.show()
g = g.figure
g.savefig(mySVGOut)

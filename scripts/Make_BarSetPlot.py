#!/usr/bin/env python3
"""Generates a BarSet Plot from a provided dataset."""

# NECESSARY IMPORTS
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import functions.parameters.all_file_funcs as myfunc

# READ IN THE FILES AND GENERATE PATH / CATEGORICAL NAMES
FileCSV = myfunc.get_data_path(myfunc.get_file_from_cmd())
#FileCSV = myfunc.get_data_path("your_file_goes_here")
mySVGOut = myfunc.my_output_file(FileCSV, plot_type="BarSet",extension="svg")
DataSet = pd.read_csv(FileCSV,index_col = 0)

#TissueOrder = ["Colon"]	                           #Must edit for new dataset
TissueOrder = ["mLN","PeyersPatch","Colon"]	           #Must edit for new dataset

#TreatmentOrder = ["ControlDiet","HiFiDiet"]
#TreatmentOrder = ["Control","Amp","Vanc"]		       #Must edit for new dataset
#TreatmentOrder = ["Control_Starch", "Control_AcStarch", "Amp_Starch", "Amp_AcStarch"]
#TreatmentOrder = ["SPF", "GF"]
#TreatmentOrder = ["WT", "CD64-creSTING-flox"]
TreatmentOrder = ["Control","Amp","AmpHydroxybutyrate","AmpTributyrin"]

# GENERATE COLOR WHEELS
WhiteWheel = myfunc.get_white_wheel(DataSet, "Treatment")
Colors = myfunc.get_default_wheel()

g = sns.catplot(data=DataSet,
    kind="bar",                   #type of categorical graph
	col = "Tissue",               #column separator category
	col_order = TissueOrder,      #column ordering
    x="Treatment",                #x axis data
    y="Log_Copies",               #y axis data 
    order = TreatmentOrder,	      #defines the order of the tissues on the x axis
    ci="sd",                      #specifies whether using an error bar or a confidence interval
    errwidth = .75,	              #line width of the error bar
    capsize = .1,	              #controls the cap of the stdev whisker
    palette= Colors,              #controls the graph colors, each unique value of treatment should have a hex code
 	saturation = 1,               #saturation of color (1 is full, 0 is black and white)
    height=6,		              #controls the height of the graph
    aspect = .5,                  #changes the aspect ratio of the graph, 4 Categories
#    aspect = 1, #3 Categories
#    aspect = .7, #2 Categories
	linewidth = 1,                #defines the line thickness around the bar
	edgecolor = "black"	          #defines the line color around the bar
)

# GENERATE THE SWARMPLOT
ax = sns.catplot(data=DataSet,
    kind="swarm", 
	col = "Tissue",
	col_order = TissueOrder,
    x="Treatment", 
    y="Log_Copies", 
    order = TreatmentOrder,	      #defines the order of the tissues on the x axis
	palette = WhiteWheel,         #defines color palette to make sure every dot is white
	edgecolor = "black",          #defines edges of the plot points
	height = 6,	                  #defines size of dot
	linewidth = .75,              #defines the line thickness around the white dot
)

# SHOW / SAVE THE OUTPUT
#plt.show()
g.savefig(mySVGOut)
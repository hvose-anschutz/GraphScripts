#!/usr/bin/env python3

"""This is a test document for a bar graph with points."""

# NECESSARY IMPORTS AND STYLE SETTINGS
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import functions.parameters.all_file_funcs as myfunc
sns.set_theme(style="whitegrid")

# READ IN DATA AND SET UP AXES
DataSet = pd.read_csv('2Categories.csv',index_col = 0)
TissueOrder = ["mLN","PeyersPatch","Colon"]
TreatmentOrder = ["MHV-Y", "MHV-Y_dHE"] 

# GENERATE COLOR WHEELS
WhiteWheel = myfunc.get_white_wheel(DataSet, "Treatment")
Colors = myfunc.get_default_wheel()

# MAKE BAR PLOT
g = sns.catplot(data=DataSet,
    kind="bar",
    x="Tissue", 
    y="Log_Copies", 
    hue="Treatment",	#defines how the bars will be split
    order = TissueOrder,	#defines the order of the tissues on the x axis
    hue_order = TreatmentOrder, #defines the order of the treatment on the X axis
    ci="sd", #specifies whether using an error bar or a confidence interval
    errwidth = .75,	#line width of the error bar
    capsize = .1,	#This controls the cap of the stdev whisker
    palette= Colors.colors, #This controls the colors on the graph, must be a hash Treatment value to Hex code
 #   alpha=.6, 
    height=6,		#This controls the height of the graph
 #   aspect = 1, #3 Categories
    aspect = .7, #2 Categories
	linewidth = 1, #defines the line thickness around the bar
	edgecolor = "black"	#defines the line color around the bar
)
g.despine(left=True)
g.set_axis_labels("", "Log Copies")
g.legend.set_title("")

# MAKE SCATTERPLOT TO SHOW OBSERVATIONS
ax = sns.swarmplot(data=DataSet, 
					x="Tissue", 
					y="Log_Copies", 
					hue="Treatment", 
					dodge = "true",	#Makes sure the dots are not plotted in the same column
				    order = TissueOrder,
					palette = WhiteWheel, #defines color palette to make sure every dot is white
					edgecolor = "black",
					size = 9,	#defines size of dot
					linewidth = .75, #defines the line thickness around the white dot
)


#SHOW AND SAVE OUTPUT
g._legend.remove()
#plt.show()
g.savefig("output2.svg")
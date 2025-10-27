#!/usr/bin/env python3

"""Generates a barplot with categorical swarmplot overlayed."""

# NECESSARY IMPORTS
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import functions.parameters.all_file_funcs as myfunc

# PROCESS THE FILE
#FileCSV = myfunc.get_file_from_cmd()
FileCSV = "Data.csv"
mySVGOut = myfunc.my_output_file(FileCSV, plot_type="Bar",extension="svg")  #Generates a regular expression to automate the output filename

# READ IN THE DATA
DataSet = pd.read_csv(FileCSV,index_col = 0)       #Creates a 2D editable table

#FIRST VARIABLE
#TissueOrder = ["Colon"]	                       #Must edit for new dataset
TissueOrder = ["mLN","PeyersPatch","Proximal Colon","Epithelial cells"]	       #A list of labels 
#TreatmentOrder = ["ControlDiet","HiFiDiet"]
#TreatmentOrder = ["Control","Amp","Vanc"]		   #Must edit for new dataset
#TreatmentOrder = ["Control_Starch", "Control_AcStarch", "Amp_Starch", "Amp_AcStarch"]

#SECOND (OPTIONAL) VARIABLE
#TreatmentOrder = ["MHV-Y", "MHV-Y_dHE"]            #A list of labels
#TreatmentOrder = ["SPF", "GF"]
#TreatmentOrder = ["WT", "CD64-creSTING-flox"]
#TreatmentOrder = ["Control","Amp","AmpHydroxybutyrate","AmpTributyrin"]


# GENERATE COLOR WHEELS
Colors = myfunc.make_wheel()
custom_colors = myfunc.make_wheel()

Colors.add(["mLN","PeyersPatch","Proximal Colon","Epithelial cells"])
custom_colors.add(["mLN","PeyersPatch","Proximal Colon","Epithelial cells"],["#AE3899","#CF92DD","#009933","#EDAB21"])

WhiteWheel = myfunc.get_white_wheel(DataSet, "Tissue") #specify dataset loaded in and the variable to match colors to

Colors.print_colors()
custom_colors.print_colors()

# GENERATE THE BARPLOT

g = sns.catplot(data=DataSet,
    kind="bar",                 #specifies the kind of categorical plot
    #row = "Tissue",             #determines the faceting of the grid
    x="Tissue",                  #x axis data
    y="Log_Copies",             #y axis data
    hue="Tissue",	            #defines how the bars will be split
    order = TissueOrder,	    #defines the order of the tissues on the x axis
    #hue_order = TreatmentOrder, #defines the order of the treatment on the X axis
    errorbar="sd",                    #specifies whether using an error bar or a confidence interval
    err_kws={'linewidth':0.75},	            #line width of the error bar
    capsize = .1,	            #controls the cap of the stdev whisker
    palette= Colors.colors,            #controls the colors on the graph, each value of Treatment must have a hex code
 	saturation = 1,             #controls the saturation of the color (1 is full, 0 is black and white)
    height=6,		            #controls the height of the graph
    aspect = 1.2,               #controls the aspect ratio of the output graph, 4 Categories
#    aspect = 1, #3 Categories
#    aspect = .7, #2 Categories
	linewidth = 1,              #defines the line thickness around the bar
	edgecolor = "black"	        #defines the line color around the bar
)
#g.despine(left=True)
#g.set_axis_labels("", "")       #sets labels to be empty, default will pull from the data
g.set_xlabels("")
g.set_ylabels("")
#g.legend.set_title("")          #sets the plot title to be empty, default will pull from the data


# DRAW CATEGORICAL SWARMPLOT TO SHOW OBSERVATIONS

ax = sns.swarmplot(data=DataSet, 
					x="Tissue",                 #x axis data
					y="Log_Copies",             #y axis data
					hue="Tissue",            #category separating the data by color
					dodge = "true",	            #Makes ure the dots are not plotted in the same column
				    order = TissueOrder,        #specifies the order of data on the plot
			        #hue_order = TreatmentOrder, #defines the order of the second variable on the X axis
					palette = WhiteWheel,       #defines color palette to make sure every dot is white
					edgecolor = "black",        #defines the edge color of the dots
					size = 12,	                #defines size of dot
					linewidth = .75,            #defines the line thickness around the white dot
)

#ax.set(ylim=(0, 6))           #limits the y axis range        
#g._legend.remove()             #removes the legend from the plot

# SHOW / SAVE THE PLOT

g.set_xlabels("")
g.set_ylabels("")               
plt.savefig(mySVGOut)          #saves the file to the generated_images folder
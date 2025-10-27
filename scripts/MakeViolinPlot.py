#!/usr/bin/env python3

"""Generates a Violin Plot based off of an inputted file"""

# NECESSARY IMPORTS
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import functions.parameters.all_file_funcs as myfunc

# OPEN THE FILES AND GENERATE PATH NAMES
FileCSV = myfunc.get_file_from_cmd()                 #if being used as a command line input, this specifies the "input" parameter
#FileCSV = myfunc.get_data_path("your_data_goes_here")
mySVGOut = myfunc.my_output_file(FileCSV, plot_type="Violin",extension="svg") #regex to generate a new filename based on the .csv filename

# READ IN THE DATA
DataSet = pd.read_csv(FileCSV,index_col = 0)

#TissueOrder = ["Colon"]	#Must edit for new dataset
TissueOrder = ["mLN","PeyersPatch","Colon"]	#Specifies the order of tissues being read in, must be edited for new datasets

#TreatmentOrder = ["ControlDiet","HiFiDiet"]
#TreatmentOrder = ["Control","Amp","Vanc"]		#Must edit for new dataset
#TreatmentOrder = ["Control_Starch", "Control_AcStarch", "Amp_Starch", "Amp_AcStarch"]
#TreatmentOrder = ["SPF", "GF"]
#TreatmentOrder = ["WT", "CD64-creSTING-flox"]
#TreatmentOrder = ["Control","Amp","AmpHydroxybutyrate","AmpTributyrin"]
TreatmentOrder = ["MHV-Y", "MHV-Y_dHE"]     #Specifies the order of treatments being read in

# GET COLORS AND DEFINTE AESTHETIC PARAMETERS
WhiteWheel = myfunc.get_white_wheel(DataSet, "Treatment")
ColorWheel = myfunc.get_default_wheel()
sns.set_theme(rc={'figure.figsize':(5,2)}) #sets the global parameters for graphing objects

# MAKE THE VIOLIN PLOT
g = sns.violinplot(data=DataSet, #data: data object being plotted
	x="Tissue",                  #x: x-axis label
	y="Log_Copies",              #y: y-axis label
	hue="Treatment",	         #hue: defines how the bars will be split
	cut = 1,                     #cut: defines how far the density extends past the data point extremes (0 limits to inside the points)
	order = TissueOrder,	     #order: defines the order of the tissues on the x axis
	hue_order = TreatmentOrder,  #hue_order: defines the order of the treatment on the X axis
	palette= ColorWheel,         #palette: controls the colors on the graph, must be a hash Treatment value to Hex code
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
					x="Tissue",                 #x-axis label
					y="Log_Copies",             #y-axis label
					hue="Treatment",            #defines how the points will be split
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
#plt.show()                #shows a preview output
g.savefig(mySVGOut)      #saves the file to a .svg format with the regex filename from earlier
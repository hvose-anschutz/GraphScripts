#!/usr/bin/env python3

"""Graphs an XY-Volcano plot."""

import seaborn as sns
import pandas as pd
import functions.parameters.all_file_funcs as myfunc


myCSV = myfunc.get_data_path("your_data_goes_here")

df = pd.read_csv(myCSV,index_col = 0, header = 0) #Reads in CSV file into Pandas Dataframe

print (df.head()) #shows the first few rows of the data to make sure everything looks OK


# Draw the full plot
g = sns.scatterplot(data=df, 
					x="FoldChange",			#Sets which column will be graphed on the X axis
					y="Pval",				#Sets which column will be graphed on the Y axis
					hue = "SPF" ,			#Sets which column determines the color of the dots
					size = "SPF" ,			#Sets which column determines the size of the dots
					edgecolor = "black",	#Sets the color of the line
					linewidth = 0.2,		#Sets the line thickness
					palette = sns.color_palette("light:#7C4480", as_cmap=True), #Defines that range of colors expressed by "hue"
					sizes = (1,200) 		#Defines that range of sizes expressed by "size"
					)
#g.set(ylim = (-0.2,5))	#Sets the Y axis range. Comment this out at first when you are first making the graph so you know what the actual range of your data is.
#g.set(xlim = (-5,5))	#Sets the X axis range. Comment this out at first when you are first making the graph so you know what the actual range of your data is.
#g.set(xticks = [-5, -3, -1, 0, 1, 3, 5])		#Sets where the ticks are on the X axis is. Comment this out at first when you are first making the graph so you know what the actual range of your data is, and then set your ticks based on that. You should include a tick at -1, 0 and 1, so you can draw the vertical bars
#g.set(yticks = [0, 1, 1.3, 2, 3, 4, 5])		#Sets where the ticks are on the Y axis is. Comment this out at first when you are first making the graph so you know what the actual range of your data is, and then set your ticks based on that. You should include a tick at 1.3 (this is p = 0.05), so you can draw the horizontal bar

fig = g.figure
fig.savefig('Skin_GF_vs_SPF_Volcano.svg') #Saves the plot to a file
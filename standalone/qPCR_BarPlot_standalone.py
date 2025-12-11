#!/usr/bin/env python3

"""Creates a barplot with an overlayed stripplot with relevant statistical
annotations for each statistically significant tissues."""

import warnings
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from statannotations.Annotator import Annotator

warnings.filterwarnings('ignore')
####################################################################################################

# PUT ALL VARIABLES FROM YOUR DATASET HERE! THERE IS NO NEED TO EDIT THE CODE BELOW #

# Your Filename
FILENAME = "../datasets/Intracellular_20251208.csv"

# File Save Options
SAVE_FIGURE = (
    False # Set to True if you want to save the plot.
)
OUTPUT_FILE = "MHVY_Supernatant_bar_qPCR.png"

# Filtering out by another column
EXTRA_FILTER = True
FILTER_COL = "Viral Genotype"
FILTER_VAL = "MHV-Y"

# The order of tissues to plot on the graph (these must match the names in your file EXACTLY)
TISSUE_ORDER = [
    1,
    0,
    -1,
    -2,
    -3,
    -4,
    -5,
    -6
]

# Treatment/Infection Order (these must match the secondary names in your file EXACTLY)
TREATMENT_ORDER = ["WT","KO"]
IGNORE_VALUES = []

# Statistical filtering and formatting
STAT_FILTER = False
LINE_PLACE = 'outside'

# Color Customization (the white_overlay_palette should match the bar_split)
CUSTOM_COLORS = ["#EDAB21","#AE3899", "#CF92DD"]
WHITE_OVERLAY = "IRG"

# x and y axis data (these must match your column names EXACTLY)
X_VALS = "log(MOI)"
Y_VALS = "LogValue"
BAR_SPLIT = "IRG"

# plot formatting
AXIS_ROTATE = 90

####################################################################################################

if EXTRA_FILTER:
    qPCR_load = pd.read_csv(FILENAME)
    qPCR_df = qPCR_load[qPCR_load[FILTER_COL] == FILTER_VAL]
else:
    qPCR_df = pd.read_csv(FILENAME)

print(qPCR_df.shape[0])

if STAT_FILTER:
    Q1 = qPCR_df[Y_VALS].quantile(0.25)
    Q3 = qPCR_df[Y_VALS].quantile(0.75)
    IQR = Q3 - Q1

    low_bound = 0
    high_bound = Q3 + (1.5 * IQR)
    filtered_df = qPCR_df[(qPCR_df[Y_VALS] >= low_bound) & (qPCR_df[Y_VALS] <= high_bound)]
else:
    filtered_df = qPCR_df

if len(IGNORE_VALUES) > 0:
    for rem in IGNORE_VALUES:
        filtered_df = filtered_df[filtered_df[BAR_SPLIT] != rem]


print(filtered_df.head())
#print(qPCR_df.shape[0])

###################################################################################################
WhiteWheel = ["#FFFFFF"] * len(list(set(filtered_df[WHITE_OVERLAY])))

# GENERATE THE BARPLOT
### Note: The x, y, and hue axes should be the same for both the catplot and the swarmplot, as this
# allows seaborn to map the dots correctly to each bar.
### The palette for the swarmplot should be the WhiteWheel generated above, as it will force all
# dots to be the same color.

g = sns.catplot(
    data=filtered_df,
    kind="bar",  # specifies the kind of categorical plot
    # row = "Tissue",            #determines the faceting of the grid, creates separate plots
    x=X_VALS, # x axis data
    y=Y_VALS, # y axis data
    hue=BAR_SPLIT,  # defines how the bars will be split
    order=TISSUE_ORDER,  # defines the order of the tissues on the x axis
    hue_order = TREATMENT_ORDER, #defines the order of the treatment on the X axis
    errorbar="sd",  # specifies whether using an error bar or a confidence interval
    err_kws={"linewidth": 0.75},  # line width of the error bar
    capsize=0.1,  # controls the cap of the stdev whisker
    palette=CUSTOM_COLORS,  # controls the colors on the graph, each value must have a hex code
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

###################################################################################################
pairs = []

for tis in TISSUE_ORDER:
    for treat in range(0,len(TREATMENT_ORDER)-1):
        for idx, treat2 in enumerate(TREATMENT_ORDER):
            if treat < idx:
                pair1 = TREATMENT_ORDER[treat]
                pair2 = treat2
                new_pair = ((tis,pair1),(tis,pair2))
                pairs.append(new_pair)

#print(pairs)

for ax_row in g.axes:
    for my_ax in ax_row:
        annot = Annotator(my_ax,
                          pairs,
                          data=filtered_df,
                          x=X_VALS,
                          y=Y_VALS,
                          hue=BAR_SPLIT,
                          order=TISSUE_ORDER,
                          hue_order=TREATMENT_ORDER)
        annot.configure(test='Mann-Whitney',
                        text_format='star',
                        loc=LINE_PLACE,
                        hide_non_significant=True,
                        verbose=2,
                        line_height=0,
                        line_offset_to_group=0)
        annot.apply_test().annotate()

###################################################################################################

# DRAW CATEGORICAL SWARMPLOT TO SHOW OBSERVATIONS

ax = sns.stripplot(
    data=filtered_df,
    x=X_VALS,  # x axis data
    y=Y_VALS,  # y axis data
    hue=BAR_SPLIT,  # category separating the data by color
    jitter=True,
    dodge=True,  # Makes ure the dots are not plotted in the same column
    order=TISSUE_ORDER,  # specifies the order of data on the plot
    hue_order = TREATMENT_ORDER, #defines the order of the second variable on the X axis
    palette=WhiteWheel,  # defines color palette to make sure every dot is white
    edgecolor="black",  # defines the edge color of the dots
    size=3,  # defines size of dot
    linewidth=0.75,  # defines the line thickness around the white dot
    legend=False,
)

ax.set(ylim=(0, None))  # limits the y axis range
ax.set_xticklabels(ax.get_xticklabels(), rotation=AXIS_ROTATE)
ax.set_title("")
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
# ax.tick_params(axis='both', which='major', labelsize=12, width=2)
# ax.tick_params(axis='both', which='minor', width=2)
# g._legend.remove()             #removes the legend from the plot

# SHOW / SAVE THE PLOT

g.set_xlabels("")
g.set_ylabels("")

if SAVE_FIGURE:
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
plt.show()

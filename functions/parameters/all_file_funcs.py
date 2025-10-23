#!/usr/bin/env python3

"""Provides all reusable parameters for seaborn graphing"""

import sys
import os
import re
import pandas as pd
from dataclasses import dataclass

DEFAULT_COLORS = ["#A66E4A",
                    "#93B7D5",
                    "#C67FAE",
                    "#A6BE47",
                    "#D7E8BC",
                    "#F3EAC3",
                    "#98DDDF",
                    "#009499",
                    "#F7EF70",
                    "#2E5283",
                    "#F6745F",
                    "#6F8D6A",
                    "#AC6C29",
                    "#E3BD33",
                    "#DE3848",
                    "#E2552D",
                    "#6D5698",
                    "#582B36"]
DEF_LEN = len(DEFAULT_COLORS)

@dataclass
class ColorWheel:
    """A dataclass used to store information about hex codes for graphs. Has a name (str) and colors (dictionary)."""
    name: str
    colors: dict[any, str]

    def add(self,var:list[str],color:None|list[str]=None):
        """Adds a color to the wheel. If color is not specified, a color from the default wheel will be added. This code does not check syntax."""
        if color != None:
            if len(var) != len(color):
                return print("Variable list and Color list are not equal sizes.")
            else:
                for idx, value in enumerate(var):
                    self.colors[value] = color[idx]
        else:
            for value in var:
                ref = len(self.colors)
                self.colors[value] = DEFAULT_COLORS[ref%DEF_LEN]
    
    def print_colors(self):
        for key,color in self.colors.items():
            print(f"{key}: {color}\n")

    def edit(self, var:str,color:str):
        try:
            self.colors[var] = color
        except ValueError:
            print(f"Key {var} is not in current wheel. Use the add function to add a new color.")

def new_wheel(name:str="new") -> ColorWheel:
    return ColorWheel(name,{})

def dict_printer(mydictionary: dict):
    """Prints and formats the contents of a provided dictionary."""
    for key, value in mydictionary.items():
            print(f"{key}: {value}\n")

def get_default_colors() -> any:
    """Returns the default colors for the Pantone Spring Summer 2025 color scheme."""
    return print(DEFAULT_COLORS)

def get_white_wheel(DataSet: pd.DataFrame, pop_value: str = "") -> ColorWheel:
    """Generates a white color wheel based on the values in the provided DataFrame. A 'pop' value may be
    provided to remove extra data columns before processing."""
    TreatType = DataSet.copy()                          #Creates an object with a copy of all the data
    TreatType = TreatType.pop(pop_value)                #Removes pop_value from the copied data
    WhiteWheel = ColorWheel("white_wheel", {})          #Initializes a dictionary
    for Treat in TreatType: 
        WhiteWheel.colors.setdefault(Treat, '#FFFFFF')  #Sets all value defaults to white
    return WhiteWheel.colors

def get_default_wheel() -> ColorWheel:
    """Generates a ColorWheel object with the name "default" and the original color wheel provided by Sidd."""

    defColorWheel = ColorWheel("default", dict([
    ('Control', '#a0c3d9'),
    ('SPF', '#f1c4c8'),
    ('GF', '#4b81bf'),
    ('DietA', '#F6C163'),
    ('DietB', '#29636C'),
    ('ControlDiet', '#BCDBE8'),
    ('HiFiDiet', '#7C4480'),
    ('Amp', '#BA412E'),
    ('Vanc', '#A36E37'),
    ('Control_Starch', '#BCDBE8'),
    ('Control_AcStarch', '#215996'),
    ('Amp_Starch', '#BA412E'),
    ('Amp_AcStarch', '#C1AFCD'),
    ('WT', '#BCDBE8'),
    ('MHV-Y_dHE', '#B54062'),
    ('MHV-Y','#BCDBE8'),
    ('CD64-creSTING-flox','#f1c4c8'),
    ('Amp','#cc4273'),
    ('AmpHydroxybutyrate','#3ca858'),
    ('AmpTributyrin','#c1db3c'),
    ]))

    return defColorWheel

#ColorWheel = ("#88BFB2","#E37D57","#4273B2") #,"#98AD8B","#E3CBCA","#DA788E","#A36E37","#BABC4E","#C1AFCD","#675852","#F3DD96")#,"#BCDBE8","#BA412E","#879FB7","#29636C","#7C4480","#B24C87","#3A714D","#483530")
#lut = dict(zip(TreatType.unique(), ColorWheel))

def make_wheel(wheel_name:str = "new") -> ColorWheel:
    """Generate an empty ColorWheel object."""
    return ColorWheel(wheel_name, dict())

def get_data_path(filename: str) -> str:
    """Gets the file path of the current directory and appends /datasets/ to allow for file organization."""
    full_path = os.getcwd() + "/datasets/" + filename
    return full_path

def get_file_from_cmd(position: int=1,in_datasets: bool=True):
    """Opens a specified file from a command line argument. The position parameter defines which argument the
       filename is passed in."""
    if in_datasets == True:
        filename = get_data_path(sys.argv[position])
    else:
        filename = sys.argv[position]
    try:
        return open(filename, "r"), sys.argv[position]
    except FileNotFoundError:
        print("File not found. Double check spelling and/or directory path.")
        sys.exit(1)

def my_output_file(filename: str, plot_type: str ="Plot", extension: str="svg") -> str:
    """Creates a regex to rename the output file based on the original .csv file. The plot type adds the name of
       the plot to the filename, and the extension specifies what file format to save (svg, png, jpeg, or pdf)."""
    try:
        if extension in ["svg", "png", "pdf", "jpeg", "jpg"]:
            just_name = filename.split("/")
            new_name = re.sub(".csv$","_Image" + plot_type + "." + extension, just_name[::-1][0],1)
            return os.getcwd() + "/generated_images/" + new_name
    except AttributeError:
        print("_io.TextIOWrapper object has no attribute 'split'. Double check that the filename passed is a string.")
        sys.exit(1)

def format_heatmap_data(df: pd.DataFrame,two_column: bool=True):
    """Formats a loaded DataFrame into a plottable heatmap. This function assumes """



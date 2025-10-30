# GraphScripts Folder

## NOTE: YOU MUST DOWNLOAD THE WHOLE FOLDER IN ORDER FOR THIS TO WORK AS INTENDED (unless using files in 'standalone')

This is a basic overview of how this folder works. I recommend using a coding environment with this code as it will be easier to troubleshoot if things don't work as intended. I personally use VS Code, but I know Notepad++ is also a valid option. 

# Requirements
All install requirements are listed in references/requirements.txt. If you have this file, you can call `pip install -r requirements.txt` to automatically install all required packages.

# Organization
There are a number of folders in this repo that serve different purposes:

### scripts vs standalone
The `scripts` folder is a folder that utilizes the full file structure of the repo. Data used in these scripts is expected to be in the `datasets` folder, the functions used in the code are stored in `functions`, and any generated images will be automatically outputted to `generated_images`. These files are necessary for these scripts to work, and thus all of them should be downloaded together if intending to use this locally. If using `git clone`, this will happen automatically. 

The `standalone` folder is exactly as it sounds; these scripts can be downloaded individually and run without requiring any other folder. This can be useful if you are planning to edit a specific script very heavily, or in a way that may interfere with existing code architecture. Note that all datasets and generated images must be in the same directory where the file is located.

### functions
This is where all of the built-in functions for each script reside. Unless you are planning to add functions to your local code environment for these GraphScripts, there is no need to edit this folder. 

### references
These are aesthetic references as defined by the Viralogue Lab presentation aesthetic standards. All colors used in these scripts is defined via hex codes. If using the `scripts` folder, the built-in functions come pre-loaded with these, but can be adjusted to create a different order if desired.

### testing
A folder where I am keeping my scripts that aren't fully converted from Sidd's scripts. Two versions will be added upon finishing: one to `scripts` and one to `standalone`.

# Some notes and warnings:

### `plt.show()` functionality

- If you're on a Linux distribution (like Ubuntu), there's a nonzero chance that the `plt.show()` commands will not work at all. Additionally, there is also a chance that using `plt.show()` will cause saved plots to end up empty. If `debug_show_plot` is true, know that the saved figure may end up empty. (This has something to do with the way the object is initialized, but I am not at a point where I have an easy fix currently. I'll update here once I do.)

### for the `scripts` folder
- Most files have two file read-in options. The unused option should always be commented out (to avoid errors):
1) From the terminal
2) From the actual script

If you are running the script from the terminal (i.e. you type out `python3 my_script.py` into your command window), then you want to make sure the function `myfunc.get_file_from_cmd()` is un-commented. This should be un-commented by default. This function is checking your command input for parameters (like a filename), to which it then automatically imports it into the script. If I want to run `my_script.py` with the dataset `my_data.csv`, my terminal command would look like:

`python3 my_script.py my_data.csv`

Note that in both options, you should only give the title of the file, not the full path. If for some reason these scripts will get run on the HPC, option 1 is the only valid option (as it's only terminal commands).

- If you generate any images (which I believe all figure-saving commands are un-commented by default), they will be saved to the `generated-images` folder. If you move that folder, it might throw an error. 

- Not sure what a function does? In an IDE, you should be able to hover over a function and see the parameters it takes, their data types, and their expected outputs (along with a basic description of the functionality.) I've done my best to implement this for all of my functions that I've written, though some of the descriptions might not be the most...descriptive as of now. If you have questions, feel free to ask me what's up.

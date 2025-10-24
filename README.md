# GraphScripts Folder

## NOTE: YOU MUST DOWNLOAD THE WHOLE FOLDER IN ORDER FOR THIS TO WORK AS INTENDED

This is a basic overview of how this folder works. I recommend using a coding environment with this folder as it will be easier to troubleshoot if things don't work as intended. I personally use VS Code, but I know Notepad++ is also a valid option. 

To make the functions in this folder work, you must download THE ENTIRE FOLDER! The `functions` folder has a bunch of extra coding structure in it that is meant to make the main scripts easier to read/use.

# A couple of basic notes on this:

- IDE stands for Integrated Development Environment. This is software that is used to look at code, such as VS Code or Notepad++ (I reference IDEs a few times).

- When using these scripts, I have made a separate folder called `datasets`. This is where all of the scripts are looking when they expect a dataset or csv file. Be sure to upload/move them to that folder before running a script.

- Most files have two file read-in options. The unused option should always be commented out (to avoid errors):
1) From the terminal
2) From the actual script

If you are running the script from the terminal (i.e. you type out `python3 my_script.py` into your command window), then you want to make sure the function `myfunc.get_file_from_cmd()` is un-commented. This should be un-commented by default. This function is checking your command input for parameters (like a filename), to which it then automatically imports it into the script. If I want to run `my_script.py` with the dataset `my_data.csv`, my terminal command would look like:

`python3 my_script.py my_data.csv`

If you are running the script through an IDE, there are usually options for you to run the script without using the terminal. Because it has no parameters this way, you have to specify the file inside of the script. The second function for read-in should say `myfunc.get_data_path("your_file_goes_here")` where "your_file_goes_here" is replaced with the dataset. Technically this also works if you want to run from the terminal without specifying a file, but I wouldn't recommend it. 

Note that in both options, you should only give the title of the file, not the full path. If for some reason these scripts will get run on the HPC, option 1 is the only valid option (as it's only terminal commands).

- If you generate any images (which I believe all figure-saving commands are un-commented by default), they will be saved to the `generated-images` folder. If you move that folder, it might throw an error. 

- If you're on a Linux distribution (like Ubuntu), there's a nonzero chance that the `plt.show()` commands will not work at all. Additionally, there is a chance that using `plt.show()` will cause saved plots to end up empty. If `debug_show_plot` is true, know that the saved figure may end up empty.

- Not sure what a function does? In an IDE, you should be able to hover over a function and see the parameters it takes, their data types, and their expected outputs (along with a basic description of the functionality.) I've done my best to implement this for all of my functions that I've written, though some of the descriptions might not be the most...descriptive as of now. If you have questions, feel free to ask me what's up.

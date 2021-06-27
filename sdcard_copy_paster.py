# -*- coding: utf-8 -*-
"""
@author: simon

Works with multispectral images, script only works if sdcard_sorter.py
has been executed

"""

import shutil, os
import pathlib


def getsize(path):
    root_directory = pathlib.Path(path)
    bytes_path = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    return bytes_path
# gets the size of given path (default D:/DCIM)


confirm = input("The default path is set to D:/DCIM/, do you wish to continue? y or n, to change path press c:")


if confirm == "y" or confirm == "c":
    
    path = 'D:/DCIM/'
    # default path
    
    if confirm == "c":
        path = input("input the new path")
    
    print("The size of the path is {} bytes".format(getsize(path)))
    
    
    directory = os.listdir(path)
    # normal path to SD-card
    
    counter = 1
    for folder in directory:
        print("progression: working on folder {} out of {}".format(counter, len(directory)))
        if folder[-1].isnumeric():
        # if the last charater in the string is a number, we assume it we want
        # those files moved to the same folder name with no number
            dest_folder = folder[:len(folder) - 2]
            # destination folder for the files in the '_"number"' folder
            
            directory_folder = os.listdir('{}/{}'.format(path,folder))
            # current folder in the for-loop
            
            for file in directory_folder:
                if file.endswith("JPG") or file.endswith("TIF"):
                    # only moves jpg and TIF files
                    shutil.move("{}{}/{}".format(path,folder,file), "{}{}".format(path,dest_folder))
                    # moves each file from '_"number"' file to the one without number
                    
            shutil.rmtree("{}{}".format(path,folder))
            # removes empty folders with "bin", "MRK" and "obs"
            counter += 1
    print("Done")
    print("The size of the path is now {} bytes".format(getsize(path)))
    
else:
    print("You did not input a valid command (y, n or c)")
            


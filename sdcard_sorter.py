# -*- coding: utf-8 -*-
"""
@author: simon

A simple script to make all files in a directory have different names.
(Adding '_"number"' behind each file)
Usefull when sorting dronepictures.
"""

import pathlib
import os


def getsize(path):
    root_directory = pathlib.Path(path)
    bytes_path = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    return bytes_path
# gets the size in bytes of given path (default D:/DCIM)


confirm = input("The default path is set to D:/DCIM/, do you wish to continue? y or n, to change path press c:")

if confirm == "y" or confirm == "c":
    
    root_path = 'D:/DCIM/'
    # path to SD-card
    
    if confirm == "c":
        root_path = input("input the new path")
        
    print("The size of the path is {} bytes".format(getsize(root_path)))
    
      
    directory = os.listdir(root_path)
    # path to SD-card
    

    counter = 1
    for x in directory:
    # for every folder in directory to SD-card
    
        print("progression: working on folder {} out of {}".format(counter, len(directory)))
        # progression
        
        for path in pathlib.Path("{}{}".format(root_path,x)).iterdir():
            if path.is_file():
                old_name = path.stem
        # original filename
        
        
                old_extension = path.suffix
        # original file extension
        
        
                directory_1 = path.parent
        # current file location
        
                new_name = old_name + "_{}".format(counter) + old_extension
        
                path.rename(pathlib.Path(directory_1, new_name))
        # rename 'path' to 'new_name'
        
        counter += 1
    print("Done")
    print("The size of the path is now {} bytes, (should not change)".format(getsize(root_path)))
    
else:
    print("You did not input a valid command (y, n or c)")
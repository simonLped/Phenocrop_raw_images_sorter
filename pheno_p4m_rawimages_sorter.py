# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 08:26:22 2021

@author: simon
"""
import pathlib
import shutil, os


def getsize(path):
    root_directory = pathlib.Path(path)
    bytes_path = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    return bytes_path
# gets the size in bytes of given path (default D:/DCIM)


confirm = input("The default path is set to D:/DCIM/, do you wish to continue? y or n, to change path press c:")
print("""Make sure the folder structure is correct (ex: 100MEDIA, 101FPLAN, 102MEDIA, 103FPLAN, 104FPLAN, 105MEDIA),
      with 12 calibration files in the first MEDIA, 6 in the last, and 18 in the rest.""")
fields_str = input('input the fields done from first to last, (ex: masbasis, graminor, nobalyield):')
fields = fields_str.split(',')

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
    print("Done renaming files")
    print("The size of the path is now {} bytes, (should not change)".format(getsize(root_path)))
    
    ################################### sorter part 1
    path = "D:/DCIM/"
    original_dir = os.listdir(path)
    
    x = 0
    y = 1
    for folder in original_dir:
        updated_dir = os.listdir(path)
        
        if folder.endswith('MEDIA'):
            new_folder_name = fields[x] + '_cal'
            if new_folder_name in updated_dir:
                os.rename('{}{}'.format(path,folder), '{}{}'.format(path, new_folder_name + '_{}'.format(y)))
          
            else:      
                if x>0:
                    k = 0
                    folder_files = os.listdir('{}/{}'.format(path,folder))
                    old_cal_file = fields[x-1] + '_cal'
                    
                    for i in range(6):
                        shutil.move("{}{}/{}".format(path,folder,folder_files[i]), "{}{}".format(path,old_cal_file))
                #transferes 6 first files from calibration folder to previous calibration folder.
    
                os.rename('{}{}'.format(path,folder), '{}{}'.format(path, new_folder_name))
        # if folder endswith MEDIA change \foldername to fieldname_cal
            # if folder exist in updated_dir change name to fieldname_cal_y
        
        
        
        if folder.endswith('FPLAN'):
            new_folder_name = fields[x] + '_images'
            if new_folder_name in updated_dir:
                os.rename('{}{}'.format(path,folder), '{}{}'.format(path, new_folder_name + '_{}'.format(y)))
                          
            else:
                os.rename('{}{}'.format(path,folder), '{}{}'.format(path, new_folder_name))
        # if folder endswith FPLAN change foldername to fieldname_images
            # if folder exist in updated_dir change name to fieldname_images_y
        
    
    
        
        if y == len(original_dir)-1:
            break
        
        if y <= len(original_dir):
            if original_dir[y].endswith('MEDIA'):
                x += 1
        y += 1
        
        
    new_folder_name = fields[x] + '_cal'
    last_folder_files = os.listdir('{}/{}'.format(path,original_dir[-1]))
    for file in last_folder_files:
        shutil.move("{}{}/{}".format(path,original_dir[-1],file), "{}{}".format(path,new_folder_name))
    os.rmdir('{}{}'.format(path,original_dir[-1]))
    
    print('sorting part 1 is done')
    ################################### sorter part 1
    
    
    
    ################################### sorter part 2
    path = 'D:/DCIM/'
    # default path
    
    if confirm == "c":
        path = root_path
    
    
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
    ################################### sorter part 2
    
else:
    print("You did not input a valid command (y, n or c)")
    











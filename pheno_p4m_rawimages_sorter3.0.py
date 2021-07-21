#!/usr/bin/env python
# coding: utf-8

import pathlib
import shutil, os
import argparse


def getsize(path):
    root_directory = pathlib.Path(path)
    bytes_path = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    return bytes_path

################################### inputs ###################################
parser = argparse.ArgumentParser(description='add path')
parser.add_argument('--root_path', metavar='--root_path', type=str,help='enter path to data')
parser.add_argument('--fields', metavar='--fields', type=str,help='enter the fields recorded')
parser.add_argument('--cal_pics', metavar='--cal_pics', type=str,help='enter the amount of calibration pics after each flight')

args = parser.parse_args()

root_path = args.root_path
fields = args.fields
cal_pics = args.cal_pics

print('sorting the path:' + root_path + '\n')
print('given feilds:' + fields + '\n')
print('amount of calibration pics after each field, except from last' + cal_pics + '\n')

fields = fields.split(',')
# making the input fields into a list

cal_pics = cal_pics.split(',')
for i in range(0, len(cal_pics)):
    cal_pics[i] = int(cal_pics[i])
# making the input string into a list of integers
################################### inputs ###################################

print("The size of the path is {} bytes".format(getsize(root_path)))
# printing this size of the path before sorting

################################### renaming files ###################################
directory = sorted(os.listdir(root_path))
# os path

counter = 1
for x in directory:
# for every folder in the path

    print("progression: working on folder {} out of {}".format(counter, len(directory)))
    # progression
    print('In folder: {}'.format(x))
    
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
    
        print('renamed: {}, to: {}'.format(old_name, new_name))
        
    counter += 1
print("Done renaming files")
################################### renaming files ###################################

################################## renaming folders ##################################
original_dir = sorted(os.listdir(root_path))
#os path (original)

x = 0
y = 1
for folder in original_dir:
    updated_dir = sorted(os.listdir(root_path))
    
    if folder.endswith('MEDIA'): 
        new_folder_name = fields[x] + '_cal'
        if new_folder_name in updated_dir:
            new_folder_name = new_folder_name + '_{}'.format(y)
            os.rename('{}{}'.format(root_path,folder), '{}{}'.format(root_path, new_folder_name))
      
        else:      
            if x>0:
                k = 0
                folder_files = sorted(os.listdir('{}/{}'.format(root_path,folder)))
                old_cal_file = fields[x-1] + '_cal'
                
                for i in range(6*(cal_pics[x-1])):
                    shutil.move("{}{}/{}".format(root_path,folder, folder_files[i]), "{}{}".format(root_path, old_cal_file))
            #transferes 6 first files from calibration folder to previous calibration folder.
                    print('moved: {}{}/{}, to: {}{}'.format(root_path, folder, folder_files[i], root_path, old_cal_file))

            os.rename('{}{}'.format(root_path,folder), '{}{}'.format(root_path, new_folder_name))
    # if folder endswith MEDIA change \foldername to fieldname_cal
        # if folder exist in updated_dir change name to fieldname_cal_y
    
    
    
    if folder.endswith('FPLAN'):
        new_folder_name = fields[x] + '_images'
        if new_folder_name in updated_dir:
            new_folder_name = new_folder_name + '_{}'.format(y)
            os.rename('{}{}'.format(root_path,folder), '{}{}'.format(root_path, new_folder_name))
                      
        else:
            os.rename('{}{}'.format(root_path,folder), '{}{}'.format(root_path, new_folder_name))
    # if folder endswith FPLAN change foldername to fieldname_images
        # if folder exist in updated_dir change name to fieldname_images_y
    


    
    if y == len(original_dir)-1:
        break
    
    if y <= len(original_dir):
        if original_dir[y].endswith('MEDIA'):
            x += 1
    y += 1
    
    print('renamed: {}{}, to: {}{}'.format(root_path, folder, root_path, new_folder_name))
    
    
new_folder_name = fields[x] + '_cal'
last_folder_files = sorted(os.listdir('{}/{}'.format(root_path,original_dir[-1])))
for file in last_folder_files:
    shutil.move("{}{}/{}".format(root_path,original_dir[-1],file), "{}{}".format(root_path,new_folder_name))
    print('moved: {}{}/{}, to: {}{}'.format(root_path, original_dir[-1], file, root_path, new_folder_name))
os.rmdir('{}{}'.format(root_path, original_dir[-1]))
print('deleted: {}{}'.format(root_path, original_dir[-1]))


print('done renaming folders')
################################## renaming folders ##################################

#################################### moving files ####################################
directory = sorted(os.listdir(root_path))
# os path (sorted)

counter = 1
for folder in directory:
    print("progression: working on folder {} out of {}".format(counter, len(directory)))
    if folder[-1].isnumeric():
    # if the last charater in the string is a number, we assume it we want
    # those files moved to the same folder name with no number
        dest_folder = folder[:len(folder) - 2]
        # destination folder for the files in the '_"number"' folder
        
        directory_folder = sorted(os.listdir('{}/{}'.format(root_path,folder)))
        # current folder in the for-loop
        
        for file in directory_folder:
            if file.endswith("JPG") or file.endswith("TIF"):
                # only moves jpg and TIF files
                shutil.move("{}{}/{}".format(root_path, folder, file), "{}{}".format(root_path,dest_folder))
                # moves each file from '_"number"' file to the one without number
                print('moved: {}{}/{}, to: {}{}'.format(root_path, folder, file, root_path, dest_folder))

        shutil.rmtree("{}{}".format(root_path,folder))
        print('deleted: {}{}'.format(root_path, folder))
        # removes empty folders with "bin", "MRK" and "obs"
        counter += 1
print("All done")
#################################### moving files ####################################

print("The size of the  is now {} bytes".format(getsize(root_path)))
    











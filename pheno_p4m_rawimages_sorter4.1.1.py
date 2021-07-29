#!/usr/bin/env python
# coding: utf-8

import pathlib
import shutil, os
import argparse
from tqdm import tqdm


################################### inputs ###################################
parser = argparse.ArgumentParser(description='add path')
parser.add_argument('--input_path', metavar='--input_path', type=str,help='enter path to data')
parser.add_argument('--fields', metavar='--fields', type=str,help='enter the fields recorded')
parser.add_argument('--cal_pics', metavar='--cal_pics', type=str, default='not given',help='enter the amount of calibration pics after each flight')

args = parser.parse_args()

input_path = args.input_path
fields = args.fields
cal_pics = args.cal_pics

print('sorting the path:' + input_path)
print('given feilds:' + fields)
print('amount of calibration pics after each field, except from last: ' + cal_pics + '\n')

fields_str = fields
fields = fields.split(',')
fields = [s.strip() for s in fields] 
# making the input fields into a list

if cal_pics == 'not given':
    cal_pics = list()
    fields_amount = len(fields)
    for i in range(fields_amount-1):
        cal_pics.append(1)
else:
    cal_pics_str = cal_pics
    cal_pics = cal_pics.split(',')
    for i in range(0, len(cal_pics)):
        cal_pics[i] = int(cal_pics[i])
# making the input string into a list of integers

input_path = input_path.strip()
if input_path[-1] != '/':
    input_path = input_path + '/'

rapport_file = open(input_path + 'rapport.txt', 'a')
rapport_file.write('sorting the path:' + input_path + '\n' + 'given fields:' + fields_str + '\n')
################################### inputs ###################################

################################### renaming files ###################################
directory = sorted(os.listdir(input_path))
# os path
directory.remove('rapport.txt')

rapport_file.write('folders in directory:' + '\n')

for folder in directory:
    rapport_file.write(folder + '\n')
        

counter = 1
for folder in tqdm(directory):
# for every folder in the path
    current_path = '{}{}'.format(input_path,folder)
    if os.path.isdir(current_path):
        
        rapport_file.write( "progression: working on folder {} out of {}".format(counter, len(directory)) + '\n' + 'In folder: {}'.format(folder) + '\n')
        
        for path in pathlib.Path("{}{}".format(input_path,folder)).iterdir():
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
        
            rapport_file.write('renamed: {}{}/{}, to: {}{}/{}'.format(input_path, folder, old_name, input_path, folder, new_name) + '\n')
            
    counter += 1

rapport_file.write("Done renaming files\n")
################################### renaming files ###################################

################################## renaming folders ##################################
original_dir = sorted(os.listdir(input_path))
original_dir.remove('rapport.txt')
#os path (original)

x = 0
y = 1
for folder in tqdm(original_dir):
    updated_dir = sorted(os.listdir(input_path))
    updated_dir.remove('rapport.txt')
    
    if folder.endswith('MEDIA'): 
        new_folder_name = fields[x] + '_cal'
        if new_folder_name in updated_dir:
            new_folder_name = new_folder_name + '_{}'.format(y)
            os.rename('{}{}'.format(input_path,folder), '{}{}'.format(input_path, new_folder_name))
      
        else:      
            if x>0:
                k = 0
                folder_files = sorted(os.listdir('{}/{}'.format(input_path,folder)))
                old_cal_file = fields[x-1] + '_cal'
                
                for i in range(6*(cal_pics[x-1])):
                    shutil.move("{}{}/{}".format(input_path,folder, folder_files[i]), "{}{}".format(input_path, old_cal_file))
            #transferes 6 first files from calibration folder to previous calibration folder.
                    rapport_file.write('moved: {}{}/{}, to: {}{}'.format(input_path, folder, folder_files[i], input_path, old_cal_file + '\n'))

            os.rename('{}{}'.format(input_path,folder), '{}{}'.format(input_path, new_folder_name))
    # if folder endswith MEDIA change \foldername to fieldname_cal
        # if folder exist in updated_dir change name to fieldname_cal_y
    
    if folder.endswith('FPLAN'):
        new_folder_name = fields[x] + '_images'
        if new_folder_name in updated_dir:
            new_folder_name = new_folder_name + '_{}'.format(y)
            os.rename('{}{}'.format(input_path,folder), '{}{}'.format(input_path, new_folder_name))
        else:
            os.rename('{}{}'.format(input_path,folder), '{}{}'.format(input_path, new_folder_name))
    # if folder endswith FPLAN change foldername to fieldname_images
        # if folder exist in updated_dir change name to fieldname_images_y
    
    if y == len(original_dir)-1:
        break
    
    if y <= len(original_dir):
        if original_dir[y].endswith('MEDIA'):
            x += 1
    y += 1

    rapport_file.write('renamed: {}{}, to: {}{}'.format(input_path, folder, input_path, new_folder_name) + '\n')
    
    
new_folder_name = fields[x] + '_cal'
last_folder_files = sorted(os.listdir('{}/{}'.format(input_path,original_dir[-1])))
for file in last_folder_files:
    shutil.move("{}{}/{}".format(input_path,original_dir[-1],file), "{}{}".format(input_path,new_folder_name))

    rapport_file.write('moved: {}{}/{}, to: {}{}'.format(input_path, original_dir[-1], file, input_path, new_folder_name) + '\n')
    
os.rmdir('{}{}'.format(input_path, original_dir[-1]))

rapport_file.write('deleted: {}{}'.format(input_path, original_dir[-1]) + '\n')
rapport_file.write('done renaming folders' + '\n')
################################## renaming folders ##################################

#################################### moving files ####################################
directory = sorted(os.listdir(input_path))
directory.remove('rapport.txt')
# os path (sorted)
# hides the rapport from the sorter

counter = 1
counter_2 = 1
for folder in tqdm(directory):
    
    if folder[-1].isnumeric():
        
        rapport_file.write("progression: working on folder {} out of {}".format(counter_2, len(directory)) + '\n')
        rapport_file.write('In folder: {}'.format(folder) + '\n')
        
    # if the last charater in the string is a number, we move files to the folder with no number
        x = 0
        length = len(folder)
        last_char = folder[length-1-x]
        
        while last_char.isalpha() == False:
            x += 1
            last_char = folder[length-1-x]
            
        dest_folder = folder[:len(folder) - x] 
        
        # destination folder for the files in the '_"number"' folder
        
        directory_folder = sorted(os.listdir('{}/{}'.format(input_path,folder)))
        # current folder in the for-loop
        
        for file in directory_folder:
            if file.endswith("JPG") or file.endswith("TIF"):
                # only moves jpg and TIF files
                shutil.move("{}{}/{}".format(input_path, folder, file), "{}{}".format(input_path,dest_folder))
                # moves each file from '_"number"' file to the one without number

                rapport_file.write('moved: {}{}/{}, to: {}{}'.format(input_path, folder, file, input_path, dest_folder) + '\n')

        shutil.rmtree("{}{}".format(input_path,folder))

        rapport_file.write('deleted: {}{}'.format(input_path, folder) + '\n')
        
        # removes empty folders with "bin", "MRK" and "obs"
        counter += 1
    counter_2 += 1
#################################### moving files ####################################

rapport_file.write("All done" + '\n')
rapport_file.close()
    











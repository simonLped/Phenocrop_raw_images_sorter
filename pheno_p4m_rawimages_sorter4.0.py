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

print('sorting the path:' + root_path)
print('given feilds:' + fields)
print('amount of calibration pics after each field, except from last: ' + cal_pics + '\n')

fields_str = fields
fields = fields.split(',')
fields = [s.strip() for s in fields]
# making the input fields into a list

cal_pics_str = cal_pics
cal_pics = cal_pics.split(',')
for i in range(0, len(cal_pics)):
    cal_pics[i] = int(cal_pics[i])
# making the input string into a list of integers

if root_path[-1] != '/':
    root_path = root_path + '/'
    
with open(root_path + 'rapport.txt', 'a') as the_file:
    the_file.write('sorting the path:' + root_path + '\n' + 'given fields:' + fields_str + '\n' + 'amount of calibration pics after each field, except from last' + cal_pics_str + '\n')
################################### inputs ###################################

print("The size of the path is {} bytes".format(getsize(root_path)))
# printing this size of the path before sorting

with open(root_path + 'rapport.txt', 'a') as the_file:
    the_file.write("The size of the path is {} bytes".format(getsize(root_path)) + '\n')

################################### renaming files ###################################
directory = sorted(os.listdir(root_path))
# os path
directory.remove('rapport.txt')

with open(root_path + 'rapport.txt', 'a') as the_file:
    the_file.write('folders in directory:' + '\n')
for folder in directory:
    with open(root_path + 'rapport.txt', 'a') as the_file:
        the_file.write(folder + '\n')
        

counter = 1
for x in directory:
# for every folder in the path
    current_path = '{}{}'.format(root_path,x)
    if os.path.isdir(current_path):
        print("progression: working on folder {} out of {}".format(counter, len(directory)))
        # progression
        print('In folder: {}'.format(x))
        
        with open(root_path + 'rapport.txt', 'a') as the_file:
            the_file.write( "progression: working on folder {} out of {}".format(counter, len(directory)) + '\n' + 'In folder: {}'.format(x) + '\n')
        
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
        
            print('renamed: {}{}/{}, to: {}{}/{}'.format(root_path, x, old_name, root_path, x, new_name))
            
            with open(root_path + 'rapport.txt', 'a') as the_file:
                the_file.write('renamed: {}{}/{}, to: {}{}/{}'.format(root_path, x, old_name, root_path, x, new_name) + '\n')
            
    counter += 1
print("Done renaming files")

with open(root_path + 'rapport.txt', 'a') as the_file:
    the_file.write("Done renaming files\n")
################################### renaming files ###################################

################################## renaming folders ##################################
original_dir = sorted(os.listdir(root_path))
original_dir.remove('rapport.txt')
#os path (original)

x = 0
y = 1
for folder in original_dir:
    updated_dir = sorted(os.listdir(root_path))
    updated_dir.remove('rapport.txt')
    
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
    
    with open(root_path + 'rapport.txt', 'a') as the_file:
        the_file.write('renamed: {}{}, to: {}{}'.format(root_path, folder, root_path, new_folder_name) + '\n')
    
    
new_folder_name = fields[x] + '_cal'
last_folder_files = sorted(os.listdir('{}/{}'.format(root_path,original_dir[-1])))
for file in last_folder_files:
    shutil.move("{}{}/{}".format(root_path,original_dir[-1],file), "{}{}".format(root_path,new_folder_name))
    
    print('moved: {}{}/{}, to: {}{}'.format(root_path, original_dir[-1], file, root_path, new_folder_name))
    
    with open(root_path + 'rapport.txt', 'a') as the_file:
        the_file.write('moved: {}{}/{}, to: {}{}'.format(root_path, original_dir[-1], file, root_path, new_folder_name) + '\n')
    
os.rmdir('{}{}'.format(root_path, original_dir[-1]))
print('deleted: {}{}'.format(root_path, original_dir[-1]))

with open(root_path + 'rapport.txt', 'a') as the_file:
        the_file.write('deleted: {}{}'.format(root_path, original_dir[-1]) + '\n')
    
print('done renaming folders')

with open(root_path + 'rapport.txt', 'a') as the_file:
        the_file.write('done renaming folders' + '\n')
################################## renaming folders ##################################

#################################### moving files ####################################
directory = sorted(os.listdir(root_path))
directory.remove('rapport.txt')
# os path (sorted)
# hides the rapport from the sorter

counter = 1
counter_2 = 1
for folder in directory:
    
    if folder[-1].isnumeric():
        
        print("progression: working on folder {} out of {}".format(counter_2, len(directory)))
        print('In folder: {}'.format(folder))
    
        with open(root_path + 'rapport.txt', 'a') as the_file:
            the_file.write("progression: working on folder {} out of {}".format(counter_2, len(directory)) + '\n')
            the_file.write('In folder: {}'.format(folder) + '\n')
        
    # if the last charater in the string is a number, we move files to the folder with no number
        x = 0
        length = len(folder)
        last_char = folder[length-1-x]
        
        while last_char.isalpha() == False:
            x += 1
            last_char = folder[length-1-x]
            
        dest_folder = folder[:len(folder) - x] 
        
        # destination folder for the files in the '_"number"' folder
        
        directory_folder = sorted(os.listdir('{}/{}'.format(root_path,folder)))
        # current folder in the for-loop
        
        for file in directory_folder:
            if file.endswith("JPG") or file.endswith("TIF"):
                # only moves jpg and TIF files
                shutil.move("{}{}/{}".format(root_path, folder, file), "{}{}".format(root_path,dest_folder))
                # moves each file from '_"number"' file to the one without number
                print('moved: {}{}/{}, to: {}{}'.format(root_path, folder, file, root_path, dest_folder))
                
                with open(root_path + 'rapport.txt', 'a') as the_file:
                    the_file.write('moved: {}{}/{}, to: {}{}'.format(root_path, folder, file, root_path, dest_folder) + '\n')

        shutil.rmtree("{}{}".format(root_path,folder))
        print('deleted: {}{}'.format(root_path, folder))
        
        with open(root_path + 'rapport.txt', 'a') as the_file:
                    the_file.write('deleted: {}{}'.format(root_path, folder) + '\n')
        
        # removes empty folders with "bin", "MRK" and "obs"
        counter += 1
    counter_2 += 1
print("All done")
#################################### moving files ####################################

print("The size of the  is now {} bytes".format(getsize(root_path)))
    
with open(root_path + 'rapport.txt', 'a') as the_file:
    the_file.write("All done" + '\n')
    the_file.write("The size of the  is now {} bytes".format(getsize(root_path)) + '\n')
    











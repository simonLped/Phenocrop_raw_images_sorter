# -*- coding: utf-8 -*-
"""

@author: simon

works with p4m, run sdcard_sorter.py first
"""

import shutil, os

print('Make sure the folder structure is correct (ex: 100MEDIA, 101FPLAN, 102MEDIA, 103FPLAN, 104FPLAN, 105MEDIA)')
fields_str = input('input the fields done from first to last, (ex: graminor, nobalyield, masbasis):')
fields = fields_str.split(',')

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
        print('stopp her!')
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

        
    
    
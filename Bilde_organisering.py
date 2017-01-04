# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 18:30:44 2017

@author: Gunvor
"""

import os, shutil
import calendar
from PIL import Image

def get_date_taken(path):
    """
    Returns the date of the origin of the image, or False if the date can
    not be found.
    """
    try:
        return Image.open(path)._getexif()[36867]
    except:
        return False

def rename(source, filename, destination):
    """
    Examines whether there already exists a file of the same name in the
    destination directory. If such a file exists, an index is appended at the
    end of the file that is to be moved to the same directory. 
    Returns the destination path of the file, containing the new filename.
    """
    i = 1
    
    file_destination = os.path.join(destination,filename)
    filename_info = filename.split('.')
    
    while os.path.isfile(file_destination):
        filename = filename_info[0] + '(' + str(i) + ').' + filename_info[1]
        i = i + 1
        file_destination = os.path.join(destination,filename)
        
    return file_destination

# PATH TO SOURCE AND DESTINATION
to_import = r'C:\Users\Gunvor\Desktop\DCIM'
#to_import = r'C:\Users\Gunvor\Pictures\Testmappe'
imported_pictures = r'C:\Users\Gunvor\Pictures\Importert'

# CREATE FOLDER 'Diverse' TO HANDLE PICTURES WITHOUT DATE
diverse = os.path.join(imported_pictures,'Diverse')
os.makedirs(diverse)

# COPY ALL PICTURES FROM SOURCE TO DESTINATION
print('Copying files')
copied = []
for dirpath, dirnames, filenames in os.walk(to_import):
    for filename in filenames:
        filepath = os.path.join(dirpath,filename)
        destination_path = rename(dirpath, filename, imported_pictures)
        shutil.copy(filepath, destination_path)
        copied.append(destination_path)

# ORGANIZE ALL PICTURES INTO YEAR AND MONTH FOLDERS + 'Diverse'
print('Moving to directories')
for filepath in copied:
    information = get_date_taken(filepath)
    
    if information:
        year = information[:4]
        month = int(information[5:7])
        destination_path = os.path.join(imported_pictures, year, str(month) + '_' + calendar.month_name[month])            
        
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        shutil.move(filepath, destination_path)
    else:
        shutil.move(filepath, diverse)




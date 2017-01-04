# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 18:30:44 2017

@author: Gunvor
"""

import os, shutil
import calendar
from PIL import Image

def folder_name(month):
    """
    Returns a folder name based on the month.
    """
    return str(month) + '_' + calendar.month_name[month]

def get_date_taken(path):
    """
    Returns the date of the origin of the image, or False if the date can
    not be found.
    """
    try:
        return Image.open(path)._getexif()[36867]
    except:
        return False

def rename(source, filename, destination, format_str = '({}).'):
    """
    Examines whether there already exists a file of the same name in the
    destination directory. If such a file exists, an index is appended at the
    end of the file that is to be moved to the same directory. 
    Returns the destination path of the file, containing the new filename.
    """
    i = 1
    file_destination = os.path.join(destination,filename)
    first, last = filename.split('.')
    
    while os.path.isfile(file_destination):
        filename = first + format_str.format(i) + last                 
        file_destination = os.path.join(destination,filename)
        i += 1
        
    return file_destination

    
if __name__ == '__main__':
    # PATH TO SOURCE AND DESTINATION
    IMPORT_PATH = r'C:\Users\Gunvor\Desktop\DCIM'
    #to_import = r'C:\Users\Gunvor\Pictures\Testmappe'
    IMPORTED_PICS = r'C:\Users\Gunvor\Pictures\Importert'
    
    # CREATE FOLDER 'Diverse' TO HANDLE PICTURES WITHOUT DATE
    diverse = os.path.join(IMPORTED_PICS,'Diverse')
    os.makedirs(diverse)
    
    # COPY ALL PICTURES FROM SOURCE TO DESTINATION
    print('Copying files')
    copied = []
    for dirpath, dirnames, filenames in os.walk(IMPORT_PATH):
        for filename in filenames:
            filepath = os.path.join(dirpath,filename)
            destination_path = rename(dirpath, filename, IMPORTED_PICS)
            shutil.copy(filepath, destination_path)
            copied.append(destination_path)
    
    # ORGANIZE ALL PICTURES INTO YEAR AND MONTH FOLDERS + 'Diverse'
    print('Moving to directories')
    for filepath in copied:
        information = get_date_taken(filepath)
        
        if information:
            year = information[:4]
            month = int(information[5:7])
            destination_path = os.path.join(IMPORTED_PICS, year, folder_name(month))            
            
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
    
            shutil.move(filepath, destination_path)
        else:
            shutil.move(filepath, diverse)
            
    print('Biip, biip, blop. Finished.\n \
    Processed {} images.'.format(len(copied)))




        
        
        
        
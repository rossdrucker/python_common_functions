# -*- coding: utf-8 -*-
"""
@author: Ross Drucker
"""

import os

def find_files(file_type, path_a = os.getcwd(), spec_val = '', with_file_path = False):
    '''
    Find all files in the current directory that match a specified extension (e.g. "Find all .csv files")
        
    file_type: the type of file to look for
    path_a: the directory in which to look for the files
    spec_val: make sure that the file contains a special character, helps with file selection
    with_file_path: only a True of False, whether you want the whole file path or not
    '''
	
    file_list = []
	
    for file in os.listdir(path_a):
        
        if file.endswith(file_type) and spec_val in file:
            
            if with_file_path:
                file_list.append(os.path.join(path_a, file))
                
            else:
                file_list.append(file)
	
    return file_list

def rename_move_file(current_file_name, current_file_path, new_file_name = [], new_file_path = []):
    '''
    Takes in a file and will move it from the old directory to the new one
    '''
    
    # If the new file name is a list, it implies we are renaming a file
    if new_file_name == []:
        new_file_name = current_file_name
        
    # If the new file path is a list, it implies we are keeping the file in the same location
    if new_file_path == []:
        new_file_path = current_file_path
        
    # Move/rename the file
    old_file = current_file_path + '\\' + current_file_name
    new_file = new_file_path + '\\' + new_file_name
    os.rename(old_file, new_file)












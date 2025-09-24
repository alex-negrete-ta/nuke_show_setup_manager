
import os
import nuke

def grab_root_name(path):
    '''
    Description:
    Grab the given path and get the last two words.

    Input:
    path(str): Full path of where the shot will be set.

    Output:
    root_folders(list): List of the last two strings needed.
    '''
    # Use os.path.normpath() to normalize the path and then split it
    dir_list = os.path.normpath(path).split(os.path.sep)
    
    # Grab the last two elements from the list
    root_folders = dir_list[-2:]
    
    
    #print(root_folders)
    #print(dir_list)
    return root_folders

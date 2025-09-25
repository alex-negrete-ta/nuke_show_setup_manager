import nuke
import nukescripts
import os
import re

def read_files(show_path):
    '''
    Description:
    It reads the files from the show path and ingests it into nuke.

    Input:
    show_path(dict): A dictionary with the folder structure of the show.

    Output:
    read_node(dict): A node in nuke with the read information.
    first_frame(int): The first frame of the plate.
    last_frame(int): The last frame of the plate.
    '''
       # Set the path to my read folder.
    footage_path_folder = show_path['comp']['02_footage']['01_plate']
    
    # Get the sequence information directly from the folder
    sequence = nuke.getFileNameList(footage_path_folder)
    sequence_info = sequence[0]  # e.g., 'test.####.exr 1-50'

    # Parse the sequence info
    parts = sequence_info.split()
    footage_name = parts[0]  # 'test.####.exr'
    range_part = parts[1]    # '1-50'

    # Get the frame range
    first_frame, last_frame = map(int, range_part.split('-'))

    # Build the full path
    file_path = os.path.join(footage_path_folder, footage_name)
    
    # Normalize path to Nuke standards
    norm_path = os.path.normpath(file_path)
    nuke_read_path = norm_path.replace(os.path.sep, '/')

    # Setting the read file.
    read_node = nuke.createNode('Read')
    read_node['file'].setValue(nuke_read_path)
    read_node['raw'].setValue(True)  # Should be boolean, not string
    
    # Manually set the frame range on the Read node
    read_node['first'].setValue(first_frame)
    read_node['last'].setValue(last_frame)
    
    # Force reload
    read_node['reload'].execute()


    return read_node, first_frame, last_frame
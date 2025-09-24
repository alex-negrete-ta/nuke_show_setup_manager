import nuke
import os

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
    footage_path = os.listdir(footage_path_folder)
    footage_name=footage_path[0]
    file_path = os.path.join(footage_path_folder,footage_name)
    # Normalizing the path to nukes standards.
    norm_path = os.path.normpath(file_path)
    nuke_read_path = norm_path.replace(os.path.sep,'/')
    # Setting the read file.
    read_node = nuke.createNode('Read')
    read_node['raw'].setValue('True')
    read_node['file'].setValue(nuke_read_path)

    # Get the first frame, and last frame information.
    first_frame = read_node['first'].value()
    last_frame = read_node['last'].value()


    return read_node,first_frame,last_frame
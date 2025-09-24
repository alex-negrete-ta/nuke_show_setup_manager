import os
import nuke

# Searchs, verifys and if not creates a folder strucuture and deletes the rest.
def create_folder_structure(shot_path):
    '''
    Description:
    Verifies the folder you selected and goes and verifies folder, creates if it doesn't exist and 
    deletes the rest.

    Input:
    root_path (str): the folder path directory of the root project.

    Output:
    folder_strucutre (dir): Directory of all the folders needed.
    '''
    # Establish the folders and values needed to create.
    folder_structure = {} 
    comp_root_folders = [
                        '01_scripts',
                        '02_footage',
                        '03_assets',
                        '04_renders'
                       ] 
    
    footage_comp_folder = [
                            '01_plate',
                            '02_ref_mov',
                            '03_onset_ref',
                            '04_LUT'
                           ] 
    
    render_comp_folder = [
                        '01_mov',
                        '02_exr'
                        ]
     
    try:
         # Create the comp folder if it doesn't exist.
        comp_path = os.path.join(shot_path, 'comp')
        os.makedirs(comp_path, exist_ok=True)
        print(f'Created main comp directory: {comp_path}')
        folder_structure['comp'] = {}

        # Loop through the comp folders creating the folders in comp_root_folders.
        for required_folder in comp_root_folders:
            folder_path = os.path.join(comp_path, required_folder)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Verified or created: {folder_path}")
            
            # Specific sub-folder creation for '02_footage'
            if required_folder == '02_footage':
                folder_structure['comp'][required_folder] = {}
                for sub_folder in footage_comp_folder:
                    sub_path = os.path.join(folder_path, sub_folder)
                    os.makedirs(sub_path, exist_ok=True)
                    print(f"  Created footage subfolder: {sub_path}")
                    folder_structure['comp'][required_folder][sub_folder] = sub_path
            
            elif required_folder == '04_renders':
                folder_structure['comp'][required_folder] = {}
                for sub_folder in render_comp_folder:
                    sub_path = os.path.join(folder_path, sub_folder)
                    os.makedirs(sub_path, exist_ok=True)
                    print(f"  Created footage subfolder: {sub_path}")
                    folder_structure['comp'][required_folder][sub_folder] = sub_path

            else:
                #Adds it to a dictionary for non-footage folders
                folder_structure['comp'][required_folder] = folder_path
            
        

    
    except PermissionError as e:
        #nuke.message(f'Error in creating the folder structure: {e}')
        return False
    
    return folder_structure

def main (path):
    folder_structure = create_folder_structure(path)
    return folder_structure
    
    
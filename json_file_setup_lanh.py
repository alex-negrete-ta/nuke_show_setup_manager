import os
import nuke

def get_json_path(name,root):
    '''
    Description:
    Get the root directory, and create a json file path.

    Input:
    name (str): The name of the presets file.
    root (str): 

    Output:
    json_nuke_path (str): The path of the json file with nuke slashes.
    '''
    # Sets the json name. 
    json_name = f'{name}.json'
    print (json_name)
    print(name)
    
    # This will now create a folder like C:\Users\YourUsername\presets
    presets_folder = os.path.join(root, 'presets') 
    
    print(json_name)
    print(name)
    
    # Ensure the directory exists before returning the path
    os.makedirs(presets_folder, exist_ok=True)
    
    json_path = os.path.join(presets_folder, json_name)

    json_nuke_path = json_path.replace(os.path.sep,'/')
    
    print(json_nuke_path)
    return json_nuke_path
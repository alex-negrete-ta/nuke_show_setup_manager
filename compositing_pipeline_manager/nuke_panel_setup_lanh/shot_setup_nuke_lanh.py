import nuke
import os


def setup_new_script(show_path, show_specifications):
    """
    Description:
    Sets up a new nuke file with the right naming conventions and colorspaces.

    Input:
    show_path(str): The root folder of the show comp.
    show_specifications(dir): A dictionary with all the show specs

    Output:

    """

    # Create folder path if it doesnt exist.
    folder_structure = create_folder_structure(show_path)

    # Get the paths needed
    exr_path = folder_structure["comp"]["04_renders"]["02_exr"]
    mov_path = folder_structure["comp"]["04_renders"]["01_mov"]
    nk_file_path = show_specifications["nuke_file"]

    # Get the directory from the file path
    output_dir = os.path.dirname(nk_file_path)

    # Create the directory if it doesn't exist
    # The 'exist_ok=True' flag prevents an error if the directory already exists
    os.makedirs(output_dir, exist_ok=True)

    # Clear the current script to start fresh
    nuke.scriptClear()

    # Read plate
    footage, first_frame, last_frame = read_files(folder_structure)

    # Get the root node
    root = nuke.root()

    # Set up the file values as objects.
    aspect_ratio = show_specifications["aspect_ratio"]
    # color_space = show_specifications['color_space']
    # frame_range = show_specifications['frame_range']
    fps = show_specifications["fps"]

    # Set project format
    root["format"].setValue(aspect_ratio)

    # Set frame range
    root["first_frame"].setValue(int(first_frame))
    root["last_frame"].setValue(int(last_frame))

    # Set FPS
    root["fps"].setValue(float(fps))

    nuke.createNode("Viewer")

    # Set up the viewe settings
    set_up_viewer_color(show_specifications)

    # footage = nuke.createNode('Constant')
    footage.hideControlPanel()

    # Create an OCIO input color space.
    ocio_input = nuke.createNode("OCIOColorSpace")
    ocio_input["in_colorspace"].setValue(show_specifications["screen_color"])
    ocio_input["out_colorspace"].setValue(show_specifications["workspace_color"])
    ocio_input.setXpos(footage.xpos())
    ocio_input.setYpos(footage.ypos() + 100)
    ocio_input.setInput(0, footage)
    ocio_input.hideControlPanel()

    # Set the Backdrop for the input.
    input_backdrop = nuke.createNode("BackdropNode")
    input_backdrop["label"].setValue("Input")
    input_backdrop["note_font_size"].setValue(36)
    input_backdrop.setXpos(footage.xpos() - 25)
    input_backdrop.setYpos(footage.ypos() - 75)
    input_backdrop["bdwidth"].setValue(200)
    input_backdrop["bdheight"].setValue(200)
    input_backdrop.hideControlPanel()

    # Change the colorspace back to screen colorspace
    ocio_output = nuke.createNode("OCIOColorSpace")
    ocio_output["in_colorspace"].setValue(show_specifications["workspace_color"])
    ocio_output["out_colorspace"].setValue(show_specifications["screen_color"])
    ocio_output.setXpos(ocio_input.xpos())
    ocio_output.setYpos(ocio_input.ypos() + 500)
    ocio_output.setInput(0, ocio_input)
    ocio_output.hideControlPanel()

    # Remove the Alpha from the final renders.
    remove_alpha = nuke.createNode("Remove")
    remove_alpha["channels"].setValue("Alpha")
    remove_alpha.setXpos(ocio_output.xpos())
    remove_alpha.setYpos(ocio_output.ypos() + 50)
    remove_alpha.setInput(0, ocio_output)
    remove_alpha.hideControlPanel()

    # Create dots to adjust the reformat of the HD.
    dot1 = nuke.createNode("Dot")
    dot1.setXpos(remove_alpha.xpos() + 34)
    dot1.setYpos(remove_alpha.ypos() + 100)
    dot1.setInput(0, remove_alpha)
    dot1.hideControlPanel()

    dot2 = nuke.createNode("Dot")
    dot2.setXpos(dot1.xpos() + 350)
    dot2.setYpos(dot1.ypos())
    dot2.setInput(0, dot1)
    dot2.hideControlPanel()

    # Reformat both to HD playblast
    reformat_hd = nuke.createNode("Reformat")
    reformat_hd["format"].setValue("HD_1080")
    reformat_hd.setYpos(dot2.ypos() + 100)
    reformat_hd.setXpos(dot2.xpos() - 34)
    reformat_hd.setInput(0, dot2)
    reformat_hd.hideControlPanel()

    # Set up the correct paths for the files
    mov_path_file = os.path.join(mov_path, show_specifications["mov_name"])
    mov_norm_path = os.path.normpath(mov_path_file)
    mov_correct_path = mov_norm_path.replace(os.path.sep, "/")
    exr_path_file = os.path.join(exr_path, show_specifications["exr_name"])
    exr_norm_path = os.path.normpath(exr_path_file)
    exr_correct_path = exr_norm_path.replace(os.path.sep, "/")

    # Create a Write node for mov
    write_mov_node = nuke.createNode("Write")
    write_mov_node["file"].setValue(mov_correct_path)
    write_mov_node["file_type"].setValue("mov")
    write_mov_node.setYpos(reformat_hd.ypos() + 50)
    write_mov_node.setXpos(reformat_hd.xpos())
    write_mov_node.setInput(0, reformat_hd)
    write_mov_node.hideControlPanel()

    # Create MOV background
    backdrop_mov = nuke.createNode("BackdropNode")
    backdrop_mov["label"].setValue("MOV")
    backdrop_mov["note_font_size"].setValue(36)
    backdrop_mov.setXpos(reformat_hd.xpos() - 100)
    backdrop_mov.setYpos(reformat_hd.ypos() - 100)
    backdrop_mov["bdwidth"].setValue(200)
    backdrop_mov["bdheight"].setValue(200)
    backdrop_mov.hideControlPanel()

    # Reformat to final resolution.
    reformat = nuke.createNode("Reformat")
    reformat.setXpos(dot1.xpos() - 34)
    reformat.setYpos(dot1.ypos() + 100)
    reformat.setInput(0, dot1)
    reformat.hideControlPanel()

    # Create a Write node for exr
    write_exr_node = nuke.createNode("Write")
    write_exr_node["file"].setValue(exr_correct_path)
    write_exr_node["file_type"].setValue("exr")
    write_exr_node.setInput(0, reformat)
    write_exr_node.setYpos(reformat.ypos() + 50)
    write_exr_node.setXpos(reformat.xpos())
    write_exr_node.hideControlPanel()

    # Create exr background
    backdrop_exr = nuke.createNode("BackdropNode")
    backdrop_exr["label"].setValue("EXR")
    backdrop_exr["note_font_size"].setValue(36)
    backdrop_exr.setXpos(reformat.xpos() - 100)
    backdrop_exr.setYpos(reformat.ypos() - 100)
    backdrop_exr["bdwidth"].setValue(200)
    backdrop_exr["bdheight"].setValue(200)
    backdrop_exr.hideControlPanel()

    # Now, you can safely save the Nuke file
    nuke.scriptSaveAs(nk_file_path)

    return


# Searchs, verifys and if not creates a folder strucuture and deletes the rest.
def create_folder_structure(shot_path):
    """
    Description:
    Verifies the folder you selected and goes and verifies folder, creates if it doesn't exist and
    deletes the rest.

    Input:
    root_path (str): the folder path directory of the root project.

    Output:
    folder_strucutre (dir): Directory of all the folders needed.
    """
    # Establish the folders and values needed to create.
    folder_structure = {}
    comp_root_folders = ["01_scripts", "02_footage", "03_assets", "04_renders"]

    footage_comp_folder = ["01_plate", "02_ref_mov", "03_onset_ref", "04_LUT"]

    render_comp_folder = ["01_mov", "02_exr"]

    # Create the comp folder if it doesn't exist.
    comp_path = os.path.join(shot_path, "comp")
    os.makedirs(comp_path, exist_ok=True)
    print(f"Created main comp directory: {comp_path}")
    folder_structure["comp"] = {}

    # Loop through the comp folders creating the folders in comp_root_folders.
    for required_folder in comp_root_folders:
        folder_path = os.path.join(comp_path, required_folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Verified or created: {folder_path}")

        # Specific sub-folder creation for '02_footage'
        if required_folder == "02_footage":
            folder_structure["comp"][required_folder] = {}
            for sub_folder in footage_comp_folder:
                sub_path = os.path.join(folder_path, sub_folder)
                os.makedirs(sub_path, exist_ok=True)
                print(f"  Created footage subfolder: {sub_path}")
                folder_structure["comp"][required_folder][sub_folder] = sub_path

        elif required_folder == "04_renders":
            folder_structure["comp"][required_folder] = {}
            for sub_folder in render_comp_folder:
                sub_path = os.path.join(folder_path, sub_folder)
                os.makedirs(sub_path, exist_ok=True)
                print(f"  Created footage subfolder: {sub_path}")
                folder_structure["comp"][required_folder][sub_folder] = sub_path

        else:
            # Adds it to a dictionary for non-footage folders
            folder_structure["comp"][required_folder] = folder_path

    return folder_structure


def read_files(show_path):
    """
    Description:
    It reads the files from the show path and ingests it into nuke.

    Input:
    show_path(dict): A dictionary with the folder structure of the show.

    Output:
    read_node(dict): A node in nuke with the read information.
    first_frame(int): The first frame of the plate.
    last_frame(int): The last frame of the plate.
    """
    # Set the path to my read folder.
    footage_path_folder = show_path["comp"]["02_footage"]["01_plate"]

    # Get the sequence information directly from the folder
    sequence = nuke.getFileNameList(footage_path_folder)
    sequence_info = sequence[0]  # e.g., 'test.####.exr 1-50'

    # Parse the sequence info
    parts = sequence_info.split()
    footage_name = parts[0]  # 'test.####.exr'
    range_part = parts[1]  # '1-50'

    # Get the frame range
    first_frame, last_frame = map(int, range_part.split("-"))

    # Build the full path
    file_path = os.path.join(footage_path_folder, footage_name)

    # Normalize path to Nuke standards
    norm_path = os.path.normpath(file_path)
    nuke_read_path = norm_path.replace(os.path.sep, "/")

    # Setting the read file.
    read_node = nuke.createNode("Read")
    read_node["file"].setValue(nuke_read_path)
    read_node["raw"].setValue(True)  # Should be boolean, not string

    # Manually set the frame range on the Read node
    read_node["first"].setValue(first_frame)
    read_node["last"].setValue(last_frame)

    # Force reload
    read_node["reload"].execute()

    return read_node, first_frame, last_frame


def set_up_viewer_color(show_specifications):
    """
    Description:
    Sets up the viewer color space.

    Input:
    show_specifications(dict): Its a dictionary with a key of ['viewer'], with a color string.

    Output:
    viewer (dict): nuke viewer node with the adjusted viewer settings.
    """
    # Set up the viewer Color.
    viewer_color = show_specifications["viewer"]

    # Get the active viewer instance
    viewer = nuke.activeViewer()

    # Get the viewer node and set the viewerProcess knob
    viewer.node()["viewerProcess"].setValue(viewer_color)

    return viewer


def main(show_path, specs):
    """
    Description:
    Creates a Nuke Script with the specifications passed through.

    Input:
    show_path (str): Is the path to the shot folder.
    specs (dic): All the specifications of the show.
    """
    # show_path = 'C:/Users/Luis Alejandro/Documents/test'
    # Run the Main function
    setup_new_script(show_path, specs)

    return

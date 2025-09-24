import nuke
import os
import create_folder_directory_comp_lanh
import read_nuke_files_lanh as rf
import nuke_viewer_setup_lanh as vw

    
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
    folder_structure = create_folder_directory_comp_lanh.main(show_path)

    # Get the paths needed
    exr_path = folder_structure['comp']['04_renders']['02_exr']
    mov_path = folder_structure['comp']['04_renders']['01_mov']
    nk_file_path = show_specifications['nuke_file']

    # Get the directory from the file path
    output_dir = os.path.dirname(nk_file_path)

    # Create the directory if it doesn't exist
    # The 'exist_ok=True' flag prevents an error if the directory already exists
    os.makedirs(output_dir, exist_ok=True)

 

    # Clear the current script to start fresh
    nuke.scriptClear()
    
    # Read plate
    footage,first_frame,last_frame = rf.read_files(folder_structure)

    # Get the root node
    root = nuke.root()

    # Set up the file values as objects.
    aspect_ratio = show_specifications['aspect_ratio'] 
    #color_space = show_specifications['color_space']
    #frame_range = show_specifications['frame_range']
    fps = show_specifications['fps']

    # Set project format
    root['format'].setValue(aspect_ratio)

    # Set frame range
    root["first_frame"].setValue(int(first_frame))
    root["last_frame"].setValue(int(last_frame))

    #Set FPS
    root['fps'].setValue(float(fps))

    viewer = nuke.createNode("Viewer")

    # Set up the viewe settings
    vw.set_up_viewer_color(show_specifications)

    #footage = nuke.createNode('Constant')
    footage.hideControlPanel()

    # Create an OCIO input color space.
    ocio_input = nuke.createNode('OCIOColorSpace')
    ocio_input['in_colorspace'].setValue(show_specifications['screen_color'])
    ocio_input['out_colorspace'].setValue(show_specifications['workspace_color'])
    ocio_input.setXpos(footage.xpos())
    ocio_input.setYpos(footage.ypos() + 100)
    ocio_input.setInput(0,footage)
    ocio_input.hideControlPanel()

    # Set the Backdrop for the input.
    input_backdrop = nuke.createNode('BackdropNode')
    input_backdrop['label'].setValue('Input')
    input_backdrop['note_font_size'].setValue(36)
    input_backdrop.setXpos(footage.xpos()- 25)
    input_backdrop.setYpos(footage.ypos() - 75)
    input_backdrop['bdwidth'].setValue(200)
    input_backdrop['bdheight'].setValue(200)
    input_backdrop.hideControlPanel()

    # Change the colorspace back to screen colorspace
    ocio_output = nuke.createNode('OCIOColorSpace')
    ocio_output['in_colorspace'].setValue(show_specifications['workspace_color'])
    ocio_output['out_colorspace'].setValue(show_specifications['screen_color'])
    ocio_output.setXpos(ocio_input.xpos())
    ocio_output.setYpos(ocio_input.ypos() + 500)
    ocio_output.setInput(0,ocio_input)
    ocio_output.hideControlPanel()

    # Remove the Alpha from the final renders.
    remove_alpha = nuke.createNode('Remove')
    remove_alpha['channels'].setValue('Alpha')
    remove_alpha.setXpos(ocio_output.xpos())
    remove_alpha.setYpos(ocio_output.ypos()+50)
    remove_alpha.setInput(0,ocio_output)
    remove_alpha.hideControlPanel()

    # Create dots to adjust the reformat of the HD.
    dot1 = nuke.createNode('Dot')
    dot1.setXpos(remove_alpha.xpos() + 34)
    dot1.setYpos(remove_alpha.ypos() +100)
    dot1.setInput(0,remove_alpha)
    dot1.hideControlPanel()

    dot2 = nuke.createNode('Dot')
    dot2.setXpos(dot1.xpos() + 350)
    dot2.setYpos(dot1.ypos())
    dot2.setInput(0,dot1)
    dot2.hideControlPanel()

    # Reformat both to HD playblast
    reformat_hd = nuke.createNode('Reformat')
    reformat_hd['format'].setValue('HD_1080')
    reformat_hd.setYpos(dot2.ypos() + 100)
    reformat_hd.setXpos(dot2.xpos() - 34)
    reformat_hd.setInput(0,dot2)
    reformat_hd.hideControlPanel()

    # Set up the correct paths for the files
    mov_path_file = os.path.join(mov_path, show_specifications['mov_name'])
    mov_norm_path = os.path.normpath(mov_path_file)
    mov_correct_path = mov_norm_path.replace(os.path.sep,'/')
    exr_path_file = os.path.join(exr_path, show_specifications['exr_name'])
    exr_norm_path = os.path.normpath(exr_path_file)
    exr_correct_path = exr_norm_path.replace(os.path.sep,'/')

    # Create a Write node for mov
    write_mov_node = nuke.createNode("Write")
    write_mov_node["file"].setValue(mov_correct_path)
    write_mov_node["file_type"].setValue("mov")
    write_mov_node.setYpos(reformat_hd.ypos() + 50)
    write_mov_node.setXpos(reformat_hd.xpos())
    write_mov_node.setInput(0,reformat_hd)
    write_mov_node.hideControlPanel()

    # Create MOV background
    backdrop_mov = nuke.createNode('BackdropNode')
    backdrop_mov['label'].setValue('MOV')
    backdrop_mov['note_font_size'].setValue(36)
    backdrop_mov.setXpos(reformat_hd.xpos()-100)
    backdrop_mov.setYpos(reformat_hd.ypos() - 100)
    backdrop_mov['bdwidth'].setValue(200)
    backdrop_mov['bdheight'].setValue(200)
    backdrop_mov.hideControlPanel()

    # Reformat to final resolution.
    reformat = nuke.createNode('Reformat')
    reformat.setXpos(dot1.xpos() - 34)
    reformat.setYpos(dot1.ypos() + 100)
    reformat.setInput(0,dot1)
    reformat.hideControlPanel()

    # Create a Write node for exr
    write_exr_node = nuke.createNode("Write")
    write_exr_node["file"].setValue(exr_correct_path)
    write_exr_node["file_type"].setValue("exr")
    write_exr_node.setInput(0,reformat)
    write_exr_node.setYpos(reformat.ypos() + 50)
    write_exr_node.setXpos(reformat.xpos())
    write_exr_node.hideControlPanel()

    # Create exr background
    backdrop_exr = nuke.createNode('BackdropNode')
    backdrop_exr['label'].setValue('EXR')
    backdrop_exr['note_font_size'].setValue(36)
    backdrop_exr.setXpos(reformat.xpos() - 100)
    backdrop_exr.setYpos(reformat.ypos() - 100)
    backdrop_exr['bdwidth'].setValue(200)
    backdrop_exr['bdheight'].setValue(200)
    backdrop_exr.hideControlPanel()

    # Now, you can safely save the Nuke file
    nuke.scriptSaveAs(nk_file_path)

    return 
    

def main():
    show_path = 'C:/Users/Luis Alejandro/Documents/test'
    setup_new_script(show_path, specs)

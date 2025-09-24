import nuke

def set_up_viewer_color(show_specifications):
    '''
    Description:
    Sets up the viewer color space.

    Input:
    show_specifications(dict): Its a dictionary with a key of ['viewer'], with a color string.

    Output:
    viewer (dict): nuke viewer node with the adjusted viewer settings.
    '''
    # Set up the viewer Color.
    viewer_color = show_specifications['viewer']
    
    # Get the active viewer instance
    viewer = nuke.activeViewer()

    # Get the viewer node and set the viewerProcess knob
    viewer.node()['viewerProcess'].setValue(viewer_color)

    return viewer
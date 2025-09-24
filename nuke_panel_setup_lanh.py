import nuke
import os
import json
import PySide2 as ps
import importlib
import PyOpenColorIO as ocio
import json_file_setup_lanh as jsfile
import shot_setup_nuke_lanh as nkfile
import get_root_folders as getroot

# Refreshes any files before starting
importlib.reload(jsfile)
importlib.reload(nkfile)

class ShowPresetsUI(ps.QtWidgets.QDialog):
    def __init__(self, parent=None):
        '''
        Description:
        Initialize the class, or ui window in this case.

        Input:
        parent(class): Optional parent class to inherit.

        Output:
        None
        '''
        super(ShowPresetsUI, self).__init__(parent)
        
        # Default specifications template
        self.default_specs = {
            'aspect_ratio': 'HD_1080',
            'color_space': 'sRGB',
            'frame_range': '1-100',
            'viewer': 'None',
            'screen_color': 'texture_paint',
            'workspace_color': 'scene_linear',
            'exr_name': 'final.####.exr',
            'mov_name': 'final.mov',
            'fps': '24'
        }
        
        # Current working specs
        self.current_specs = self.default_specs.copy()
        self.current_show_path = ""
        
        self.setWindowTitle("Shot Presets Manager")
        self.setMinimumSize(600, 500)
        self.resize(600,300)
        self.setWindowFlags(ps.QtCore.Qt.Window)
        
        self.init_ui()
        #self.load_show_presets()
        
    def init_ui(self):
        '''
        Description:
        A class function that sets up the title and the UI.

        Input:
        none
        
        Output:
        None
        '''
        layout = ps.QtWidgets.QVBoxLayout(self)
        
        # Title
        title = ps.QtWidgets.QLabel("Shot Setup Manager")
        title.setAlignment(ps.QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 15px;")
        layout.addWidget(title)
        
        # Show selection and path section
        self.create_show_section(layout)
        
        # Specifications editor
        self.create_specs_editor(layout)
        
        # Action buttons
        self.create_action_buttons(layout)
        
    def create_show_section(self, parent_layout):
        group = ps.QtWidgets.QGroupBox("Shot Setup:")
        layout = ps.QtWidgets.QVBoxLayout(group)
        
        # New show name input
        new_shot_layout = ps.QtWidgets.QHBoxLayout()
        new_shot_layout.addWidget(ps.QtWidgets.QLabel("Compositors Name:"))
        self.show_name_input = ps.QtWidgets.QLineEdit()
        self.show_name_input.setPlaceholderText("Enter the compositors name...")
        self.show_name_input.setToolTip('Add the compostior name as formatted to the show' \
                                        ' to add to the file name')
        new_shot_layout.addWidget(self.show_name_input)
        layout.addLayout(new_shot_layout)
        
        # Show path selection
        path_layout = ps.QtWidgets.QHBoxLayout()
        path_layout.addWidget(ps.QtWidgets.QLabel("Shot Path:"))
        
        self.show_path_label = ps.QtWidgets.QLabel("No path selected")
        self.show_path_label.setStyleSheet("border: 1px solid gray; padding: 5px; background: #f0f0f0;")
        self.show_path_label.setToolTip('In the browse button, search for your shot folder ' \
                                        'click on the root folder.')
        path_layout.addWidget(self.show_path_label, 1)
        
        browse_btn = ps.QtWidgets.QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_show_path)
        path_layout.addWidget(browse_btn)
        
        layout.addLayout(path_layout)

        # Add an add preset button
        preset_layout = ps.QtWidgets.QHBoxLayout()
        preset_layout.addWidget(ps.QtWidgets.QLabel("Show Preset:"))
        
        self.preset_path_label = ps.QtWidgets.QLabel("No path selected")
        self.preset_path_label.setStyleSheet("border: 1px solid gray; padding: 5px; background: #f0f0f0;")
        self.preset_path_label.setToolTip('In the browse button, search for your shot folder ' \
                                        'click on the root folder.')
        preset_layout.addWidget(self.preset_path_label, 1)
        
        search_btn = ps.QtWidgets.QPushButton("Browse")
        search_btn.clicked.connect(self.browse_preset_path)
        search_btn.clicked.connect(self.load_preset_settings)
        preset_layout.addWidget(search_btn)
        
        layout.addLayout(preset_layout)
        
        parent_layout.addWidget(group)

    # Come back here to manually set up the list of options.   
    def create_specs_editor(self, parent_layout):
        group = ps.QtWidgets.QGroupBox("Show Specifications")
        form_layout = ps.QtWidgets.QFormLayout(group)
        
        # Create input widgets for each spec
        self.spec_widgets = {}

        # Grab the available list.
        color_spaces, aspect_ratios, viewer_color = self.get_options()

        # Get color spaces
        #color_spaces = nuke.getOcioColorSpaces()

        
        # Aspect Ratio
        self.spec_widgets['aspect_ratio'] = ps.QtWidgets.QComboBox()
        self.spec_widgets['aspect_ratio'].addItems(
                                                    aspect_ratios
                                                    )
        form_layout.addRow("Aspect Ratio:", self.spec_widgets['aspect_ratio'])
        
        # Color Space
        self.spec_widgets['viewer'] = ps.QtWidgets.QComboBox()
        self.spec_widgets['viewer'].addItems(
                                                viewer_color
                                            )
        form_layout.addRow("Color Space:", self.spec_widgets['viewer'])

        # Screen Color
        self.spec_widgets['screen_color'] = ps.QtWidgets.QComboBox()
        self.spec_widgets['screen_color'].addItems(
                                                    color_spaces
                                                    )
        form_layout.addRow("Screen Color:", self.spec_widgets['screen_color'])
        
        # Workspace Color
        self.spec_widgets['workspace_color'] = ps.QtWidgets.QComboBox()
        self.spec_widgets['workspace_color'].addItems(
                                                        color_spaces
                                                        )
        form_layout.addRow("Workspace Color:", self.spec_widgets['workspace_color'])
        
        # EXR Name
        self.spec_widgets['exr_name'] = ps.QtWidgets.QLineEdit()
        form_layout.addRow("EXR Name:", self.spec_widgets['exr_name'])
        
        # MOV Name
        self.spec_widgets['mov_name'] = ps.QtWidgets.QLineEdit()
        form_layout.addRow("MOV Name:", self.spec_widgets['mov_name'])
        
        # FPS
        self.spec_widgets['fps'] = ps.QtWidgets.QComboBox()
        self.spec_widgets['fps'].addItems(['23.976', '24', '25', '29.97', '30', '50', '59.94', '60'])
        self.spec_widgets['fps'].setEditable(True)
        form_layout.addRow("FPS:", self.spec_widgets['fps'])
        
        
        parent_layout.addWidget(group)

    # Come back to this to set up the action buttons. COME HERE TO CONNECT.
    def create_action_buttons(self, parent_layout):
        '''
        Description:
        Creates the Save Show Preset, Start New Script, and close bottons.

        Input:
        None

        Output:
        None
        '''
        button_layout = ps.QtWidgets.QHBoxLayout()
        
        # Save Show Preset
        save_btn = ps.QtWidgets.QPushButton("Save Show Preset")
        save_btn.clicked.connect(self.save_show_preset)
        save_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 8px;")
        button_layout.addWidget(save_btn)
        
        # Setup New Script (calls your existing function)
        setup_btn = ps.QtWidgets.QPushButton("Setup New Script")
        setup_btn.clicked.connect(self.transfer_data)
        setup_btn.clicked.connect(self.close)
        setup_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        button_layout.addWidget(setup_btn)
        
        # Close
        close_btn = ps.QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("background-color: #FA003F; color: white; font-weight: bold; padding: 8px;")
        button_layout.addWidget(close_btn)
        
        parent_layout.addLayout(button_layout)
        
                
    def browse_show_path(self):
        '''
        Description:
        Browses the paths and sets the text of the selected file.

        Input:
        None

        Output:
        show_path(str): A path to your comp folder.
        '''
        current_path = self.show_path_label.text()
        if current_path == 'No path selected':
            current_path = os.path.expanduser("~")
        folder = ps.QtWidgets.QFileDialog.getExistingDirectory(
                                                                self, 
                                                                "Select Folder",
                                                                current_path
                                                                )
        if folder:
            self.current_show_path = folder
            show_path = self.show_path_label.setText(folder)
            show_path_txt = str(show_path)
        #print(folder)
        return folder

    def browse_preset_path(self):
        '''
        Description:
        Sets the JSON preset file for the show.

        Input:
        None

        Output:
        json_preset(str): .JSON file path.
        '''

        current_path = self.preset_path_label.text()
        if current_path == "No path selected":
            current_path = os.path.expanduser("~")
            
        file_path, _ = ps.QtWidgets.QFileDialog.getOpenFileName(
            self, 
            "Select Preset JSON File",
            current_path,
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            json_preset = self.preset_path_label.setText(file_path)
            # You might also want to call a function here to load the data from this file
            # e.g., self.load_preset_from_file(file_path)
        return json_preset
            
    def save_show_preset(self):
        '''
        Description:
        It saves the selected nodes in the show settings into a json file
        
        Input:
        None

        Output:
        filename(str): Is the path of the saved json file.
        '''
        json_preset = dict()
        shot_path = self.browse_show_path()
        name = 'preset'
        #print(shot_path)
        #print (name)
        filename = jsfile.get_json_path(name,shot_path)
        #print(filename)
        for key,widget in self.spec_widgets.items():
            if isinstance(widget, ps.QtWidgets.QLineEdit):
                json_preset[key] = widget.text()
            elif isinstance(widget, ps.QtWidgets.QComboBox):
                json_preset[key] = widget.currentText()
        #print(json_preset)
        
        with open(filename,'w') as f:
            json.dump(json_preset,f,indent = 4)
        #print('Succesfully exported to {}'.format(filename))

        return filename

    def load_preset_settings (self):
        '''
        Description:
        It loads the presets of a json file into the respective keys.

        Input:
        None

        Output:
        self.current_specs (dic): A new updated dictionary with all the current specs.
        '''
        with open(self.preset_path_label.text(), "r") as f:
            data = json.load(f)

        self.current_specs = data.copy()

        # print (self.current_specs)

        for key, widget in self.spec_widgets.items():
            value = self.current_specs.get(key, '')
            # print(f'This is the value {value}')
            if isinstance(widget, ps.QtWidgets.QComboBox):
                index = widget.findText(value)
                if index >= 0:
                    widget.setCurrentIndex(index)
                    # print (f'index {index}')
                else:
                    widget.setEditText(value)
                    # print (f'value: {value}')
            elif isinstance(widget, ps.QtWidgets.QLineEdit):
                widget.setText(value)

        # print (self.spec_widgets.items())

        ps.QtWidgets.QMessageBox.information(self, "Preset Loaded", "Preset loaded successfully!")

        return self.current_specs

    def get_options (self):
        '''
        Description:
        Grabs all the available items in the list and adds it to the menu.

        Input:
        None

        Ouput:
        options_vl(list): List of all the available colorspaces in the OCIOColorspace node
        aspect_ratios(list): List of all the available aspect ratios/
        viewer_color(list): List of all the available viewer color. 
        '''
        # Grab all the color references available.
        options_vl = []
        # Get the active OCIO config Nuke is using
        config = ocio.GetCurrentConfig()

        # Get *only* the defined color spaces (no displays, no views)
        color_spaces = [cs.getName() for cs in config.getColorSpaces()]

        # Grab all the aspect ratios available
        aspect_ratios = []
        for format_obj in nuke.formats():
            aspect_ratios.append(format_obj.name())

        # Grab all the available viewer options
        viewer_color = []
        viewer = nuke.activeViewer()
        colors = viewer.node()['viewerProcess'].values()
        for i in colors:
            viewer_color.append(i)
        
        return color_spaces, aspect_ratios, viewer_color

        
    
    def transfer_data(self):
        '''
        Description:
        Adds the results to a list that exports it to a set up script.

        Input:
        None

        Output:
        specs (dict): All the values gathered by the UI.
        '''

        # Set the dictionary blank.
        specs = {}

        # Gets the shot folder path.
        shot_path = self.show_path_label.text()
        
        # Get the specs information into the file.
        for key,widget in self.spec_widgets.items():
            if isinstance(widget, ps.QtWidgets.QLineEdit):
                specs[key] = widget.text()
            elif isinstance(widget, ps.QtWidgets.QComboBox):
                specs[key] = widget.currentText()

        # Grab the folders name for the naming convention.        
        show_shot_name = getroot.grab_root_name(shot_path)
        show_name,shot_number = show_shot_name
        compers_name = self.show_name_input.text()

        # Set the naming files for the shows and outputs.
        file_name = f'{show_name}_{shot_number}_comp_{compers_name}_v01'
        file_name_path = f'{shot_path}/comp/01_scripts/'
        base_file_path = os.path.join(file_name_path,file_name)
        nk_file_path = f'{base_file_path}.nk'
        exr_name = f"{file_name}_{self.spec_widgets['exr_name'].text()}"
        mov_name = f"{file_name}_{self.spec_widgets['mov_name'].text()}"

        # Rename the exr and mov inputs.
        specs['exr_name'] = exr_name
        specs['mov_name'] = mov_name
        specs['nuke_file'] = nk_file_path


        nkfile.setup_new_script(shot_path,specs)

        return

def show_presets_manager():#
    '''
    Description:
    It checks if the window is created, deletes the window, and draws a new one.

    Input:
    None

    Output:
    show_presets_manager.ui(class): Is an object that stores the UI class in it.
    '''
    
   # Check if the function has the attribute (window), named dialog. if it does, it closes it.
    if hasattr(show_presets_manager, 'ui'):
        try:
            show_presets_manager.ui.close()
        except:
            pass
    
    # Stores the class into the show_presets_manager.ui attribute.
    show_presets_manager.ui = ShowPresetsUI()

    # Shows the window.
    show_presets_manager.ui.show()

    #print(type(show_presets_manager.ui))

    return show_presets_manager.ui

def main():
    '''
    Description:
    It runs the UI program.

    Input:
    None

    Output:
    None
    '''
    # Runs the program.
    show_presets_manager()
    

# Run the UI
if __name__ == "__main__":
    show_presets_manager()


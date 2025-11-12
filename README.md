# nuke_show_setup_manager
A Nuke Python script that creates a UI that sets up and automates the load-in of new Nuke scripts for compositors.


# How it works:
Its a tool that prevents setting kickbacks for compositors in a show. A UI that helps lead compositors set up a preset for a show/shot comp requirements, and lets the compositors load in the preset, type their name, and start working right away.

# The benefits:
Less lost time teaching compositors what to add in their colorspaces, and fewer kickbacks in the publishing of finals due to colorspace, frame range, and aspect ratio mistakes.

# HOW TO INSTALL:
Simply download the repository into your .nuke file and add these lines of code into your init.py file.

    import nuke
    import nuke_panel_setup_lanh 
    
   # Create a menu item to launch your plugin
    toolbar = nuke.menu('Nuke')
    my_menu = toolbar.addMenu('AN Tools', index = 1000)

    # Add a command to the menu that calls the function to show your UI
    my_menu.addCommand('Shot setup', 'nuke_panel_setup_lanh.main()')

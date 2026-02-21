# nuke_show_setup_manager
A Nuke Python script that creates a UI that sets up and automates the load-in of new Nuke scripts for compositors.

<img width="600" height="530" alt="image" src="https://github.com/user-attachments/assets/103ab81a-ba37-47f8-8d7a-9a0326746b7b" />


# The Problem:
At my studio, we had a Compositor supervisor who created the documentation and the base script for Compositors to set their script to start working. The problem happened when compositors started working; they ignored color spaces for their comps, naming conventions, and project settings when they submitted for finals. The problem got even worse when she left, since there was no one to continue the documentation. Our studio at school is mostly run by artists who couldn't or didn't want to work in production and documentation. So I produced a tool that would facilitate this process for both Compositors lead in the future and Compositors. 

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

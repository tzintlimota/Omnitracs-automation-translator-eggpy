# Omnitracs-automation-translator-eggpy
This repository contains the code to translate Eggplant HOS Mobile functions to Python with the library pyIMR 
https://github.com/Omnitracs/automation-image-recognition-tool.

Structure:

`Images\`:

        a) Buttons\: The same folders and captures from Eggplant project
        b) ExpectedScreens\: Full IVG screen captures to use with expected_image method
        
`AlertCheck.py`: Script that can be run in parallel to discard or handle HOS prompts (Certify, Load Info and Alert Warnings)

`connection_credentials.py`: This is a configuration file but it has a bug for linux, so for the time being is not being used

`dependencies_(mac_linux/win10).bat:` This .bar file triggers requirement.txt in order to install dependencies
            
             To Install dependencies, open a terminal on the cloned project and run the command: dependencies_win10.bat
              
`eggpy.py`: This script contains the code that translates Eggplatn script to Python.
            Line 14 contains the name of the file to be translated.
            This file needs to be updated once the code of a new method has been added to IVG_ELD_Core, IVG_Common or WinMachine_Common
            
`ImageProcessor.py:` Methods to handle image recognition on the IVG through VNC connection
 
`IVG_Common.py:` Methods related to functionality of the IVG outside of the HOS app

`IVG_ELD_Core.py:` Methods related to functionality og Hours of Service app

`IVG_var.txt:` The contains of this file are used as a flag to enable AlertCheck for test cases that need to validate any of the prompts

`requirements.txt:` This file contains all the required packages that need to be installed. It is used by dependencies_mac_linux.bat or 
                    dependencies_win10.bat.
                    
 
 
            
     




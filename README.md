# Comment Tool 

This tool lets 
the user write comments. \
A possible usage could be as an extension to the blue pencil tool in maya to use during the animation pipeline to write feedback. \
The tool can be run in Maya or as a standalone program, where no maya is needed

![img_12.png](images%2Fimg_12.png)
## Prerequisites

This tool runs in **Linux** and **Maya**

To run the tool in Maya, **Maya 2023** needs to be installed. \
To run the standalone program **vlc media player** needs to be installed.

Other packages that need to be installed are **python 3.9** and **PySide**

## Installation

download the git repository as a .zip file and unpack it wherever wanted

### Linux

open a new terminal and navigate to the **CommentToolPlugin/** folder and run **python install.py**

![img.png](images%2Fimg.png)

This creates the needed files to run the tool in Maya. \
For the standalone program either run the **executable file** in **executable/** or open it with the terminal.  \
Therefore navigate to **CommentToolPlugin/python/src** and run either 

![img_2.png](images%2Fimg_2.png)

or 

![img_3.png](images%2Fimg_3.png)

### Windows

with the Explorer navigate to the **CommentToolPlugin/** folder. Open a new cmd window by typing cmd into the path. This opens a new cmd window which is set to the right path. \
Run **python install.py**:

![img_7.png](images%2Fimg_7.png)

This creates the needed files to run the tool in Maya. \
For the standalone program either run the **executable file** in **executable/** or open it with another command.  \
Therefore navigate with the Explorer to **CommentToolPlugin\python\src** and open a new cmd window by typing cmd into the path. \
Run **python CommentToolStandalone.py**

![img_8.png](images%2Fimg_8.png)

### Install manually

If you don't want to run the **install.py** script there is a way to install it manually. Navigate to **CommentToolPlugin/installScripts** \
Open **MayaCommentTool.mod** with either a text editor or script editor and change the path in line 1 so it directs to the **CommentToolPlugin/** folder. \
Copy that file in :
* /maya/modules (Linux)
* \Documents\maya\modules (Windows)

Copy the **shelf_CommentTool.mel** into:
* /maya/2023/prefs/shelves/ (Linux)
* \Documents\maya\2023\prefs\shelves (Windows)

## Running the Tool in Maya

After successfully installing the tool open Maya (or close and reopen it if it is already open). You should now see a new shelf called **Comment Tool**. \
By pressing the shelf button the tools open. 

![img_9.png](images%2Fimg_9.png)

If the open scene already has comments you'll be asked if you want to open them.
You can now:
* write, edit, delete and reload comments
* save comments and a playblast of the scene
  * the comments and the video are saved in a Comments folder which is in the same directory as the maya file
* jump between the comments or jump to a specific comment by double-clicking on it. 

## Running the standalone program

After opening the standalone program, a window should pop up asking if you want to load a video. If comments connected to the video are found, they can be loaded aswell. \
Regardless the Comment tool opens. 

![img_11.png](images%2Fimg_11.png)

You can now:
* write, edit, delete and save comments
  * the comments are saved in the same directory as the loaded video
* open a new video

Example files can be found in the **example/** folder



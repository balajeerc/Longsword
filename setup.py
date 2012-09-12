# A simple setup script to create an executable using matplotlib.
#
# test_matplotlib.py is a very simple matplotlib application that demonstrates
# its use.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
import os

import cx_Freeze

base = None
if sys.platform == "win32":
    base = "Win32GUI"

#We prepare a list of included files that are to be part of the
#executable's zip or msi
ignoredFolders = ['src','build','.git']
ignoredFiles = ['setup.py','.gitignore','.project','.pydevproject','longsword.py','README.txt','NOTES','.DS_Store']
includedFiles = []
currentDirectory = os.getcwd()
ignoredFolderPatterns = []
for folder in ignoredFolders:
    pattern = os.path.sep+folder
    ignoredFolderPatterns.append(pattern)
    print("Ignoring pattern:"+pattern)
for rootFolder, subFolders, files in os.walk(currentDirectory):
        ignoreFolder = False
        for pattern in ignoredFolderPatterns:
            if rootFolder.find(pattern) != -1:                
                #print("Ignoring folder: " + rootFolder)
                ignoreFolder = True
                break
        if not ignoreFolder:                    
            for file in files:
                #Check if the current file is in the list of ignored files
                if file in ignoredFiles:
                    #print("Ignoring file:" + os.path.join(rootFolder,file))
                    continue            
                filepath = os.path.join(rootFolder,file)
                #cx_Freeze only accepts relative filepaths and of the
                #form with forward slashes only
                relpath = os.path.relpath(filepath,currentDirectory)
                incPath = relpath.replace('\\','/')
                print(incPath)
                includedFiles.append(incPath)
            
buildOptions = dict(
		packages = ["sys","os","json","random","math","pyglet","cocos"],
        excludes = ["Tkinter"],
        include_files = includedFiles
)

iconFile = "assets/icons/professor"
if sys.platform == "win32":
    iconFile += ".ico"
elif sys.platform == "darwin":
    iconFile += ".icns"
else:
    iconFile += ".png"    
executables = [
        cx_Freeze.Executable("longsword.py", base = base, icon=iconFile)
]

cx_Freeze.setup(
        name = "Longsword",
        version = "0.1",
        description = "Longsword the Game",
        executables = executables,
        options = dict(build_exe = buildOptions)
)



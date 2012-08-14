# A simple setup script to create an executable using matplotlib.
#
# test_matplotlib.py is a very simple matplotlib application that demonstrates
# its use.
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import cx_Freeze
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

buildOptions = dict(
        excludes = ["Tkinter"])

executables = [
        cx_Freeze.Executable("main.py", base = base)
]

cx_Freeze.setup(
        name = "Longsword",
        version = "0.1",
        description = "Longsword the Game",
        executables = executables,
        options = dict(build_exe = buildOptions)
)


=============
Longsword
=============

A simple side scrolling game where you kill aliens with a long blade!

Do checkout the:
 - Source repository: https://github.com/balajeerc/Longsword

If you only want to play the game on windows, download the build from:
https://docs.google.com/open?id=0B_3UZN1ZieQgRjlEUUZkNDFycmM

Building and running
--------------------

Longsword is a game written in Python using the Cocos2d API. The following build instructions are common to all platforms. In short you will need a *nix like system to compile and run the game. On Microsoft Windows, you will need to install something like MSys or Cygwin to get things working. I managed to it running on Windows by installing Git Bash and then following the steps described below.

1. Install Python 2.7.x. Most modern GNU/Linux distributions come with python 2.7 installed. To find what installation you have, Open your terminal and type:

  $ python --version

 For download and installation instructions, go to http://www.python.org/

(On Microsoft Windows, you may need to add the directory containing the Python executable to your PATH environment variable, so that you can easily invoke it from the shell environment [Git Bash, Cygwin, MSyS] that you have installed.

2. Install setup tools for Python 2.7 instructions at: http://pypi.python.org/pypi/setuptools

3. Install pyglet (NOTE: You necessarily need to install pyglet from SVN and BEFORE you install cocos2d. This is because the Cocos2d installer, if it does not find an existing Pyglet installation, will install the stable release of Pyglet, instead of SVN Trunk, which is what we need for Longsword).

You will need mercurial DVCS to grab the latest pyglet source.

  $ hg clone https://pyglet.googlecode.com/hg/ pyglet
  $ cd pyglet
  $ sudo python setup.py install

4. Install cocos2d (NOTE: you need the SVN trunk) using the following instructions:

  $ svn checkout http://los-cocos.googlecode.com/svn/trunk/ cocos2d 
  $ cd cocos2d
  $ sudo python setup.py install

You should now have cocos2d installed into the site-packages directory of your Python installation. You should test that your cocos2d installation is working by:

  $ cd test
  $ python test_tmx.py

You should have a window with a minimalist car running around an abstract looking map.

5. Finally, once you have a working cocos2d installation, go inside the Longsword source repository and:

  $ python longsword.py

You should now be able to play Longsword.

6. Generating final application: Longsword source comes with cxFreeze scripts to build final, frozen application from the source python scripts. 
To generate the executables for you platform, install cxFreeze from http://cx-freeze.sourceforge.net
Inside the Longsword root directory (i.e. the directory containing longsword.py), do:

  $python setup.py build

You will now have ready-to-run binaries for your platform installed in the build/ directory. 


Should you have any problems with this installation process, please drop me an email and I'll get back to you ASAP: mail at balajeerc dot info

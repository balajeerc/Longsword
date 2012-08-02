=============
Longsword
=============

A simple side scrolling game where you kill aliens with a long blade!

Do checkout the:
 - Source repository: https://github.com/balajeerc/Longsword

Building and running
--------------------

Longsword is a game written in Python using the Cocos2d API. 

1. Install Python 2.7.x. Most modern GNU/Linux distributions come with python 2.7 installed. To find what installation you have, Open your terminal and type:

  $ python --version

 For download and installation instructions, go to http://www.python.org/

2. Install setup tools for your distribution using instructions at: http://pypi.python.org/pypi/setuptools

3. Install cocos2d (NOTE: you need the SVN trunk) using the following instructions:

  $ svn checkout http://los-cocos.googlecode.com/svn/trunk/ cocos2d 
  $ cd cocos2d
  $ sudo python setup.py install

You should now have cocos2d installed into the site-packages directory of your Python installation. You should test that your cocos2d installation is working by:

  $ cd test
  $ python test_tmx.py

You should have a window with a minimalist car running around an abstract looking map.

4. Finally, once you have a working python installation, go inside the Longsword source repository and:

  $ python main.py

This should have Longsword running on your system.	

Should you have any problems with this installation process, please drop me an email and I'll get back to you ASAP: mail at balajeerc dot info

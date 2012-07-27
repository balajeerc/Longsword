#    Copyright 2012 Balajee.R.C
#    
#    This file is part of Longsword
#    
#    Longsword is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    Longsword is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with Longsword.  If not, see <http://www.gnu.org/licenses/>.

import pyglet
import cocos

import entity

class Player(entity.Entity):
    """Main player for Longsword"""
    
    def __init__(self):
        super(Player,self).__init__()
        self.load("assets/player")
                        
    def registerEventHandlers(self,layer):
        """Sets up input handlers for the player
        
        Given a cocos layer, this method assigns the input event handlers
        defined on that layer to the player class, since in Longsword
        all input handling will be done within player
        
        Keyword arguments:
        layer -- cocos2d layer that listens for events
        """
        layer.on_key_press = self.onKeyDown
        layer.on_key_release = self.onKeyUp        
        layer.on_mouse_motion = self.onMouseMove
        layer.on_mouse_press = self.onMouseDown
        
    
    #Event handlers for player
    def onKeyDown(self, key, modifiers):
        walkFactor = 10
        if key == 119:  #W key
            self.playAnimation("walkUp")
            self.translate(0,walkFactor)
        elif key == 97: #A key
            self.playAnimation("walkLeft")
            self.translate(-walkFactor,0)
        elif key == 115: #S key
            self.playAnimation("walkDown")
            self.translate(0,walkFactor*-1)
        elif key == 100: #D key
            self.playAnimation("walkRight")
            self.translate(walkFactor,0)
            
    def onKeyUp(self, key, modifiers):
        self.stopAnimation()
    
    def onMouseMove(self, x, y, dx, dy):
        pass
    
    def onMouseDown(self, x, y, buttons, modifiers):
        pass

        
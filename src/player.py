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

import gamemanager
import entity
import debug
import beam

class Player(entity.Entity):
    """Main player for Longsword"""
    
    def __init__(self):
        super(Player,self).__init__()
        self.load("assets/player")
        self.keyState = {key: False for key in ["W","A","S","D"]}
        self.keyAxisState = [0.0,0.0]
        self.speed = 100.0 #Speed of player movement, in pixels per second
        self.lastKeyPressed = None
        self.beam = beam.Beam()
        self.beam.showBounds(True)
        gamemanager.GameManager.getInstance().addEntity(self.beam)
        self.rotationRate = 0.5
                       
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
        """Key down handler"""
        if key == 119:  #W key
            self.keyState["W"] = True
            self.lastKeyPressed = "W"
        elif key == 97: #A key
            self.keyState["A"] = True
            self.lastKeyPressed = "A"
        elif key == 115: #S key
            self.keyState["S"] = True
            self.lastKeyPressed = "S"
        elif key == 100: #D key
            self.keyState["D"] = True
            self.lastKeyPressed = "D"
            
    def onKeyUp(self, key, modifiers):
        """Key up handler"""
        if key == 119:  #W key
            self.keyState["W"] = False
        elif key == 97: #A key
            self.keyState["A"] = False
        elif key == 115: #S key
            self.keyState["S"] = False
        elif key == 100: #D key
            self.keyState["D"] = False
    
    def onMouseMove(self, x, y, dx, dy):
        currRotation = self.beam.sprite.rotation
        currRotation += (dy)*self.rotationRate*-1
        if currRotation > 70.0:
            currRotation = 70;
        if currRotation < -70.0:
            currRotation = 70.0 
        self.beam.rotateTo(currRotation)   
#        debug.clearLog()
#        debug.log("rotation: "+str(self.beam.sprite.rotation))
        
    def onMouseDown(self, x, y, buttons, modifiers):
        pass

    def updateKeyAxisState(self):
        """Calculates the net direction in which the player must move
        based on current keystate"""
        self.keyAxisState[0] = 0.0
        self.keyAxisState[1] = 0.0
        if self.keyState["W"]:
            self.keyAxisState[1] = self.keyAxisState[1]+1.0
        if self.keyState["S"]:
            self.keyAxisState[1] = self.keyAxisState[1]-1.0
        if self.keyState["A"]:
            self.keyAxisState[0] = self.keyAxisState[0]-1.0
        if self.keyState["D"]:
            self.keyAxisState[0] = self.keyAxisState[0]+1.0
                                          
    def update(self, timeSinceLastUpdate, *args, **kwargs):
        """Update method for the player character in Longsword
        
        Keyword arguments:
        timeSinceLastUpdate -- time elapsed since the last time this update was called
        args -- list of arguments to this update method
        kwargs --         
        """
        #Call super class update
        super(Player,self).update(timeSinceLastUpdate, *args, **kwargs)        
        self.updateKeyAxisState()       
        #First, based on input key state, we move the player around
        #self.sprite.x = self.sprite.x + self.keyAxisState[0]*self.speed*timeSinceLastUpdate
        #self.sprite.y = self.sprite.y + self.keyAxisState[1]*self.speed*timeSinceLastUpdate         
        self.translate(self.keyAxisState[0]*self.speed*timeSinceLastUpdate, 
                       self.keyAxisState[1]*self.speed*timeSinceLastUpdate)
        
        #Play corresponding animation
        #We have a certain priority ordering here
        #If the player is moving up, even if he is moving to the left
        #at the same time, the moving up animation is played
        if self.keyAxisState[0]==0.0 and self.keyAxisState[1]==0.0:
            self.stopAnimation()
        else:
            if not self.currentAnimation:
                self.playAnimation("walkRight")
        focus_pt_x = self.sprite.x + 270
        focus_pt_y = 320
        
        gamemanager.GameManager.getInstance().getScrollingManager().set_focus(focus_pt_x,focus_pt_y)
        
        #Now handle the mouse moves so that the beam is rotated
        #We start by aligning the beam to the player's hand
        beamRect = self.beam.sprite.get_rect()
        
        offset = [0.0,0.0]
        if self.currentAnimation:
            offset = [-5,1]
        else:
            offset = [-4,2]
        self.beam.moveTo(self.sprite.x+beamRect.width*0.5+offset[0],
                          self.sprite.y-beamRect.height*0.5+offset[1])
                
    def notifyCollision(self,other):
        """Updates the collision lists for colliders"""
        super(Player,self).notifyCollision(other)
        #print(self.entityName + " collided with " + other.entityName + " at " + str(other.cshape.center))    
        #other.sprite.visible = False
        
        
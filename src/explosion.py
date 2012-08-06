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

import entity
import debug
import beam

class Explosion(entity.Entity):    
    def __init__(self,pt):
        super(Explosion,self).__init__(spawnPt=pt)        
        self.load("assets/explosion")
        self.zval = 3
        self.exploded = False
        self.sprite.scale = 0.75
        
    def explode(self, removeAfterExplosion=True):
        self.playAnimation("explode")
        self.exploded = removeAfterExplosion
        
    def update(self, timeSinceLastUpdate, *args, **kwargs):
        """Update method for NPC in Longsword
        
        Keyword arguments:
        timeSinceLastUpdate -- time elapsed since the last time this update was called
        args -- list of arguments to this update method
        kwargs --         
        """
        #Call super class update
        super(Explosion,self).update(timeSinceLastUpdate, *args, **kwargs)
        if self.exploded and not self.isAnimationPlaying():
            self.stopAnimation()
            self.destroy()
            print("Destroying explosion")
            
    def destroy(self):
        """Destroys this entity"""
        super(Explosion,self).destroy()
        #Play the explosion sound here        
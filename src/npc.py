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

class NPC(entity.Entity):
    
    def __init__(self,entityName,characterType,pt):
        super(NPC,self).__init__(spawnPt=pt)        
        self.load("assets/"+characterType+"/"+entityName)
        self.speed = 100.0
        self.characterType = characterType
        self.zval = 3
        
    def update(self, timeSinceLastUpdate, *args, **kwargs):
        """Update method for NPC in Longsword
        
        Keyword arguments:
        timeSinceLastUpdate -- time elapsed since the last time this update was called
        args -- list of arguments to this update method
        kwargs --         
        """
        #Call super class update
        super(NPC,self).update(timeSinceLastUpdate, *args, **kwargs)
        self.translate(self.speed*timeSinceLastUpdate*-1, 0.0)
        if not self.currentAnimation:
            self.playAnimation("walkLeft")
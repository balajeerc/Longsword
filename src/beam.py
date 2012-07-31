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
from cocos import collision_model

import entity
import debug
import math

class BeamSubCollider():
    def __init__(self,center,radius):
        self.cshape = cocos.collision_model.CircleShape(center,radius)
        self.beamSubCollider = True
        self.entityName = "beamCollider"
        
class Beam(entity.Entity):
    """Player's beam for Longsword"""

    def __init__(self):
        super(Beam,self).__init__()
        self.zval = 2 #To make sure that the beam is in front of player
        self.load("assets/beam")
        self.sprite.transform_anchor_x -= self.sprite.get_rect().width*0.5
        #We need to compose the beam of various smaller spheres along the
        #the beam so that it can test collision with enemies
        self.subColliders = []
        numSubColliders = int(self.sprite.width/20)+1
        for i in range(numSubColliders):
            center = self.sprite.position
            radius = 10
            collider = BeamSubCollider(center,radius)
            self.subColliders.append(collider)
        self.updateColliderPositions()       
        
    def updateColliderPositions(self):
        beamOrigin = self.sprite.transform_anchor_x
        cosRot = math.cos(self.sprite.rotation*math.pi/180.0)
        sinRot = math.sin(self.sprite.rotation*math.pi/180.0)
        for i in range(len(self.subColliders)):
            pos = cocos.euclid.Vector2(beamOrigin+i*10*cosRot,
                                       beamOrigin+i*10*sinRot)
            self.subColliders[i].center = pos
            
    def addToCollisionManager(self,collisionManager):
        for collider in self.subColliders:
            collisionManager.add(collider)    
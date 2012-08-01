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

import math

import pyglet
import cocos
from cocos import collision_model

import entity
import debug
import util

class BeamSubCollider():
    def __init__(self,center,radius):
        self.cshape = cocos.collision_model.CircleShape(center,radius)
        self.beamSubCollider = True
        self.entityName = "beamCollider"
        self.circlePts = util.generateCirclePoints(radius, 12)
        self.boundLines = []
        self.initBoundLines()
        self.boundsVisible = False
        #This beam sub-collider is a not a collider as are the regular
        #entity colliders, hence
        self.isCollider = False
        
    def getCirclePts(self):
        offsetPts = []
        for pt in self.circlePts:
            offsetPt = self.cshape.center + pt
            offsetPts.append(offsetPt)
        return offsetPts
    
    def initBoundLines(self):
        for pt in self.circlePts:
            self.boundLines.append(cocos.draw.Line((0,0),(100,100),(255,255,255,255)))
            self.boundLines[len(self.boundLines)-1].visible = False
        self.updateBounds(True)
            
    def updateBounds(self, forceUpdate=False):
        if forceUpdate or self.boundsVisible:                
            offsetPts = self.getCirclePts()
            #print("OffsetPt1 - ("+str(offsetPts[0].x)+","+str(offsetPts[0].y)+")")
            #print("CshapeCenter - ("+ str(self.cshape.center[0])+","+str(self.cshape.center[1])+")")
            for i in range(len(offsetPts)-1):
                self.boundLines[i].start = offsetPts[i]
                self.boundLines[i].end = offsetPts[i+1]
            #We also add the closing line
            self.boundLines[len(offsetPts)-1].start = offsetPts[len(offsetPts)-1]
            self.boundLines[len(offsetPts)-1].end = offsetPts[0]        
        
    def showBounds(self,show=True):
        for line in self.boundLines:
            line.visible = show
        self.boundsVisible = show
            
    def register(self,gameLayer):
        for line in self.boundLines:
            gameLayer.add(line)     
            
class Beam(entity.Entity):
    """Player's beam for Longsword"""

    def __init__(self):
        super(Beam,self).__init__()
        self.isBeam = True
        self.zval = 2 #To make sure that the beam is in front of player
        self.load("assets/beam")
        self.sprite.transform_anchor_x -= self.sprite.get_rect().width*0.5
        #We need to compose the beam of various smaller spheres along the
        #the beam so that it can test collision with enemies
        self.subColliders = []
        numSubColliders = int(self.sprite.width/20)+1
        for i in range(numSubColliders):
            center = cocos.euclid.Vector2(self.sprite.x,self.sprite.y)
            radius = 10
            collider = BeamSubCollider(center,
                                       radius)
            self.subColliders.append(collider)
        self.updateColliderPositions()       
        self.boundsVisible = False
    
    def register(self, gameLayer):
        super(Beam,self).register(gameLayer)
        for collider in self.subColliders:
            collider.register(gameLayer)
        
    def updateColliderPositions(self):
        beamOriginX = self.sprite.position[0]-self.sprite.width*0.5*math.cos(self.sprite.rotation*math.pi/180) 
        beamOriginY = self.sprite.position[1]       
        #beamOriginX = self.sprite.transform_anchor[0]
        #beamOriginY = self.sprite.transform_anchor[1]
        #print("New location- x:"+str(beamOriginX)+", y:"+str(beamOriginY))
        cosRot = math.cos(self.sprite.rotation*math.pi*-1/180.0)
        sinRot = math.sin(self.sprite.rotation*math.pi*-1/180.0)
        for i in range(len(self.subColliders)):
            pos = cocos.euclid.Vector2(beamOriginX+i*10*cosRot*2,
                                       beamOriginY+i*10*sinRot*2)
            self.subColliders[i].cshape.center = pos
            self.subColliders[i].updateBounds()
            
    def addToCollisionManager(self,collisionManager):
        for collider in self.subColliders:
            collisionManager.add(collider)
            
    def showBounds(self,show=True):
        for collider in self.subColliders:
            collider.showBounds(show)
        self.boundsVisible = show    

    def updateCollision(self):
        """Updates the colllision shape, after the game logic phase of game update"""
        super(Beam,self).updateCollision()
        self.updateColliderPositions()
         
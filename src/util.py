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
import cocos

def generateCirclePoints(radius,subdivisions=12):
    """Returns a list of points that, when connected with lines,can be used
    to draw a circle. Increased subdivisions count leads to smoother circles.
    
    Keyword arguments:
    radius -- radius of circle
    subdivisions -- number of subdivisions on the circle's circumference
    """
    if subdivisions < 6:
        subdivisions = 6
    
    circlePts = []
    angularInterval = 2*math.pi/subdivisions
    for i in range(subdivisions):
        circlePt = cocos.euclid.Vector2(0.0,0.0)
        circlePt.x = radius*math.cos(angularInterval*i)
        circlePt.y = radius*math.sin(angularInterval*i)
        circlePts.append(circlePt)
        
    return circlePts    
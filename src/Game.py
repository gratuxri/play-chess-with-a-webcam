#!/usr/bin/python
# -*- encoding: utf-8 -*-
# part of https://github.com/WolfgangFahl/play-chess-with-a-webcam
from JsonAbleMixin import JsonAbleMixin
from YamlAbleMixin import YamlAbleMixin
import numpy as  np

class Game(JsonAbleMixin):
    """ keeps track of a games state in a JavaScript compatible way to exchange game State information
    across platforms e.g. between Python backend and JavaScript frontend"""
    
    def __init__(self, name):
        self.name=name

        
    
class WebCamGame(JsonAbleMixin):
    """ keeps track of a webcam games state in a JavaScript compatible way to exchange game and webcam/board State information
    across platforms e.g. between Python backend and JavaScript frontend"""
    
    def __init__(self, name):
        self.name=name
        self.game=Game(name)
        self.warp=Warp()
        

class Warp(YamlAbleMixin, JsonAbleMixin):
    """ holds the trapezoid points to be use for warping an image take from a peculiar angle """

    # construct me from the given setting
    def __init__(self, pointList=[], rotation=0, bgrColor=(0, 255, 0)):
        self.rotation = rotation
        self.bgrColor = bgrColor
        self.pointList = pointList
        self.updatePoints()

    def rotate(self, angle):
        self.rotation = self.rotation + angle
        if self.rotation >= 360:
            self.rotation = self.rotation % 360

    def updatePoints(self):
        pointLen = len(self.pointList)
        if pointLen == 0:
            self.points = None
        else:
            self.points = np.array(self.pointList)
        self.warping = pointLen == 4

    def addPoint(self, px, py):
        """ add a point with the given px,py coordinate
        to the warp points make sure we have a maximum of 4 warpPoints if warppoints are complete when adding reset them
        this allows to support click UIs that need an unwarped image before setting new warp points.
        px,py is irrelevant for reset """
        if len(self.pointList) >= 4:
            self.pointList = []
        else:
            self.pointList.append([px, py])
        self.updatePoints()
#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# part of https://github.com/WolfgangFahl/play-chess-with-a-webcam
from StateDetector import StateDetector
from StateDetector import  CannotBuildStateException
from HelpTesting import TheTestEnv

testEnv=TheTestEnv()
# test the StateDetector
def test_StateDetector():
    for index in range(0,9):
        image=testEnv.getImage(index+1)
        stateDetector=StateDetector()
        try:
            stateDetector.detectState(image)
        except  CannotBuildStateException as cbse:
            print(cbse)
            pass
        
test_StateDetector()

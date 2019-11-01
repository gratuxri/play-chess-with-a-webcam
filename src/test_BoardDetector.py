#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# part of https://github.com/WolfgangFahl/play-chess-with-a-webcam
from webchesscam import  WebChessCamArgs
from BoardDetector import BoardDetector
from Board import Board
from Video import Video
from timeit import default_timer as timer
from WebApp import WebApp
from RunningStats import ColorStats
from Environment import TestEnvironment
import cv2

testEnv = TestEnvironment()
frameDebug = True


def test_BoardFieldColorDetector():
    video = Video()
    board = Board()
    board.chessboard.clear()
    image = video.readImage(testEnv.testMedia + "chessBoard011.jpg")
    # this is a still image
    frameIndex = 1
    BoardDetector.debug = True
    boardDetector = BoardDetector(board, video)
    maxDistance = 5
    maxSteps = 7
    stepSteps = 1
    # how long to show results (e.g. 2 secs)
    totalWaitTime = 2000
    # wait only a fraction of the totalWaitTime
    waitTime = int(totalWaitTime / (maxDistance * maxSteps / stepSteps))
    for distance in range(1, maxDistance + 1, 1):
        for step in range(1, maxSteps + 1, stepSteps):
            testImage = image.copy()
            start = timer()
            testImage = boardDetector.analyze(testImage, frameIndex, distance, step)
            end = timer()
            count = (2 * distance + 1) * (2 * distance + 1)
            size = distance * (step + 1)
            if frameDebug:
                print("%.3fs for distance %2d with %4d pixels %2d x %2d " % (end - start, distance, count, size, size))  # Time in seconds, e.g. 5.38091952400282
            video.showImage(testImage, "fields", True, waitTime)
    video.close()


def test_FieldDetector():
    video = Video()
    webApp = WebApp(WebChessCamArgs(["--debug","--speedup=4"]).args)
    frames = None
    for boardIndex in range(2):
        BoardDetector.debug = True
        # setup webApp params to reuse warp method
        webApp.video = video
        if boardIndex == 1:
            video.open(testEnv.testMedia + 'emptyBoard001.avi')
            webApp.board.chessboard.clear_board()
            frames = 16
        if boardIndex == 0:
            video.open(testEnv.testMedia + 'scholarsmate.avi')
            frames = 20
            # @TODO speed up and test all frames again
            # frames=334
        webApp.warp.rotation = 270
        webApp.warp.pointList = []
        webApp.warp.addPoint(140, 5)
        webApp.warp.addPoint(506, 10)
        webApp.warp.addPoint(507, 377)
        webApp.warp.addPoint(137, 374)

        for frame in range(0, frames):
            ret, bgr, quitWanted = video.readFrame(show=False)
            assert ret
            assert bgr is not None
            # bgr = cv2.cvtColor(jpgImage, cv2.COLOR_RGB2BGR)
            height, width = bgr.shape[:2]
            # print ("%d: %d x %d" % (frame,width,height))
            start = timer()
            bgr = webApp.warpAndRotate(bgr)
            image = cv2.resize(bgr, (int(width * 1.5), int(height * 1.5)))
            video.showImage(image, "BoardDetector", keyWait=200)
            end = timer()
    video.close()


def test_ColorDistance():
    assert 25 == ColorStats.square(5)
    cStats = ColorStats()
    cStats.push(128, 128, 128)
    colorKey = cStats.colorKey()
    assert 49152 == colorKey
    
def test_FieldStates():    
    video=Video()
    board = Board()
    BoardDetector.debug = True
    boardDetector = BoardDetector(board, video)
    sortedFields=boardDetector.sortByFieldState();
    counts = board.fieldStateCounts()    
    for fieldState,fields in sortedFields.items():
        print ("%s: %2d" % (fieldState,len(fields)))
        assert counts[fieldState]==len(fields)

def test_MaskFieldStates():
    pass    
    

test_ColorDistance()
test_FieldStates()
test_MaskFieldStates()
test_BoardFieldColorDetector()
test_FieldDetector()

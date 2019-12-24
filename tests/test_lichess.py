'''
Created on 2019-12-21

@author: wf
'''
from pcwawc.lichess import Lichess
from pcwawc.lichess import Game as LichessGame
import getpass
import lichess.api

debug=True
def test_lichess():
    lichess=Lichess()
    if lichess.client is not None:
        account=lichess.getAccount()
        if debug:
            print(account)
        #print(account.adict)
        pgn="""[Event "Play Chess With a WebCam"]
[Site "Willich, Germany"]
[Date "2019-12-21 12:46:49"]
[Round "1"]
[White "Wolfgang"]
[Black "Maria"]
[Result "1-0"]

1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7# 1-0"""
        lichess.pgnImport(pgn)
    pass

def test_game():
    game_id="cpOszEMY"
    lichess=Lichess()
    game=lichess.game(game_id)
    assert game["id"]==game_id
    assert game["moves"]=="e4 e5 Bc4 Nc6 Qh5 Nf6 Qxf7#"
    
class MoveHandler():
    def __init__(self,game,movesToPlay):
        self.game=game
        self.movesToPlay=movesToPlay
        pass
    
    def onState(self,event):
        state=event.state    
        print ("%3d moves played: %s" % (state.moveIndex+1,state.moves))
        index=state.moveIndex+1
        if index<len(self.movesToPlay):
            self.game.move(self.movesToPlay[index])
        
        
def test_OTB_stream():
    if getpass.getuser()=="wf":
        lichess=Lichess(debug=True)
        # challenge my self
        lichess.challenge(lichess.getAccount().username)
        game_id=lichess.waitForChallenge()
        game=LichessGame(lichess,game_id,debug=True)
        moveHandler=MoveHandler(game,["e2e4","e7e5","f1c4","b8c6"])
        game.subscribe(moveHandler.onState)
        game.start()
        #game.move('e2e4')
        #game.move('e7e5')  
        #game.move('f1c4')
        #game.move('b8c6')
        #game.abort()
        # game.move('b8c6')
        #game.resign()
        #game.stop()
       
def test_rating():
    user = lichess.api.user('thibault')
    rating=user['perfs']['blitz']['rating']
    assert rating>1000   

#test_rating()    
#test_lichess()
#test_game()
test_OTB_stream()

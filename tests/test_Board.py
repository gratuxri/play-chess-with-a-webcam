#!/usr/bin/python3
# part of https://github.com/WolfgangFahl/play-chess-with-a-webcam
from pcwawc.Board import Board
from pcwawc.Field import FieldState
import chess


# check the sequence of  moves end positon against the expected FEN notation string
def checkMovesEndPosition(moves, expectedFen):
    board = Board()
    for move in moves:
        san = board.performMove(move)
        print (san)
    checkEndPosition(board, expectedFen)


# check the expected end position
def checkEndPosition(board, expectedFen):
    print("---Final positions---")
    fen = board.fen()
    print (fen)
    unicode = board.unicode()
    print (unicode)
    pgn = board.getPgn()
    print (pgn)
    assert expectedFen == fen


# test the board state using "easy" notation
def test_BoardEasy():
    moves = [
        ['D2', 'D4'],  # d4
        ['G8', 'F6'],  # Nf6
        ['C2', 'C4'],  # c4
        ['E7', 'E6'],  # e6
        ['C4', 'C5'],  # c5
        ['F8', 'D6'],  # Bd6
        ['D1', 'A4'],  # Qa4
        ['B7', 'B5'],  # b5
        ['B5', 'B6'],  # cxb6, En Passant
        ['E8', 'G8'],  # 0-0
        ['B6', 'C7']  # bxc7, Hidden eat
    ]
    expectedFen = "rnbq1rk1/p1Pp1ppp/3bpn2/2P5/Q2P4/8/PP2PPPP/RNB1KBNR"
    checkMovesEndPosition(moves, expectedFen)


# test using pgn notation
def test_BoardPgn():
    pgn = "1. d4 Nf6 2. c4 e6 3. c5 Bd6 4. Qa4 b5 5. cxb6 O-O 6. bxc7"
    board = Board()
    board.setPgn(pgn)
    expectedFen = "rnbq1rk1/p1Pp1ppp/3bpn2/8/Q2P4/8/PP2PPPP/RNB1KBNR"
    checkEndPosition(board, expectedFen)


def test_cellNames():
    board = Board()
    astr = ""
    for row in range(0, 8):
        for col in range(0, 8):
            fieldName = board.GetCellName(col, row)
            field = board.fieldAt(row, col)
            # print (row,col,fieldName,field.an)
            assert field.an.upper() == fieldName
            astr = astr + fieldName
    print (astr)
    assert astr == "A8B8C8D8E8F8G8H8A7B7C7D7E7F7G7H7A6B6C6D6E6F6G6H6A5B5C5D5E5F5G5H5A4B4C4D4E4F4G4H4A3B3C3D3E3F3G3H3A2B2C2D2E2F2G2H2A1B1C1D1E1F1G1H1"


def test_Pieces():
    board = Board()
    assert board.piecesOfColor(chess.WHITE) == 16
    assert board.piecesOfColor(chess.BLACK) == 16
    counts = board.fieldStateCounts()
    assert len(counts) == 6
    assert counts[FieldState.WHITE_EMPTY] == 16
    assert counts[FieldState.WHITE_BLACK] == 8
    assert counts[FieldState.WHITE_WHITE] == 8

    assert counts[FieldState.BLACK_EMPTY] == 16
    assert counts[FieldState.BLACK_BLACK] == 8
    assert counts[FieldState.BLACK_WHITE] == 8

    print (board.unicode())
    bstr = ""
    for row in range(0, 8):
        for col in range(0, 8):
            field = board.fieldAt(row, col)
            piece = field.getPiece()
            bstr = bstr + field.an
            # print (row,col,piece)
            if piece is not None:
                bstr += piece.symbol()
                if piece.symbol().upper == "Q":
                    assert piece.color == field.fieldColor
    #print(bstr)
    assert bstr == "a8rb8nc8bd8qe8kf8bg8nh8ra7pb7pc7pd7pe7pf7pg7ph7pa6b6c6d6e6f6g6h6a5b5c5d5e5f5g5h5a4b4c4d4e4f4g4h4a3b3c3d3e3f3g3h3a2Pb2Pc2Pd2Pe2Pf2Pg2Ph2Pa1Rb1Nc1Bd1Qe1Kf1Bg1Nh1R"
    board.chessboard.clear()
    assert board.piecesOfColor(chess.WHITE) == 0
    assert board.piecesOfColor(chess.BLACK) == 0


def test_PieceAt():
    """
    see https://stackoverflow.com/questions/55650138/how-to-get-a-piece-in-python-chess
    see https://python-chess.readthedocs.io/en/latest/core.html """
    debug = False
    board = chess.Board()
    if debug:
        print (board.unicode())
        print(" square | row | col | type | piece | color | field")
        print("--------+-----+-----+------+-------+-------+------")
    for row in range(0, 8):
        for col in range(0, 8):
            squareIndex = row * 8 + col
            square = chess.SQUARES[squareIndex]
            piece = board.piece_at(square)
            fieldColor = (col + row) % 2 != 1
            if piece is None:
                assert row in {2, 3, 4, 5}
            else:
                if debug:
                    print("%7d | %3d | %3d | %4d | %5s | %4s | %4s" % (square, row, col, piece.piece_type, piece.symbol(), "white" if piece.color else "black", "black" if fieldColor else "white"))
                if row in {0, 1}:
                    assert piece.color == chess.WHITE
                    # white symbols are upper case
                    assert ord(piece.symbol()) > ord('A') and ord(piece.symbol()) < ord('Z')
                if row in {6, 7}:
                    assert piece.color == chess.BLACK
                    # black symbols are lower case
                    assert ord(piece.symbol()) > ord('a') and ord(piece.symbol()) < ord('z')


test_PieceAt()
test_Pieces()
test_cellNames()
test_BoardEasy()
test_BoardPgn()

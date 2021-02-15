import random

class GameService:

    def __init__(self, boardservice, movementservice):

        self.boardService = boardservice
        self.movementService = movementservice
        self.moveResult = MoveResult()
        self.initializegame()

    def initializegame(self):

        self.moveResult = MoveResult()
        self.moveResult.Position = "A1"
        self.moveResult.Lives = 3

    def getcurrentgamestatus(self):

        return self.moveResult

    def makemove(self, direction):

        try:
            self.moveResult.Message = ""
            requestedPosition = self.movementService.calculatenewposition(self.moveResult.Position, direction)
            hasMine = self.boardService.hasmine(requestedPosition)
            if not hasMine:
                self.createsuccessfulmoveresult(requestedPosition)
            else:
                self.createinvalidmoveresult()

        except Exception as e:

            self.moveResult.IsValid = False
            self.moveResult.Message = e

        self.moveResult.Score = self.moveResult.Score + 1

        return self.moveResult

    def createinvalidmoveresult(self):

        self.moveResult.IsValid = False
        self.moveResult.Lives = self.moveResult.Lives - 1
        if self.moveResult.Lives > 0:
            self.moveResult.Message = "Bang! You've hit a mine"
        else:
            self.moveResult.Message = "Game over. You have failed!"
            self.moveResult.GameFinished = True

    def createsuccessfulmoveresult(self, requestedposition):

        self.moveResult.IsValid = True
        self.moveResult.Position = requestedposition
        if requestedposition.endswith("8"):
            self.moveResult.Message = "Congratulations! You have won!"
            self.moveResult.GameFinished = True


class MoveResult:
    def __init__(self):
        self.IsValid = False
        self.Position = ""
        self.Message = ""
        self.Score = 0
        self.Lives = 0
        self.GameFinished = False


class BoardService:

    def __init__(self, minepositions = None):
        if minepositions is None:
            self.initialize()
        else:
            self.minePositions = minepositions

    def initialize(self):
        self.minePositions = list()
        columns = list("ABCDEFGH")
        rows = list("2345678")

        for rw in rows:
            self.minePositions.append(f"{columns[random.randint(0, 7)]}{rw}")


    def hasmine(self, square):
        return square in self.minePositions


class MovementService:

    def calculatenewposition(self, currentposition, direction):
        if direction is None or direction is "":
            raise Exception("Direction not specified")
        currentpositionchars = list(currentposition)
        newposition = ""
        sanitiseddirection = direction.lower().strip()
        if sanitiseddirection == "right":
            currentpositionchars[0] = chr(ord(currentpositionchars[0]) + 1)
            newposition = f"{currentpositionchars[0]}{currentpositionchars[1]}"

        if sanitiseddirection == "left":
            currentpositionchars[0] = chr(ord(currentpositionchars[0]) - 1)
            newposition = f"{currentpositionchars[0]}{currentpositionchars[1]}"

        if sanitiseddirection == "down":
            currentpositionchars[1] = chr(ord(currentpositionchars[1]) - 1)
            newposition = f"{currentpositionchars[0]}{currentpositionchars[1]}"

        if sanitiseddirection == "up":
            currentpositionchars[1] = chr(ord(currentpositionchars[1]) + 1)
            newposition = f"{currentpositionchars[0]}{currentpositionchars[1]}"

        if sanitiseddirection != "up" and sanitiseddirection != "down" and sanitiseddirection != "left" and sanitiseddirection != "right":
            raise Exception("Invalid Direction specified")

        if newposition[0] not in "ABCDEFGH" or newposition[1] not in "12345678":
            raise Exception("Move outside board boundary error")

        return newposition





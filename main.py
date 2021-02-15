import minesweeper


def displaygamestartmessages(gameservice):
    print("************************")
    print("Welcome to Mine Sweeper!")
    print("************************")

    print(f"Current position: {gameservice.getcurrentgamestatus().Position}")
    print(f"Lives remaining:  {gameservice.getcurrentgamestatus().Lives}")
    print("Left, Right, Up or Down + <ENTER> to move")


def displaymoveresultmessages(moveresult):
    if not moveresult.IsValid:
        print(moveresult.Message)

    print(f"Score:           {moveresult.Score}")
    print(f"Position:        {moveresult.Position}")
    print(f"Lives remaining: {moveresult.Lives}")
    print("Left, Right, Up or Down + <ENTER> to move")


def displaygamefinishedmessage(moveresult):
    print(moveresult.Message)
    print(f"Score: {moveresult.Score}")
    print("Press <ENTER> to terminate")


boardService = minesweeper.BoardService()
movementService = minesweeper.MovementService()
gameService = minesweeper.GameService(boardService, movementService)
displaygamestartmessages(gameService)
command = input()
result = gameService.makemove(command)
while not result.GameFinished:
    displaymoveresultmessages(result)
    command = input()
    result = gameService.makemove(command)

displaygamefinishedmessage(result)
command = input()





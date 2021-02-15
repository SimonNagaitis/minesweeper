import unittest
import minesweeper


class MockBoardService:

    def __init__(self):
        self.hasminereturnvalue = False
        self.hasminewascalled = False

    def initialize(self):
        dummy = True

    def hasmine(self, square):
        self.hasminewascalled = True
        return self.hasminereturnvalue


class MockMovementService:

    def __init__(self):
        self.newpositionvalue = "C2"
        self.throwsexception = False
        self.calculatenewpositionwascalled = False

    def calculatenewposition(self, currentposition, direction):
        self.calculatenewpositionwascalled = True
        if self.throwsexception:
            raise Exception("Test")
        return self.newpositionvalue


class TestGameService(unittest.TestCase):

    def setUp(self):
        self.mockboardservice = MockBoardService()
        self.mockmovementservice = MockMovementService()
        self.gameservice = minesweeper.GameService(self.mockboardservice, self.mockmovementservice)

    def test_makemove_returns_move_result(self):
        result = self.gameservice.makemove(None)
        self.assertIsInstance(result, minesweeper.MoveResult)

    def test_makemove_calls_movementservice(self):
        result = self.gameservice.makemove("up")
        self.assertEqual(self.mockmovementservice.calculatenewpositionwascalled, True)

    def test_makemove_increments_score(self):
        result = self.gameservice.makemove("up").Score
        secondresult = self.gameservice.makemove("up").Score
        self.assertEqual(secondresult, result + 1)

    def test_makemove_returns_new_player_position(self):
        result = self.gameservice.makemove("up")
        self.assertEqual(result.Position, "C2")

    def test_makemove_returns_invalidmove_and_message_if_movementservce_returns_error(self):
        self.mockmovementservice.throwsexception = True
        result = self.gameservice.makemove("up")
        #self.assertEqual(result.Message, Exception("Test"))
        self.assertEqual(result.IsValid, False)

    def test_makemove_calls_boardservice(self):
        result = self.gameservice.makemove("up")
        self.assertEqual(self.mockboardservice.hasminewascalled, True)

    def test_makemove_returns_correctmessage_if_mineencountred(self):
        self.mockboardservice.hasminereturnvalue = True
        result = self.gameservice.makemove("up")
        self.assertEqual(result.Message, "Bang! You've hit a mine")
        self.assertEqual(result.IsValid, False)

    def test_makemove_decrements_lives_if_mine_encountered(self):
        self.mockboardservice.hasminereturnvalue = True
        self.gameservice = minesweeper.GameService(self.mockboardservice, self.mockmovementservice)
        result = self.gameservice.makemove("up")
        self.assertEqual(result.Lives, 2)

    def test_makemove_returns_correctmessage_if_lives_zero(self):
        self.mockboardservice.hasminereturnvalue = True
        result = self.gameservice.makemove("up")
        result = self.gameservice.makemove("up")
        result = self.gameservice.makemove("up")
        self.assertEqual(result.Lives, 0)
        self.assertEqual(result.Message, "Game over. You have failed!")
        self.assertEqual(result.GameFinished, True)

    def test_makemove_returns_correctmessage_if_player_moves_to_row_8(self):
        self.mockmovementservice.newpositionvalue = "B8"
        result = self.gameservice.makemove("up")
        self.assertEqual(result.Message, "Congratulations! You have won!")
        self.assertEqual(result.GameFinished, True)



class TestBoardService(unittest.TestCase):

    def setUp(self):
        minelist = list(["A1", "C3"])
        self.boardservice = minesweeper.BoardService(minelist)

    def test_has_mine_returns_true_if_position_in_list(self):
        result = self.boardservice.hasmine("A1")
        self.assertTrue(result)

    def test_has_mine_returns_false_if_position_not_in_list(self):
        result = self.boardservice.hasmine("B2")
        self.assertFalse(result)

    def test_initialize_creates_one_mine_for_each_row(self):
        self.boardservice.initialize()
        columns = list("ABCDEFGH")
        rows = list("2345678")
        for rw in rows:
            minecount = 0
            for i in range(0, 8):
                if self.boardservice.hasmine(f"{columns[i]}{rw}"):
                    minecount = minecount + 1
            self.assertEqual(minecount, 1)


class TestMovementService(unittest.TestCase):

    def setUp(self):

        self.movementservice = minesweeper.MovementService()

    def test_calculatenewposition_throws_exception_if_parameter_null(self):

        self.assertRaises(Exception, self.movementservice.calculatenewposition, None, None)

    def test_calculatenewposition_accepts_up(self):
        result = self.movementservice.calculatenewposition("B2", "up")
        self.assertEqual("B3", result)

    def test_calculatenewposition_throws_exception_if_invalid_direction_specified(self):
        self.assertRaises(Exception, self.movementservice.calculatenewposition,"B2", "bob")

    def test_calculatenewposition_accepts_down(self):
        result = self.movementservice.calculatenewposition("B2", "down")
        self.assertEqual("B1", result)

    def test_calculatenewposition_accepts_left(self):
        result = self.movementservice.calculatenewposition("B2", "left")
        self.assertEqual("A2", result)

    def test_calculatenewposition_accepts_right(self):
        result = self.movementservice.calculatenewposition("B2", "right")
        self.assertEqual("C2", result)

    def test_calculatenewposition_throws_exception_if_boundary(self):
        self.assertRaises(Exception, self.movementservice.calculatenewposition,"A1", "left")








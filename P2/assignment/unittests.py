import unittest
import queens


class TestEightQueens(unittest.TestCase):
    """ This class is used to test important
        functionalities of the queens.py module.
    """

    def test_attacking_queens_row(self):
        state = "12546568"
        eight_queens = queens.EightQueens()
        eight_queens.fill_board(state)
        self.assertEqual(4, eight_queens.get_queens_in_row())

    def test_attacking_queens_diagonal(self):
        state = "12546568"
        eight_queens = queens.EightQueens()
        eight_queens.fill_board(state)
        self.assertEqual(10, eight_queens.get_queens_in_diagonal())

    def test_attacking_queens_total(self):
        state = "12546568"
        eight_queens = queens.EightQueens()
        self.assertEqual(14, eight_queens.get_attacking_queens_count(state))

    # def test_state_to_long(self):
    #    state = "12546568312313"
    #    with self.assertRaises(SystemExit) as cm:
    #        queens.EightQueens(state)
    #    self.assertEqual(cm.exception.code, queens.WRONG_STATE_WARNING)

    # def test_state_wrong_numbers(self):
    #    state = "02999993"
    #    with self.assertRaises(SystemExit) as cm:
    #        queens.EightQueens(state)
    #    self.assertEqual(cm.exception.code, queens.WRONG_STATE_WARNING)

    def test_mutate(self):
        for i in range(100):
            state = "12546568"
            eight_queens = queens.EightQueens()
            eight_queens.fill_board(state)
            mutation_result = eight_queens.mutate(state)
            self.assertNotEqual(mutation_result, state)

    def test_crossover(self):
        eight_queens = queens.EightQueens()
        first_state = "11112222"
        second_state = "33334444"
        cut_position = 4
        result_first_half = "33332222"
        FIRST_HALF = 1
        self.assertEqual(result_first_half, eight_queens.swap_halves(
                         first_state, second_state, cut_position,
                         FIRST_HALF)[0])
        result_second_half = "11114444"
        SECOND_HALF = 0
        self.assertEqual(result_second_half, eight_queens.swap_halves(
                         first_state, second_state, cut_position,
                         SECOND_HALF)[0])


if __name__ == '__main__':
    unittest.main()

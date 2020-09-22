import unittest
from inference_algorithm import Resolution, ForwardChaining
from inference_algorithm import ResolutionKnowledgeBase
from hunt_the_wumpus import (INFERENCE_ALGORITHM_FORWARD_CHAINING,
                             INFERENCE_ALGORITHM_RESOLUTION)
from WumpusWorld import Wumpus_World
from WorldState import Action


class TestResolutionAlgorithm(unittest.TestCase):
    """ This class is used to test error prone functionalities
        of the hunt_the_wumpus.py module.
    """

    @classmethod
    def setUpClass(cls):
        """ This method is called once when the test class loads.
            Creates our resolution object on which we test our functions here.
        """
        cls.inference_algorithm = Resolution()

    @classmethod
    def tearDown(cls):
        """ This method is called after every test case.
        """
        cls.inference_algorithm.knowledge_base.rules = []

    @classmethod
    def setUp(cls):
        """ This method is called before every test case.
        """
        cls.world = Wumpus_World(INFERENCE_ALGORITHM_RESOLUTION)

    def test_resolve_left_clause_empty(cls):
        left_clause = {""}
        right_clause = {"W11", "W22", "W33"}
        result_as_list = cls.inference_algorithm.resolve(left_clause,
                                                         right_clause)
        for resulting_set in result_as_list:
            if {""}.issubset(resulting_set):
                return True
        return False

    def test_resolve_right_clause_empty(cls):
        left_clause = {"W11", "W22", "W33"}
        right_clause = {""}
        result_as_list = cls.inference_algorithm.resolve(left_clause,
                                                         right_clause)
        for resulting_set in result_as_list:
            if {""}.issubset(resulting_set):
                return True
        return False

    def test_resolve_resulting_in_empty_clause(cls):
        left_clause = {"W11"}
        right_clause = {"-W11"}
        result_as_list = cls.inference_algorithm.resolve(left_clause,
                                                         right_clause)
        for resulting_set in result_as_list:
            if {""}.issubset(resulting_set):
                return True
        return False

    def test_resolve_resulting_in_non_empty_clause(cls):
        left_clause = {"P33", "W11"}
        right_clause = {"P22", "-W11"}
        result_as_list = cls.inference_algorithm.resolve(left_clause,
                                                         right_clause)
        for resulting_set in result_as_list:
            if {"P33", "P22"}.issubset(resulting_set):
                return True
        return False

    def test_resolve_with_multiple_matches(cls):
        left_clause = {"P11", "P22"}
        right_clause = {"-P22", "-P11"}
        result_as_list = cls.inference_algorithm.resolve(left_clause,
                                                         right_clause)
        expected_resolvent1 = {'P11', '-P11'}
        expected_resolvent2 = {'-P22', 'P22'}
        first_match = False
        second_match = False
        for resolvent in result_as_list:
            if resolvent == expected_resolvent1:
                first_match = True
            if resolvent == expected_resolvent2:
                second_match = True
        if (first_match and second_match):
            return True
        else:
            return False

    def test_string_to_set(cls):
        kb = ResolutionKnowledgeBase()
        input_string = "W11vP22vP33"
        expected_set = {'W11', 'P22', 'P33'}
        cls.assertEqual(kb.string_to_set(input_string), expected_set)

    def test_add_to_knowledge_base_atomic_literal(cls):
        cls.inference_algorithm.tell("-P12")
        cls.inference_algorithm.tell("W22")
        cls.inference_algorithm.tell("-W01")
        cls.inference_algorithm.tell("P32")
        expected_result = [{"-P12"}, {"W22"}, {"-W01"}, {"P32"}]
        cls.assertEqual(cls.inference_algorithm.knowledge_base.rules,
                        expected_result)

    def test_resolution_true_single_step(cls):
        cls.inference_algorithm.knowledge_base.add_to_kb("W22vW33vW10")
        cls.inference_algorithm.knowledge_base.add_to_kb("P01")
        cls.inference_algorithm.knowledge_base.add_to_kb("W01")
        cls.assertTrue(cls.inference_algorithm.ask("W01"))

    def test_resolution_true_multiple_steps(cls):
        cls.inference_algorithm.knowledge_base.add_to_kb("W22vW33vW10")
        cls.inference_algorithm.knowledge_base.add_to_kb("P01")
        cls.inference_algorithm.knowledge_base.add_to_kb("W01vW11")
        cls.inference_algorithm.knowledge_base.add_to_kb("-W11")
        cls.assertTrue(cls.inference_algorithm.ask("W01"))

    def test_resolution_false(cls):
        cls.inference_algorithm.knowledge_base.add_to_kb("W22vW33vW10")
        cls.inference_algorithm.knowledge_base.add_to_kb("P01")
        cls.inference_algorithm.knowledge_base.add_to_kb("-W01")
        cls.assertFalse(cls.inference_algorithm.ask("W01"))

    def test_practical_case_not_enough_knowledge_to_find_wumpus(cls):
        cls.assertFalse(cls.world.inference_algorithm.ask("W10"))

    def test_practical_case_enough_knowledge_to_find_wumpus(cls):
        cls.world.exec_action(Action.TURNLEFT)
        cls.world.exec_action(Action.WALK)
        cls.assertTrue(cls.world.inference_algorithm.ask("W10"))

    def test_practical_case_not_enough_knowledge_to_find_pit(cls):
        cls.world.exec_action(Action.TURNLEFT)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.assertFalse(cls.world.inference_algorithm.ask("P12"))

    def test_practical_case_enough_knowledge_to_find_pit(cls):
        cls.world.exec_action(Action.TURNLEFT)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.TURNRIGHT)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.TURNRIGHT)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.TURNRIGHT)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.TURNRIGHT)
        cls.world.exec_action(Action.WALK)
        cls.assertTrue(cls.world.inference_algorithm.ask("P12"))


class TestForwardChainingAlgorithm(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ This method is called once when the test class loads.
            Creates our resolution object on which we test our functions here.
        """
        cls.inference_algorithm = ForwardChaining()

    @classmethod
    def tearDown(cls):
        """ This method is called after every test case.
        """
        cls.inference_algorithm.knowledge_base.rules = []

    @classmethod
    def setUp(cls):
        """ This method is called before every test case.
        """
        cls.world = Wumpus_World(INFERENCE_ALGORITHM_FORWARD_CHAINING)

    def test_tell_single_literal(cls):
        cls.inference_algorithm.tell("W")
        clauses = cls.inference_algorithm.knowledge_base.clauses
        for clause in clauses:
            if "W" in clause.conclusion:
                return True
        return False

    def test_tell_implication(cls):
        cls.inference_algorithm.tell("P11,-P00=>W33")
        clauses = cls.inference_algorithm.knowledge_base.clauses
        if ("W33" in clauses[0].conclusion and "P11,-P00" in
                clauses[0].premise and clauses[0].count == 2):
            return True
        return False

    def test_ask_no_solution(cls):
        cls.inference_algorithm.tell("W11")
        cls.inference_algorithm.tell("P22")
        cls.inference_algorithm.tell("P33")
        cls.assertFalse(cls.inference_algorithm.ask("W00"))

    def test_practical_case_not_enough_knowledge_to_find_wumpus(cls):
        """ Makes the player spawn and ask if there is a wumpus at position
            x=1 y=0.
        """
        cls.assertFalse(cls.world.inference_algorithm.ask("W10"))

    def test_practical_case_enough_knowledge_to_find_wumpus(cls):
        """ Make the player spawn and walk around the wumpus.
            We should now able to detect if there is a wumpus at x=1 x=0
            for the fixed wumpus world config.
        """
        cls.world.exec_action(Action.TURNLEFT)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.TURNRIGHT)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.TURNRIGHT)
        cls.world.exec_action(Action.WALK)
        cls.assertTrue(cls.world.inference_algorithm.ask("W10"))

    def test_practical_case_not_enough_knowledge_to_find_pit(cls):
        cls.world.exec_action(Action.TURNLEFT)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.assertFalse(cls.world.inference_algorithm.ask("P12"))

    def test_practical_case_enough_knowledge_to_find_pit(cls):
        cls.world.exec_action(Action.TURNLEFT)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.TURNRIGHT)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.TURNRIGHT)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.TURNRIGHT)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.WALK)
        cls.world.exec_action(Action.TURNRIGHT)
        cls.world.exec_action(Action.WALK)
        cls.assertTrue(cls.world.inference_algorithm.ask("P12"))


if __name__ == '__main__':
    unittest.main()

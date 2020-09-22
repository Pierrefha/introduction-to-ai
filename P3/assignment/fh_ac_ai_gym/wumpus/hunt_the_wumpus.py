# import wumpus world class
from fh_ac_ai_gym.wumpus.WumpusWorld import Wumpus_World
from fh_ac_ai_gym.wumpus.WorldState import Action

# CONSTANTS
# todo maybe create globals file
INVALID_INPUT = -1
INFERENCE_ALGORITHM_RESOLUTION = 1
INFERENCE_ALGORITHM_FORWARD_CHAINING = 2
WRONG_INFERENCE_ALGORITHM_ERROR = "The inference algorithm you passed is"
"not supported!"


class Game:
    """ Entry point of the Hunt the Wumpus game. Creates the wumpus world and
        enables controlling the environment. Actions are passed via std input.
    """
    def __init__(self, inference_algorithm):
        self.wumpus_env = Wumpus_World(inference_algorithm)
        self.wumpus_env.print()

    def start(self):
        """ Starts the game. Repeatedly query the player for new actions.
        """
        while(True):
            action = self.parse_action()
            if (action == INVALID_INPUT):
                print("Skipping invalid input. Not executing an action.")
            else:
                # exec_action returns false if adventurer dies.
                if not self.wumpus_env.exec_action(action):
                    self.wumpus_env.print()
                    print("You have died. Game over!")
                    exit(0)
                self.wumpus_env.print()

    def parse_action(self):
        """ Reads standard input and returns corresponding action.
        """
        user_input = input("Your action:") or str(INVALID_INPUT)
        return {
                'K': Action.WALK,
                'J': Action.TURNLEFT,
                'L': Action.TURNRIGHT,
                'G': Action.GRAB,
                'S': Action.SHOOT,
                'C': Action.CLIMB,
                'A': Action.ASK,
                'T': Action.TELL,
                }.get(user_input[0].upper(), INVALID_INPUT)


if __name__ == '__main__':
    # init game using resolution as inference algorithm
    # game = Game(INFERENCE_ALGORITHM_RESOLUTION)
    # game.start()

    # init game using forward chaining as inference algorithm
    game = Game(INFERENCE_ALGORITHM_FORWARD_CHAINING)
    game.start()

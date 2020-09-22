import random


def swap_second_half(state_one, state_two, cut_position):
    """" Cuts both states at cut position and swaps
         the resulting second parts with each other.

         Returns a pair of cut and swapped states.
    """
    first_state_left = first_state[0:cut_position]
    first_state_right = second_state[cut_position:]
    second_state_left = second_state[0:cut_position]
    second_state_right = first_state[cut_position:]
    resulting_first = first_state_left+first_state_right
    resulting_second = second_state_left+second_state_right
    return (resulting_first, resulting_second)


def swap_first_half(state_one, state_two, cut_position):
    """" Cuts both states at cut position and swaps
         the resulting first parts with each other.

         Returns a pair of cut and swapped states.
    """
    first_state_right = first_state[cut_position:]
    first_state_left = second_state[0:cut_position:]
    second_state_right = second_state[cut_position:]
    second_state_left = first_state[0:cut_position:]
    resulting_first = first_state_left+first_state_right
    resulting_second = second_state_left+second_state_right
    return (resulting_first, resulting_second)


if __name__ == '__main__':
    first_state = "11112222"
    second_state = "33334444"
    print(f"first state:{first_state} second state: {second_state}")
    for i in range(5):
        cut_position = round(random.random()*5)+1
        if(random.random() > 0.5):
            print("swap first half")
            result = swap_first_half(first_state, second_state, cut_position)
            print("new first state: %s new second state: %s"
                  % (result[0], result[1]))
        else:
            print("swap second half")
            result = swap_second_half(first_state, second_state, cut_position)
            print("new first state: %s new second state: %s"
                  % (result[0], result[1]))

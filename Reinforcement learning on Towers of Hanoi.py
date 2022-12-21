import random

# Get the number of disks from the user
num_disks = int(input("Enter the number of disks: "))
info = "Disk 1 is the smallest and Disk " + str(num_disks) + " is the largest. The aim is to shift all the disks " \
                                                             "from " \
                                                             "source to the target column by only placing a " \
                                                             "smaller " \
                                                             "disk on a larger disk "
print("\n")
print("*" * (len(info) + 3))  # top border
print("* " + info + "*")  # content
print("*" * (len(info) + 3), "\n")  # bottom border

# Constants
ALPHA = 0.1  # learning rate
GAMMA = 0.9  # discount factor
REWARD = 100  # reward for solving the game
PUNISHMENT = -100  # punishment for not solving the game in the minimum number of steps
MIN_STEPS = 2 ** num_disks - 1  # minimum number of steps to solve the game


def get_possible_actions(state):
    """
    Return a list of possible actions for the given state of the game.
    An action is a tuple containing the source and target columns for a disk move.
    """
    actions = []

    if state.source:  # if there are disks in the source column
        # Add an action for moving the top disk from the source column to the auxiliary column
        actions.append((state.source, state.auxiliary))

        # Add an action for moving the top disk from the source column to the target column
        actions.append((state.source, state.target))

    if state.auxiliary:  # if there are disks in the auxiliary column
        # Add an action for moving the top disk from the auxiliary column to the source column
        actions.append((state.auxiliary, state.source))

        # Add an action for moving the top disk from the auxiliary column to the target column
        actions.append((state.auxiliary, state.target))

    return actions


class Agent:
    def __init__(self):
        self.q_values = {}  # a dictionary to store the Q-values for state-action pairs

    def choose_action(self, state):
        """
        Choose an action based on the current state of the game.
        """
        actions = get_possible_actions(state)
        if actions:  # check if there are any possible actions
            action = random.choice(actions)
        else:  # if there are no possible actions, return a default action
            action = (state.source, state.target)
        return action

    def get_q_value(self, state, action):
        """
        Get the Q-value for the given state-action pair.
        """
        key = StateAction(state, action)  # create a key using the state and action
        return self.q_values.get(key, 0)  # return 0 if the state-action pair is not in the dictionary

    def update_q_value(self, state, action, reward, next_state):
        """
        Update the Q-value for the given state-action pair based on the reward and the maximum Q-value of the next state.
        """
        key = StateAction(state, action)  # create a key using the state and action
        actions = get_possible_actions(next_state)
        if actions:  # check if there are any possible actions
            next_q_value = max([self.get_q_value(next_state, next_action) for next_action in actions])
        else:  # if there are no possible actions, set next_q_value to 0
            next_q_value = 0
        self.q_values[key] = self.get_q_value(state, action) + ALPHA * (
                    reward + GAMMA * next_q_value - self.get_q_value(state, action))


class State:
    def __init__(self, disks, source, auxiliary, target):
        self.disks = disks  # a list of integers representing the disks on each column, with the smallest disk being
        # at the top and the largest disk at the bottom
        self.source = source  # a list representing the disks on the source column
        self.auxiliary = auxiliary  # a list representing the disks on the auxiliary column
        self.target = target  # a list representing the disks on the target column


class StateAction:
    def __init__(self, state, action):
        self.state = state
        self.action = action


def solve_tower_of_hanoi(agent, num_disks):
    # Initialize the game with NUM_DISKS disks on the source column
    disks = list(range(num_disks, 0, -1))
    source = disks[::]  # make a copy of the disks list
    auxiliary = []
    target = []
    state = State(disks, source, auxiliary, target)
    steps = 0  # keep track of the number of steps taken to solve the game
    count = 0

    while state.target != sorted(state.disks, reverse=True) or count < 100000000:  #
        # while the disks are not in the correct order
        # Choose an action based on the current state of the game

        if len(state.disks) == len(state.target):
            if state.target == sorted(state.disks, reverse=True):

                print("GAME COMPLETED SUCCESSFULLY in: ", steps, "steps.")
                return

            else:
                print("GAME UNSUCCESSFUL")
                return

        count += 1
        action = agent.choose_action(state)

        # Check if the chosen action is a valid action
        if (action[0] == state.source and state.source) or (action[0] == state.auxiliary and state.auxiliary):
            # Update the state of the game based on the chosen action
            next_state = State(state.disks, state.source, state.auxiliary, state.target)
            disk = next_state.source.pop() if action[0] == state.source else next_state.auxiliary.pop()
            action[1].append(disk)
            steps += 1  # increase the number of steps taken
        else:
            # Choose a new action and update the state accordingly
            next_state = state

        # Calculate the reward for the chosen action
        if next_state.disks == sorted(next_state.disks, reverse=True):  # if the game is solved

            reward = REWARD if steps == MIN_STEPS else PUNISHMENT  # give a reward if the game is solved in the
            # minimum number of steps, otherwise give a punishment
        else:
            reward = 0  # no reward for intermediate steps

        # Update the Q-value for the state-action pair based on the reward
        agent.update_q_value(state, action, reward, next_state)

        state = next_state  # update the current state of the game

    return


def main():
    # Solve the Tower of Hanoi game using reinforcement learning
    agent = Agent()
    print("\nSolving the game using reinforcement learning:")
    solve_tower_of_hanoi(agent, num_disks)


if __name__ == "__main__":
    main()

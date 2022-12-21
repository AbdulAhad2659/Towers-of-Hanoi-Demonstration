import random

# Constants for the game
NUM_DISKS = 4  # number of disks in the game
REWARD = 1  # reward for completing the game in the minimum number of steps
PUNISHMENT = -1  # punishment for completing the game in more than the minimum number of steps

# The minimum number of steps required to solve the game with NUM_DISKS disks
# is calculated using the formula 2^n - 1, where n is the number of disks
MIN_STEPS = 2 ** NUM_DISKS - 1


# A class to represent the state of the game
class State:
    def __init__(self, disks, source, auxiliary, target):
        self.disks = disks  # a list of disks, with the smallest disk at the top
        self.source = source  # the source column
        self.auxiliary = auxiliary  # the auxiliary column
        self.target = target  # the target column

    def __eq__(self, other):
        return self.disks == other.disks and self.source == other.source and self.auxiliary == other.auxiliary and self.target == other.target

    def __hash__(self):
        return hash((tuple(self.disks), self.source, self.auxiliary, self.target))


# A class to represent the AI agent
class Agent:
    def __init__(self, alpha=0.1, epsilon=0.1):
        self.alpha = alpha  # learning rate
        self.epsilon = epsilon  # exploration rate
        self.q_values = {}  # a dictionary to store the Q-values for each state-action pair

    def choose_action(self, state):
        """
        Choose an action based on the current state of the game.
        With probability epsilon, choose a random action.
        Otherwise, choose the action with the highest Q-value.
        """
        if random.uniform(0, 1) < self.epsilon:
            # choose a random action
            action = random.choice(self.get_possible_actions(state))
        else:
            # choose the action with the highest Q-value
            q_values = [self.get_q_value(state, a) for a in self.get_possible_actions(state)]
            max_q = max(q_values)
            action = self.get_possible_actions(state)[q_values.index(max_q)]

        return action

    def get_possible_actions(self, state):
        """
        Get a list of possible actions given the current state of the game.
        A disk can only be moved if it is on top of the source or auxiliary columns.
        """
        actions = []
        if state.source and (not state.auxiliary or state.source[-1] < state.auxiliary[-1]):
            actions.append((state.source, state.auxiliary))
        if state.auxiliary and (not state.source or state.auxiliary[-1] < state.source[-1]):
            actions.append((state.auxiliary, state.source))
        if state.source and (not state.target or state.source[-1] < state.target[-1]):
            actions.append((state.source, state.target))
        if state.auxiliary and (not state.target or state.auxiliary[-1] < state.target[-1]):
            actions.append((state.auxiliary, state.target))
        if state.target and (not state.source or state.target[-1] < state.source[-1]):
            actions.append((state.target, state.source))
        if state.target and (not state.auxiliary or state.target[-1] < state.auxiliary[-1]):
            actions.append((state.target, state.auxiliary))

        return actions

    def get_q_value(self, state, action):
        """
        Get the Q-value for a given state-action pair.
        If the state-action pair has not been seen before, return 0.
        """
        if (state, action) in self.q_values:
            return self.q_values[(state, action)]
        else:
            return 0

    def update_q_value(self, state, action, reward, next_state):
        """
        Update the Q-value for a given state-action pair using the Q-learning formula.
        """
        q_value = self.get_q_value(state, action)
        next_q_values = [self.get_q_value(next_state, a) for a in self.get_possible_actions(next_state)]
        max_next_q = max(next_q_values)
        new_q_value = q_value + self.alpha * (reward + max_next_q - q_value)
        self.q_values[(state, action)] = new_q_value


def solve_tower_of_hanoi(agent):
    # Initialize the game with NUM_DISKS disks on the source column
    disks = list(range(NUM_DISKS, 0, -1))
    source = disks[::]  # make a copy of the disks list
    auxiliary = []
    target = []
    state = State(disks, source, auxiliary, target)
    steps = 0  # keep track of the number of steps taken to solve the game

    while state.disks != sorted(state.disks, reverse=True):  # while the disks are not in the correct order
        # Choose an action based on the current state of the game
        action = agent.choose_action(state)

        # Update the state of the game based on the chosen action
        next_state = State(state.disks, state.source, state.auxiliary, state.target)
        disk = next_state.source.pop() if action[0] == state.source else next_state.auxiliary.pop()
        action[1].append(disk)
        steps += 1  # increase the number of steps taken

        # Calculate the reward for the chosen action
        if next_state.disks == sorted(next_state.disks, reverse=True):  # if the game is solved
            reward = REWARD if steps == MIN_STEPS else PUNISHMENT  # give a reward if the game is solved in the
            # minimum number of steps, otherwise give a punishment
        else:
            reward = 0  # no reward for intermediate steps

        # Update the Q-value for the state-action pair based on the reward
        agent.update_q_value(state, action, reward, next_state)

        state = next_state  # update the current state of the game

    return steps


# Create an AI agent
agent = Agent()

# Solve the Tower of Hanoi game using reinforcement learning
steps = solve_tower_of_hanoi(agent)

print("Minimum number of steps to complete the game:", MIN_STEPS)
print("Number of steps taken to complete the game:", steps)

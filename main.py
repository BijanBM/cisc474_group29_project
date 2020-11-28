from random import random, choice
from copy import copy

from games import *

def learn(game, epsilon, alpha, episodes, use_q_learning):
    # the learn function learns the optimal policy for a game

    # epsilon is the probability of selecting an action other than the one with the highest expectation
    # alpha controls how much how quickly the value of an action is updated
    # episodes is the number of episodes that will be performed
    # use_q_learning is a boolean that specifies whether or to use sarsa or q-learning

    # algorithmically speaking we initialize q to 0
    # however for implementation purposes we do this in a lazy fashion
    # that is, we don't put entries into q until the appropriate state is reached
    # q is a dictionary that maps a state to a dictionary
    # the dictionary maps as a state to its expected reward
    q = {}
    for ep in range(episodes):
        # consider carefully how we initialize these next 4 variables
        # to initialize S and A, we put the values into S' and A',
        # and then copy them into S and A 
        S = None
        A = None
        S_prime = game.start_state()
        A_prime = None
        
        total_reward = 0
        is_terminal = False
        while True:
            # we take action A if it exists
            if A:
                (S_prime, reward, is_terminal) = game.take_action(S, A)
                total_reward += reward
                # we break if the terminal state is reached
                if is_terminal:
                    print(str(ep)+'\t'+str(total_reward))
                    q[S][A] += alpha*(reward-q[S][A])                    
                    break
            # we create an entry for S' if it doesn't have one already
            if S_prime not in q:
                q[S_prime] = {}
                for action in game.legal_actions(S_prime):
                    q[S_prime][action] = 0
            # now we'll pick the next action
            # we this by first seperating the best action from the rest and selecting accordingly
            candidates = copy(q[S_prime])
            best_action = max(candidates, key=candidates.get)
            del candidates[best_action]
            if random() < epsilon and len(candidates):
                A_prime = choice(list(candidates))
            else:
                A_prime = best_action
            # we update Q(S, A) if it exists
            # this is the only difference between q-learning and sarsa
            if S:
                if use_q_learning:
                    q[S][A] += alpha*(reward+q[S_prime][best_action]-q[S][A])
                else:
                    q[S][A] += alpha*(reward+q[S_prime][A_prime]-q[S][A])
            # we move S' and A' into S and A
            S = S_prime
            A = A_prime
            

if __name__ == '__main__':
    learn(TicTacToe, 0.01, 0.1, 10000, True)

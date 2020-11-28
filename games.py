from random import randint, choice

# this file specifies the games used and a common interface

class Game:
    # Game is the common interface both of the games will use
    # notice how an object of type Game does NOT store the state, only the game's rules
    def start_state():
        # returns the initial game state
        pass
    def legal_actions(state):
        # returns the set of legal actions from the current states
        pass
    def take_action(state, action):
        # applies the action
        # returns as a tuple the next state, the reward, and whether or not a terminal state was reached as a boolean
        pass

class TicTacToe(Game):
    def write_tuple_2d(grid, x, y, value):
        # because tuples are immutable, it can be difficult to change a single entry in a tuple
        # this function does that
        return grid[:x] + (grid[x][:y] + (value,) + grid[x][y+1:],) + grid[x+1:]

    def player_wins(grid, player):
        # this function checks if the specified player has won
        # the player variable will be either 'x' or 'o'
        # this loop checks at rows and columns
        for i in range(3):
            for j in range(3):
                if grid[i][j] != player:
                    break
            else:
                return True
            for j in range(3):
                if grid[j][i] != player:
                    break
            else:
                return True
        # then we check diagonals
        for i in range(3):
            if grid[i][i] != player:
                break
        else:
           return True
        for i in range(3):
            if grid[i][i] != player:
                break
        else:
            return True
        # if no wins are found, return False
        return False
         
    def start_state():
        # the agent is randomly assigned as either 'x', the starting player, or 'o', the second player
        # a state is a tuple containing 2 values, which side the agent is playing, and the board
        # the current turn is represent as either the string 'x' or 'o'
        # the board is represented as a 2d tuple of strings
        # those strings are 'x', 'o', or '.' where '.' is an empty space
        empty = (('.', '.', '.'), )*3
        if randint(0, 1) == 0:
            # this is the case where the agent goes first
            return ('x', empty)
        # this is the case where we apply an action before returning
        # otherwise a random move is played
        (x, y) = (randint(0, 2), randint(0, 2))
        return ('o', TicTacToe.write_tuple_2d(empty, x, y, 'x'))

    def legal_actions(state):
        actions = []
        for i in range(3):
            for j in range(3):
                if state[1][i][j] == '.':
                    actions.append((i, j))
        return actions

    def take_action(state, action):
        # first apply the player's action
    
        (player, grid) = state
        grid = TicTacToe.write_tuple_2d(grid, action[0], action[1], player)
        if TicTacToe.player_wins(grid, player):
            return ((player, grid), 1, True)
        
        # next generate a response
        other = 'x' if player == 'o' else 'o'
        responses = TicTacToe.legal_actions((other, grid))
        if not responses: # this means the game is a draw
            return ((player, grid), 0, True)
        response = choice(responses)
        grid = TicTacToe.write_tuple_2d(grid, response[0], response[1], other)
        if TicTacToe.player_wins(grid, other): # this means the player lost
            return ((player, grid), -1, True)
        # we check one more time if the game is a draw
        if not TicTacToe.legal_actions((player, grid)):
            return ((player, grid), 0, True)
        return ((player, grid), 0, False)

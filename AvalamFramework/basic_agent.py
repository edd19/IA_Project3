#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2015, <<<<<<<<<<< Ndizera Eddy, El Jilali Solaiman >>>>>>>>>>>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""

import avalam
import minimax

class Agent:
    """This is the skeleton of an agent to play the Avalam game."""

    def __init__(self, name="Agent"):
        self.name = name

    def successors(self, state):
        """The successors function must return (or yield) a list of
        pairs (a, s) in which a is the action played to reach the
        state s; s is the new state, i.e. a triplet (b, p, st) where
        b is the new board after the action a has been played,
        p is the player to play the next move and st is the next
        step number.
        """
        for action in state[0].get_actions():
            yield (action, (state[0].clone().play_action(action), state[1]*-1, state[2]+1))

    def cutoff(self, state, depth):
        """The cutoff function returns true if the alpha-beta/minimax
        search has to stop; false otherwise.
        """
        if state[0].is_finished():
            return True
        if depth > 1:
            return True
        return False

    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """
        score = state[0].get_score()
        if score > 0:
            return 1
        elif score < 0:
            return -1
        else:
            return 0

    def play(self, board, player, step, time_left):
        """This function is used to play a move according
        to the board, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        """
        self.time_left = time_left
        newBoard = avalam.Board(board.get_percepts(player==avalam.PLAYER2))
        state = (newBoard, player, step)
        return minimax.search(state, self)


if __name__ == "__main__":
    avalam.agent_main(Agent())

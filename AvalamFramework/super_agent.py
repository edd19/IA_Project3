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
import random

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
        ommited_actions = []
        has_ommited_all = True
        for action in state[0].get_actions():
            pair = (action, (state[0].clone().play_action(action), state[1]*-1, state[2]+1))
            if self.toPlay(state,pair[1], pair[0]):
                has_ommited_all = False
                yield pair
            else:
                ommited_actions.append(pair)
        if has_ommited_all:
            for pair in ommited_actions:
                yield pair


    def cutoff(self, state, depth):
        """The cutoff function returns true if the alpha-beta/minimax
        search has to stop; false otherwise.
        """
        max_depth = 1

        if state[0].is_finished():
            return True
        if depth >= max_depth:
            return True
        return False

    def evaluate(self, state):
        """The evaluate function must return an integer value
        representing the utility function of the board.
        """

        return state[0].get_evaluation()

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

    def toPlay(self, state1, state2, action):

        #Action that decrease our score
        delta_score = state2[0].get_players_score()[0] - state1[0].get_players_score()[0]
        if delta_score < 0 :
            if state1[0].m[action[0]][action[1]] > 0 and state1[0].m[action[2]][action[3]] > 0:
                if state1[0].get_tower_actions_bis(action[0], action[1]) == [action] and state1[0].get_tower_actions_bis(action[2], action[3]) == [(action[2], action[3], action[0], action[1])]:
                    return False
            elif state2[0].m[action[2]][action[3]]==5:
                return True
            return False

        #Action that create a complement to a an opponent neighbor tower
        actions = state2[0].get_tower_actions_bis(action[2],action[3])
        for a in actions:
            neighbor = (a[2], a[3])
            if abs(state2[0].m[neighbor[0]][neighbor[1]]) + abs(state2[0].m[action[2]][action[3]]) == 5:
                if state2[0].m[neighbor[0]][neighbor[1]] * state2[0].m[action[2]][action[3]] < 0:
                    return False

        #Action that create immovable tower fot the opponent
        if state2[0].m[action[2]][action[3]] < 0 and state2[0].get_tower_actions_bis(action[2],action[3]) == []:
            return False

        return True


if __name__ == "__main__":
    avalam.agent_main(Agent())

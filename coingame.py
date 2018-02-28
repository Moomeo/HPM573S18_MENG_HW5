import numpy as np
import scr.FigureSupport as Fig


class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin
        self._reward = 0

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        self._reward = 100*self._countWins - 250
        return self._reward


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored

        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

    def get_all_reward(self):
        return self._gameRewards

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def prob_lose(self):
        tlr = 0 # the times that you lose money
        for everyreward in self._gameRewards:
            if everyreward < 0:
                tlr += 1

        return tlr/len(self._gameRewards)



# run trail of 1000 games to calculate expected reward
games = SetOfGames(prob_head=0.5, n_games=1000)

# print all rewards
print('All reward:', games.get_all_reward())
# print the average reward
print('Expected reward when the probability of head is 0.5:', games.get_ave_reward())

#Problem 1:Draw the histogram of rewards in 1000 games with a fair coin
Fig.graph_histogram(
    observations=games.get_all_reward(),
    title='Histogram of Game Reward',
    x_label='Reward($)',
    y_label='Count')
# Answer for problem 1:
#the minimum and maximum reward that I expect to see is $-250 and $250

# Problem 2:Estimate the probability of losing money in this game
print('The probability of losing money in this game:',games.prob_lose())
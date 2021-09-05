#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 17:32:03 2018

This is a computer simulation of the Spelunking game James and I were
designing yesterday.

@author: matthewgentry
"""

import numpy as np
from matplotlib import pyplot as plt

class dice_pool(object):
    def __init__(self, n = 0):
        self.n = n
    def get_n(self):
        return self.n
    def add_dice(self, m):
        self.n += m
    def remove_dice(self, m):
        self.n += -m
        if self.n < 0:
            self.n = 0 
    def roll(self):
        a = np.random.randint(6, size=self.get_n())
        n_ones = np.where(a == 0, 1, 0).sum()
        if n_ones != 0:
            self.n += -n_ones
            return 'Failure'
        else:
            return 'Success'

class character(object):
    def __init__(self, n=6):
        self.n = n
    def get_n(self):
        return self.n
    def add_dice(self, m):
        self.n += m
    def remove_dice(self, m):
        self.n += -m
        if self.n < 0:
            self.n = 0 
    def roll(self, m):
        a = np.random.randint(6, size=m)
        n_successes = np.where(a >= 4 , 1, 0).sum()
        if n_successes != 0:
            return 'Success'
        else:
            return 'Failure'  
    def choice(self,difficulty, kind='random'):
        p_base = 1.0/3.0
        p_adjust = (float(difficulty)+float(self.get_n()))/12.0 - p_base
        if kind == 'random':
            p = [p_base]*3
        elif kind == 'choice':
            p1 = np.array([max(0, p_base-p_adjust), p_base, max(0,p_base+p_adjust)])
            p = p1/p1.sum()
            print(p)
        elif kind == 3:
            p = [0,0,1]
        elif kind == 2:
            p = [0,1,0]
        elif kind == 1:
            p = [1,0,0]
        return min(np.random.choice([1,2,3],p=p), self.n)
    
        
        
kinds = ['random', 'choice', 1, 2, 3]
games = []
for kind in kinds:
    conditions = np.random.choice([4,5,6], p = [0.5,0.3,0.2],size=50)
    players = []
    player_dice = []
    for i in range(4):
        players.append(character())
        player_dice.append([players[i].get_n()])
        
    DM_pool = dice_pool()
    game = []
    for condition in conditions:
        extra_conditions = 0
        players_out = 0
        for i, player in enumerate(players):
            player_dice[i].append(player.get_n())
            if players_out == 4:
                print('GAME OVER')
            if player.get_n() == 0:
                players_out +=1
                continue
            n_dice = player.choice(condition, kind=kind)
            outcome = player.roll(n_dice)
            game.append(outcome)
            if outcome == 'Success':
                break
            else:
                extra_conditions += 1
                player.remove_dice(n_dice)
                DM_pool.add_dice(n_dice)
                if DM_pool.roll() == 'Failure':
                    extra_conditions += 4
                    dice_return = DM_pool.get_n()
                    print(dice_return)
#                    while dice_return > 0:
#                        for player in players:
#                            if dice_return > 0:
#                                player.add_dice(1)
#                                dice_return += -1
#                            else:
#                                break
        conditions = np.concatenate((conditions, np.random.choice([4,5,6], p = [0.5,0.3,0.2],size=extra_conditions)))
    games.append(game)
    plt.figure(str(kind))        
    plt.hist(game)
    plt.figure()
    plt.title(str(kind))
    for i in player_dice:
        plt.plot(i)
plt.show()
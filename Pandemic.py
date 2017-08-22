# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 12:30:46 2017

@author: Wah Tran
"""

import pandas as pd
import networkx as nx
import numpy as np
from random import shuffle

path = 'C:/Users/Wah Tran/OneDrive/Documents/Python Scripts/Pandemic/'
city_links = 'pandemic_network.csv'
city_regions = 'pandemic_regions.csv'

world = pd.read_csv(path + city_links, index_col = 0)
region = pd.read_csv(path + city_regions, index_col = 0)


class city:
    def __init__(self, name, clr, conn):
        self.name = name
        self.clr = clr
        self.conn = conn
        self.virus = {'Black':0, 'Blue':0, 'Red':0, 'Yellow':0}
#        self.cb = sum(self.virus.values())

        self.outbrk_flg = 0
        self.outbrks = 0

        
    def infect(self, n = 1):
        gm.lose(self.clr)
        
        if self.virus[self.clr] + n > 3:
            self.outbreak(self.clr)

            for i in ct.keys():
                ct[i].outbrk_flg = 0            
        else:
            self.virus[self.clr] += n
            gm.virus[self.clr] += n
            print '{0:16} infected with {1} x {2}!\n'.format(self.name, self.clr, n)
#        self.cb = sum(self.virus.values())
        

    def outbreak(self, outbrk_clr):
        gm.lose(outbrk_clr)      
        
        if self.virus[outbrk_clr] + 1 > 3:
            if self.outbrk_flg == 0:
                print '{} OUTBREAK in {}!'.format(outbrk_clr, self.name)
                self.outbrk_flg = 1
                self.virus[outbrk_clr] = 3
                self.outbrks += 1
                gm.outbrks += 1
                
                
                if gm.outbreak_status() > 7:
                    gm.lose()
                    return
                    
                for link in self.conn:
                    if ct[link].outbrk_flg == 0:
                        print '\t{0:16} infected with {1}!'.format(link, outbrk_clr)
                        ct[link].outbreak(outbrk_clr)   

        else:
            self.virus[outbrk_clr] += 1
            gm.virus[outbrk_clr] += 1
    
    def treat(self, clr):
        if self.virus[clr] <= 0:
            print 'No {} virus in {}.\n'.format(clr, self.name)
        else:
            self.virus[clr] -= 1
            print '{0:16} treated for {1} x {2}!\n'.format(self.name, self.clr, 1)
                   

class gm:
    def __init__(self, world, region):
        self.world = world
        #self.region = region

        #self.virus = {'Black':0, 'Blue':0, 'Red':0, 'Yellow':0}
        #self.outbrks = 0
        #self.epidemics = 0
        self.players = 2
        self.difficulty = 5
        self.events = 5
        
        self.start_hand = {2:4, 3:3, 4:2}
        self.infect_track = [2,2,2,3,3,4,4]
        #self.infect_rate = self.infect_track[self.epidemics]
        
        #self.infect_deck = world.index.tolist(


        #self.epi_deck = round(self.player_deck/self.difficulty)


    def create_cities(self):
        ct = {}
        for i in world.index:
            x = np.array(world.loc[i])
            y = region.loc[i][0]
            c = world.columns.values[x == 1].tolist()
            ct[i] = city(i, y, c)
        return ct

    
    def start(self):
        self.turn = 0
        
        self.virus = {'Black':0, 'Blue':0, 'Red':0, 'Yellow':0}
        self.outbrks = 0
        self.epidemics = 0
        
        self.infect_rate = self.infect_track[self.epidemics]
        
        self.infect_discard = []
        self.infect_deck = world.index.tolist()
        shuffle(self.infect_deck)
        
        self.player_discard = []
        self.player_deck = world.index.tolist() + ['* EVENT *'] * self.events
        shuffle(self.player_deck)
        
        for i in range(self.players * self.start_hand[self.players]):
            self.draw('Player')
            
        self.p_epi = (self.difficulty - self.epidemics) / float(len(self.player_deck))

        n = len(self.player_deck)/self.difficulty
        m = len(self.player_deck)%self.difficulty
        l = self.player_deck
        self.player_deck = []

        fst = 0
        for i in range(m):
            lst = fst + n + 1
            
            pile = l[fst:lst] + ['** EPIDEMIC **']
            shuffle(pile)
            self.player_deck.extend(pile)
            
            fst = lst
            
        for i in range(self.difficulty - m):
            lst = fst + n
            
            pile = l[fst:lst] + ['** EPIDEMIC **']
            shuffle(pile)
            self.player_deck.extend(pile)
            
            fst = lst

        for i in ct.keys():
            x = ct[i].virus
            ct[i].virus = x.fromkeys(x, 0) 
            
            ct[i].outbrks = 0
        
        for i in range(3,0,-1):
            for j in range(0,3):
                self.infect(n = i)


    def play(self):
        print ''
        self.turn += 1
        print '\n* Turn {} *\n'.format(self.turn)
        
        for i in range(1,5):
            self.treat(i)
        
        print '------------------------------------------\n'
        
        for i in range(2):
            if not self.player_deck:
                self.lose('time')
            
            draw = self.draw('Player')
            if draw == '** EPIDEMIC **':
                self.epidemic()
                
            self.p_epi = (self.difficulty - self.epidemics) / float(len(self.player_deck))
            
        for i in range(self.infect_rate):
            self.infect()
            print ''
        
        print '------------------------------------------'


    def treat(self, action = 1):
        ct_treat_wt = {}

        for i in ct:
            cb_wt = 2
            prob_scl = np.random.uniform(1, 1.5)
            
            x = sum(v**cb_wt for v in ct[i].virus.values())
            ct_treat_wt[i] = float(x)/(x + prob_scl)
        
        for i in sorted(ct_treat_wt, key = ct_treat_wt.get, reverse=True):
        
            if np.random.binomial(1, ct_treat_wt[i]):
                
                for j in sorted(ct[i].virus, key = ct[i].virus.get, reverse=True):
        
                    vr_treat_wt = (float(ct[i].virus[j])/4 + 0)**action
                    
                    if np.random.binomial(1, vr_treat_wt, 1) and ct[i].virus[j] > 0:
                        ct[i].treat(j)
                        break                   
                break
            

    def draw(self, deck, epi = 0):
        if deck == 'Infect':
            draw = self.infect_deck[-epi]
            self.infect_deck.remove(draw)
            self.infect_discard.append(draw)
        elif deck == 'Player':
            
            
            draw = self.player_deck[0]
            self.player_deck.remove(draw)
            self.player_discard.append(draw)
        return draw

    
    def epidemic(self):      
        self.epidemics += 1
        self.infect_rate = self.infect_track[self.epidemics]

        print 'EPIDEMIC!!!'
        print 'Infection rate is now {}!\n'.format(self.infect_rate)
        
        self.infect(n = 3, epi = 1)        
        
        # TWO EPIDEMICS IN A ROW FAILS!!
        shuffle(self.infect_discard)
        self.infect_deck[:0] = self.infect_discard
        self.infect_discard = []
        
#        self.infect_deck.append(self.infect_discard)
#        self.infect_discard = []
#        self.epi_deck += round(self.player_deck/self.difficulty)

        print '\n------------------------------------------'


    def infect(self, n = 1, epi = 0):
        city = self.draw('Infect', epi)
        ct[city].infect(n)
        

    def lose(self, clr = 0):
        self.L = 0
        
        if not self.player_deck:
            self.L = 1
            print '\nLOSE: RAN OUT OF TIME'
            
        elif clr != 0 and gm.virus[clr] == 24:
            self.L = 1
            print '\nLOSE: TOO MANY {} INFECTIONS'.format(clr)
            
        elif self.outbrks > 7:
            self.L = 1
            print '\nLOSE: TOO MANY OUTBREAKS'
        
        if self.L:
            print 'LOSE FLAG HERE'
            quit
        
    def outbrk_reset(self):
        for i in ct.keys():
            ct[i].outbrk_flg = 0

        
    def virus_status(self, disp = False, clr = 'All'):
#        if not disp:
#            cnt = {'Black':0, 'Blue':0, 'Red':0, 'Yellow':0}
#            for i in world.index:
                
        
        if disp:
            n = 0
            if clr == 'All':
                for i in world.index:
                    n += sum(ct[i].virus.values())
                    if sum(ct[i].virus.values()) != 0:
                        print '{0:16} {1}'.format(i, ct[i].virus)
                
                if n == 0:
                    print 'No infections detected.'
                
            else:
                for i in world.index:
                    n += ct[i].virus[clr]
                    if ct[i].virus[clr] != 0:
                        print '{0:16} {1}'.format(i, ct[i].virus)
                
                if n == 0:
                    print 'No {} infections detected.'.format(clr)

                
    def outbreak_status(self):
        n = 0
        for i in world.index:
            n += ct[i].outbrks
        return n
        
    def peek(self):
        print 'Player:'
        print self.player_deck[0:2]
        print '\nInfect:'
        print self.infect_deck[0:self.infect_rate]


gm = gm(world, region)
ct = gm.create_cities()
gm.start()



        







# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 07:53:21 2019

@author: Mike
"""

import random
import sys

HAND_SIZE = 6
CARD_ORDINAL_NUMBERS = ['first','second','third','fourth','fifth','sixth']

class BaseGameException(BaseException): 
    
    pass

class ProgramExit(BaseGameException): 
    
    pass

class player():
    
    
    def __init__(self, id):
        self.id = id
        self.cards = []
    
    def add_card(self, card):
        if (card):
            self.cards.append(card)
            self.cards.sort()
        
    def play_card(self, card):
        self.cards.remove(card)
  
      
class game():
    
    
    
    def __init__(self, 
                 n_players, 
                 min_range = 2, 
                 max_range = 100, 
                 cards_per_turn = 2,
                 number_piles = 4):        
        self.deck = list(range(min_range,max_range))
        self.cpt = min(cards_per_turn,6)
        self.number_piles = number_piles
        
        random.shuffle(self.deck)
        
        self.players = {}
        for i in range(0, n_players):
            self.players[i] = player(i)
            
        self.setup_initial_hands()
        self.setup_piles()

    
    def setup_initial_hands(self):
        
        for i in range(0, 6):
            for player in self.players.values():
                card = self.deck.pop(0)
                player.add_card(card)
            

    
    def setup_piles(self):
        
        self.piles = [[1],[1],[100],[100]]

        print(self.pile_statement())
        
    
    def hand_statement(self, player):
        
        hand_statement = f'''
        ============================
        Player {player.id} Cards:
    
            {', '.join(map(str,player.cards))}

        ============================
        '''
        
        return hand_statement
        
    def pile_statement(self):
        
        pile_statement = f'''
            ================
            1: {self.piles[0][-1]} - Asc
            2: {self.piles[1][-1]} - Asc
                
            3: {self.piles[2][-1]} - Desc
            4: {self.piles[3][-1]} - Desc         
            ================
            '''
        return pile_statement
        
    
    def detailed_pile_statement(self):
        
        pile_state_end = f'''    
        ================================================
        '''


        statement = pile_state_end
        for pile_number, pile in enumerate(self.piles):
            
            pile_statement = f'''
            Pile {pile_number+1}:'''
            for chunk in range(0, len(pile), 10):
                pile_statement += f'''
                {pile[chunk:chunk+10]} \n'''
                
                
            
            statement += pile_statement
            
        statement += pile_state_end

        return statement
    
    
    def draw_card(self):
        
        if len(self.deck) > 0:
            return self.deck.pop(0)
        print('Deck is empty. Almost there!')

    
    def valid_play(self, card, pile):
        
        valid = False
        if pile <= 2: #ASCENDING
            curr_val = self.piles[pile - 1][-1]
            
            if (card > curr_val) or (card + 10 == curr_val):
                valid = True
            
        else: #DESCENDING
            curr_val = self.piles[pile - 1][-1]
            
            if (card < curr_val) or (card - 10 == curr_val):
                valid = True
        
        return valid;
    
    def play_card(self, player, card, pile):
        
        self.piles[pile - 1].append(card)
        player.play_card(card)
        
    def replenish_hand(self, player):
        
        while len(player.cards) < HAND_SIZE:
            #print(f'debug: hand size = {len(player.cards)}')
            player.add_card(self.draw_card())
    
    
    def _validate_input_entry(self,text):
        
        try:
            return int(text)
        except ValueError:
            print('You did not type a number so I decided to quit')
            print('This will be fixed in a later release')
            raise
    
    def no_moves(self, player):
                
        for card in player.cards:
            for pile_idx in range(self.number_piles):
                if self.valid_play(card, pile_idx + 1):
                    
                    return False
        
        
        return True
          
   
    def play_turn(self, player):
        
        print('deck length: {0}'.format(len(self.deck)))

        for play_index in range(self.cpt):
            
            print(self.hand_statement(player))
            print(self.pile_statement())
                        
            if self.no_moves(player):               
                self.game_lose()
                

            while True:#choose an available card       
                card_to_play = self._validate_input_entry(input(f'Enter card value to play {CARD_ORDINAL_NUMBERS[play_index]}: '))
                if card_to_play in player.cards:
                    break;
                else:
                    print('Play a card you own - {0} is not in your hand'.format(card_to_play))
                    
            while True:#choose a suitable pile
                pile_to_play = int(input('Enter pile to play card on: '))
                if pile_to_play <= self.number_piles:
                    if self.valid_play(card_to_play, pile_to_play):
                        break;
                        
                    else:
                        print('Try again, card cannot be played on this pile.')
                else:
                    print('Try again, pile not valid')
                    
            self.play_card(player, card_to_play, pile_to_play)
            
            
        self.replenish_hand(player)
        


    
    def win_condition(self):
        
        win = False
        
        if (len(self.deck) == 0):
            remaining_hands = [len(player.cards) for player in self.players.values()]
            
            if sum(remaining_hands) == 0:
                win = True
                
        return win
    
    
    def game_lose(self):
        
        print('You have no possible moves!')
        print('The final board values are:')
        self.game_end()
        
        print('You lose! Good day!')
        
        raise ProgramExit


    
    def game_win(self):
        
        print('You have won the game! The final board values are:')
        self.game_end()
        
        raise ProgramExit
    
    
    def game_end(self):
        
        print(self.pile_statement())
        print('Your piles look like this:')
        print(self.detailed_pile_statement())
    
    
    def play_game(self):
        
        self.game_running = True
        
        while self.game_running == True:
            
            for player in self.players.values():
                self.play_turn(player)
                if self.win_condition():
                    self.game_win()
                    self.game_running = False
                    break
                
                    

if __name__ == "__main__":
    try:
        current_game = game(2)
        current_game.play_game()
    except ProgramExit:
        print("Goodbye!")
                
    

#current_game = game(2)
#current_game.play_game()
#



## TODO: if deck < n_players * 6 - will crash at initial deck set up
## Loss conditions
## currently hardcoded number of piles - easier game at more piles
## exit if non integer - convert to if elif loop where else if 'x' break out of game completley


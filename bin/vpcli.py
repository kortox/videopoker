#!env python
from videopoker.jacksorbetter import JacksOrBetter, JackOrBetterHandSimpleStrategy
import re

class VideoPokerCLI:
    
    def __init__(self):
        self.game_options = {"Jacks or Better" : JacksOrBetter()}
        self.game = None
    
    def select_game_type(self):
        option_ids = {}
        count = 1
        for k in self.game_options.iterkeys():
            option_ids[count] = k
            count += 1
        options = [(k,v) for k,v in option_ids.iteritems()]
        options.sort()
        for option in options:
            print option[0], option[1]
        var = raw_input("Select a game id: ")
        # TODO validation
        self.game = self.game_options[option_ids[int(var)]]
    
    def show_player_hand(self, hand):
        best_hand = JackOrBetterHandSimpleStrategy(hand).best_hand()
        print " ".join([card.basic for card in hand]), " -> ", best_hand
    
    def deal_hand(self):
        hand = self.game.draw_hand()
        print "1  2  3  4  5"
        #     AH KH QH JH 0H
        self.show_player_hand(hand)
    
    def try_to_get_1_5_indexes(self):
        holds = str(input("Choose cards to hold: "))
        if not re.match("^[12345]{1,5}$", str(holds)):
            return None
        for i in range(1,6):
            if holds.count(str(i)) > 1:
                return None
        return [int(i) - 1 for i in holds]
            
    def take_and_apply_holds(self):
        indexes_to_hold = self.try_to_get_1_5_indexes()
        while not indexes_to_hold:
            indexes_to_hold = self.try_to_get_1_5_indexes(self)
        holds = [False, False, False, False, False]
        for i in indexes_to_hold:
            holds[i] = True
        hand = self.game.hold_cards(holds)
        self.show_player_hand(hand)

    def play_game(self):
        self.select_game_type()
        print ""
        while True:
            self.deal_hand()
            self.take_and_apply_holds()
            print ""
            raw_input()
        

if __name__ == "__main__":
    vpcli = VideoPokerCLI()
    vpcli.play_game()

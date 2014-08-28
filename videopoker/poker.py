import random
import sys

class Card:
    rank_value = {  'A' : 0,
                    '2' : 1,
                    '3' : 2,
                    '4' : 3,
                    '5' : 4,
                    '6' : 5,
                    '7' : 6,
                    '8' : 7,
                    '9' : 8,
                    '10': 9,
                    'J' : 10,
                    'Q' : 11,
                    'K' : 12,
                    }
    suit_value = {
                  'C' : 0,
                  'D' : 1,
                  'H' : 2,
                  'S' : 3,
                  }

    def __init__(self, rank, suit):
        self.rank = rank
        self.rank_ord = self.rank_value[self.rank]
        self.suit = suit
        self.suit_ord = self.suit_value[self.suit]
        self.basic = self.rank + self.suit
        if self.rank == '10':
            self.basic = '0' + self.suit

    def __str__(self):
        return str((self.rank, self.suit))

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return (self.rank_value[self.rank], self.suit) < (self.rank_value[other.rank], other.suit)

class Deck:
    def __init__(self):
        self.cards = []
        for suit in ['C', 'D', 'H', 'S']:
            for rank in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']:
                self.cards.append(Card(rank, suit))
        try:
            sys_rand = random.SystemRandom()
            self.randint = sys_rand.randint
        except:
            self.randint = random.randint

    def shuffle(self):
        for i in range(0, len(self.cards)):
            index = self.randint(i, len(self.cards) - 1)
            tmp = self.cards[i]
            self.cards[i] = self.cards[index]
            self.cards[index] = tmp

    def deal_hand(self, hand_size):
        return self.cards[:hand_size]

    def deal_hand_and_deck(self, hand_size):
        return (self.cards[:hand_size], self.cards[hand_size:])    

class HandCalculator:

    def __init__(self, hand, deck_tail=None):
        self.hand = hand[:]
        self.orig_hand = hand[:] # copy of hand to keep original indexing
        self.hand.sort()
        #                   A 2 3 4 5 6 7 8 9 0 J Q K
        self.rank_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.count_cards_by_rank()
        self.suit_counts = [0,0,0,0]
        self.count_cards_by_suit()

        
    def set_hand(self, hand):
        self.__init__(hand)

    def get_cards_to_hold(self):
        pass

    # functions for calculating value of a hand
    def count_cards_by_rank(self):
        for card in self.hand:
            self.rank_counts[card.rank_ord] += 1

    def count_cards_by_suit(self):
        for card in self.hand:
            self.suit_counts[card.suit_ord] += 1

    def is_pair(self):
        if self.rank_counts.count(2) == 1 and self.rank_counts.count(3) == 0:
            return 'pair'
        return None
    
    def is_two_pair(self):
        if self.rank_counts.count(2) == 2:
            return 'two_pair'
        return None
    
    def is_three_of_a_kind(self):
        if self.rank_counts.count(3) == 1 and self.rank_counts.count(1) == 2:
            return 'three_of_a_kind'
        return None
    
    def is_straight(self):
        max_ones = 0
        for i in range(0,len(self.rank_counts)+1):
            if self.rank_counts[i%len(self.rank_counts)] == 1:
                max_ones += 1
                if max_ones == 5:
                    return 'straight'
            else:
                max_ones = 0
        return None
        ##check for royal straight
        #if self.hand[0].rank == 'A' and self.hand[1].rank == '10' and self.hand[2].rank == 'J' and self.hand[3].rank == 'Q' and self.hand[4].rank == 'K':
        #    return 'straight'
        #for i in range(0, len(self.hand) - 1):
        #   if self.hand[i+1].rank_ord - self.hand[i].rank_ord != 1:
        #        return None
        #return 'straight'
    
    def is_flush(self):
        suit = self.hand[0].suit
        for card in self.hand[0:]:
            if suit != card.suit:
                return None
        return 'flush'
    
    def is_full_house(self):
        if self.rank_counts.count(3) == 1 and self.rank_counts.count(2) == 1:
            return 'full_house'
        return None
    
    def is_four_of_a_kind(self):
        if self.rank_counts.count(4) == 1:
                return 'four_of_a_kind'
        return None
    
    def is_straight_flush(self):
        straight = self.is_straight()
        flush = self.is_flush()
        if straight and flush:
            return 'straight_flush'
        else:
            return None
    
    def is_royal_flush(self):
        if self.is_flush() and self.is_straight():
            ranks = [card.rank for card in self.hand]
            for royal in ['10', 'J', 'Q', 'K', 'A']:
                if ranks.count(royal) != 1:
                    return None
            return 'royal_flush'
        else:
            return None
    
    def best_hand(self):
        funcs = [
                 self.is_royal_flush,
                 self.is_straight_flush,
                 self.is_flush,
                 self.is_straight,
                 self.is_full_house,
                 self.is_four_of_a_kind,
                 self.is_three_of_a_kind,
                 self.is_two_pair,
                 self.is_pair, # 50% match this
                 ]
        for func in funcs:
            hand_value = func()
            if hand_value != None:
                return hand_value
        return 'high_card'

def prob_test():
    d = Deck()
    stats = {
                'royal_flush' : 0,
                'straight_flush' : 0,
                'four_of_a_kind' : 0,
                'full_house' : 0,
                'flush' : 0,
                'straight' : 0,
                'three_of_a_kind' : 0,
                'two_pair' : 0,
                'pair' : 0,
                'high_card' : 0,
            }
    num_hands = 10000
    for i in range(0,num_hands):
        d.shuffle()
        (h,t) = d.deal_hand_and_deck(5)
        calc = HandCalculator(h, t)
        best = calc.best_hand()
        #print best, h
        stats[best] += 1
        
    for k,v in stats.iteritems():
        if k != None:
            print k, ' :: ', str(1.0 * v/num_hands * 100)

class VideoPoker:
    
    def __init__(self, buy_in=1500):
        self.deck = Deck()
        self.hand = []
        self.deck_tail = []
        self.credits = buy_in
    
    def draw_hand(self):
        self.deck.shuffle()
        (self.hand, self.deck_tail) = self.deck.deal_hand_and_deck(5)
        return self.hand
    
    # indicate which indexes w/ True/False
    def hold_cards(self, indexes_to_hold = [False,False,False,False,False] ):
        next_cards = self.deck_tail[:indexes_to_hold.count(False)]
        for i in range(0,len(self.hand)):
            if indexes_to_hold[i] == False:
                self.hand[i] = next_cards.pop() # technically not drawing in the "right" order but don't matter
        return self.hand

if __name__ == "__main__":
    hands = [
             [Card('A','C'),Card('J','H'),Card('10','C'),Card('K','D'),Card('Q','S'),], # A low straight
             [Card('2','C'),Card('A','S'),Card('5','D'),Card('4','D'),Card('3','S'),], # A high straight
             [Card('A','S'),Card('J','S'),Card('10','S'),Card('K','S'),Card('Q','S'),], # royal flush
             [Card('5','H'),Card('J','H'),Card('10','H'),Card('K','H'),Card('5','H'),], # flush
             [Card('3','S'),Card('3','S'),Card('3','C'),Card('Q','S'),Card('3','C'),], # quad
             [Card('5','S'),Card('K','S'),Card('5','S'),Card('5','S'),Card('K','D'),], # full house
             [Card('5','S'),Card('Q','S'),Card('5','D'),Card('5','S'),Card('K','S'),], # trips
             [Card('Q','D'),Card('A','C'),Card('5','S'),Card('5','S'),Card('A','S'),], # dub pair
             [Card('J','S'),Card('6','S'),Card('5','C'),Card('7','S'),Card('6','D'),], # pair
             [Card('2','S'),Card('K','S'),Card('5','C'),Card('4','S'),Card('10','S'),], # high
    ]
    answers = []
    for h in hands:
        calc = HandCalculator(h)
        answers.append(calc.best_hand())
        print answers[len(answers)-1], [card.basic for card in h]
    answer_count = {'straight' : 2,
        'royal_flush' : 1,
        'flush' : 1,
        'four_of_a_kind' : 1,
        'full_house' : 1,
        'three_of_a_kind' : 1,
        'two_pair' : 1,
        'pair' : 1,
        'high_card' : 1,
        }
    for answer,count in answer_count.iteritems():
        if answers.count(answer) != count:
            sys.stderr.write("Tests failed boo! : Expected " + str(count) + " " + answer)
            exit()
    print "Tests passed yay!"
    #d = Deck()
    #num_hands = 10000
    #for i in range(0,num_hands):
    #    d.shuffle()
    #    hand = d.deal_hand(5)
    #    calc = HandCalculator(hand, None)
    #    print calc.best_hand(), hand
        

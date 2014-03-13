from poker import Deck, HandCalculator, VideoPoker

class JackOrBetterHandSimpleStrategy(HandCalculator):

    def __init__(self, hand, deck_tail = None):
        HandCalculator.__init__(self, hand, deck_tail)

    def hold_four_of_a_kind(self):
        if self.is_four_of_a_kind():
            rank_ord = self.rank_counts.index(4)
            holds = []
            for c in self.orig_hand:
                if c.rank_ord == rank_ord:
                    holds.append(True)
                else:
                    holds.append(False)
            return holds
        else:
            return None

    def hold_four_for_royal_flush(self):
        # There is a flush option
        if self.suit_counts.count(4) == 1:
            # Set holds for royals in that suit
            suit_ord = self.suit_counts.index(4)
            holds = []
            for c in self.orig_hand:
                if c.suit_ord == suit_ord and ['10','J','Q','K','A'].count(c.rank) == 1:
                    holds.append(True)
                else:
                    holds.append(False)
            # Only return holds if there were sufficient royals
            if holds.count(True) == 4:
                return holds
            else:
                return None

    def hold_three_of_a_kind(self):
        # There is a three of a kind
        if self.rank_counts.count(3) == 1:
            rank_ord = self.rank_counts.index(3)
            holds = []
            for c in self.orig_hand:
                if rank_ord == c.rank_ord:
                    holds.append(True)
                else:
                    holds.append(False)
            return holds
        else:
            return None

    def get_cards_to_hold_simple(self):
        """
            1.) Four of a kind, straight flush, royal flush
            2.) 4 to a royal flush
            3.) Three of a kind, straight, flush, full house
            4.) 4 to a straight flush
            5.) Two pair
            6.) High pair
            7.) 3 to a royal flush
            8.) 4 to a flush
            9.) Low pair
            10.) 4 to an outside straight
            11.) 2 suited high cards
            12.) 3 to a straight flush
            13.) 2 unsuited high cards (if more than 2 then pick the lowest 2)
            14.) Suited 10/J, 10/Q, or 10/K
            15.) One high card
            16.) Discard everything
        """
        #TODO implement the above list
        hold_all = [True,True,True,True,True]
        # 1.) Four of a kind, straight flush, royal flush
        if self.is_straight_flush() or self.is_royal_flush():
            return hold_all
        elif self.is_four_of_a_kind():
            return self.hold_four_of_a_kind()
        # 2.) 4 to a royal flush
        hold = self.hold_four_for_royal_flush()
        if hold:
            return hold
        # 3.) Three of a kind, straight, flush, full house
        elif self.is_straight() or self.is_flush() or self.is_full_house():
            return hold_all
        # Note that we know that full house is already excluded so 
        hold = self.hold_three_of_a_kind()
        if hold:
            return hold
        #TODO finish this
            

class JacksOrBetter(VideoPoker):
    
    def __init__(self):
        VideoPoker.__init__(self)
        

if __name__ == "__main__":
    d = Deck()
    d.shuffle()
    jackscalc = JackOrBetterHandSimpleStrategy(d.deal_hand(5))
    print [card.basic for card in jackscalc.hand]
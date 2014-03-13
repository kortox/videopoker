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

    def four_for_royal_flush(self):
        # there is a flush option
        if self.suit_counts.count(4) == 1:
            # count how many royals of that suit
            suit_ord = self.suit_counts.index(4)
            royals_in_flush = 0
            for c in self.hand:
                if c.suit_ord == suit_ord and ['10','J','Q','K','A'].count(c.rank) == 1:
                    royals_in_flush += 1
            

    def get_cards_to_hold_simple(self):
        """
            Four of a kind, straight flush, royal flush
            4 to a royal flush
            Three of a kind, straight, flush, full house
            4 to a straight flush
            Two pair
            High pair
            3 to a royal flush
            4 to a flush
            Low pair
            4 to an outside straight
            2 suited high cards
            3 to a straight flush
            2 unsuited high cards (if more than 2 then pick the lowest 2)
            Suited 10/J, 10/Q, or 10/K
            One high card
            Discard everything
        """
        #TODO implement the above list
        hold_all = [True,True,True,True,True]
        #1.) Four of a kind, straight flush, royal flush
        if self.is_straight_flush() or self.is_royal_flush():
            return hold_all
        elif self.is_four_of_a_kind():
            return self.hold_four_of_a_kind()
        #2.) 4 to a royal flush
        elif self.four_for_royal_flush():
            return
            

class JacksOrBetter(VideoPoker):
    
    def __init__(self):
        VideoPoker.__init__(self)
        

if __name__ == "__main__":
    d = Deck()
    d.shuffle()
    jackscalc = JackOrBetterHandSimpleStrategy(d.deal_hand(5))
    print [card.basic for card in jackscalc.hand]
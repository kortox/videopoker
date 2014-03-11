from poker import Deck, HandCalculator

class JackOrBetterHandCalculator(HandCalculator):

    def __init__(self, hand, deck_tail = None):
        HandCalculator.__init__(self, hand, deck_tail)

    def get_cards_to_hold(self):
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
        pass

if __name__ == "__main__":
    d = Deck()
    d.shuffle()
    jackscalc = JackOrBetterHandCalculator(d.deal_hand(5))
    print [card.basic for card in jackscalc.hand]
from random import shuffle

SUITS = ["clubs","hearts","diamonds","spades"]
RANKS = ["ace","two","three","four","five","six","seven","eight","nine","queen","jack","king"]


class Deck:
    def __init__ (self):
        self.cards = []
        self.newDeck()

    
    def dealNumCards(self,n):
        return [self.cards.pop(0) for _ in range(n)]
    
    def newDeck(self):
        self.cards.clear()
        self.cards = [(rank,suit) for rank in RANKS for suit in SUITS]
        shuffle(self.cards)

        
class Player:
    def __init__(self):
        self.hand = None

    def rankHand(self, board = False):

        allCards = list(self.hand)

        if board:
            allCards += list(board)

        ranks = [card[0] for card in allCards]
        suits = [card[1] for card in allCards]
        rank_counts = {rank: ranks.count(rank) for rank in ranks}
        
        pairs = [rank for rank, count in rank_counts.items() if count == 2]
        three_of_a_kind = [rank for rank, count in rank_counts.items() if count == 3]
        four_of_a_kind = [rank for rank, count in rank_counts.items() if count == 4]

        isFlush = (len(set(suits)) == 1 and len(allCards >= 5))




baralho = Deck()

tulio = Player()
tulio.hand = baralho.dealNumCards(2)
turn = baralho.dealNumCards(3)

tulio.rankHand([turn + baralho.dealNumCards(1)])

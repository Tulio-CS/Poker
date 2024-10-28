from random import shuffle
from copy import deepcopy




SUITS = ["clubs","hearts","diamonds","spades"]
SUITS_ICONS = {"clubs":"♣","hearts":"♥","diamonds":"♦","spades":"♠"}
RANKS = ["two","three","four","five","six","seven","eight","nine","ten","jack","queen","king","ace"]
RANKS_VALUES = {"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"jack":11,"queen":12,"king":13,"ace":14}


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

    def evalHand(self, board=[]):
        allCards = list(self.hand)
        highCard = max([RANKS_VALUES[card[0]] for card in self.hand])
        if board:
            allCards += board

        ranks = sorted([RANKS_VALUES[card[0]] for card in allCards], reverse=True)
        suits = [card[1] for card in allCards]
        rank_counts = {rank: ranks.count(rank) for rank in ranks}
        
        pairs = [rank for rank, count in rank_counts.items() if count == 2]
        three_of_a_kind = [rank for rank, count in rank_counts.items() if count == 3]
        four_of_a_kind = [rank for rank, count in rank_counts.items() if count == 4]

        suit_counts = {suit: suits.count(suit) for suit in SUITS}
        flush_suit = next((suit for suit, count in suit_counts.items() if count >= 5), None)
        isFlush = flush_suit is not None

        unique_ranks = sorted(set(ranks), reverse=True)
        isStraight = False
        straight_high_card = None

        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i + 4] == 4:
                isStraight = True
                straight_high_card = unique_ranks[i]
                break

        if set([14, 2, 3, 4, 5]).issubset(unique_ranks):
            isStraight = True
            straight_high_card = 5

        handValue = 0
        if len(pairs) == 1:
            handValue = 1
        if len(pairs) == 2:
            handValue = 2
        if len(three_of_a_kind) > 0:
            handValue = 3
        if isStraight:
            handValue = 4
        if isFlush:
            handValue = 5
        if len(three_of_a_kind) > 0 and len(pairs) > 0:
            handValue = 6
        if len(four_of_a_kind) > 0:
            handValue = 7 
        if isStraight and isFlush:
            if straight_high_card == 14:
                handValue = 9  
            else:
                handValue = 8 

        return (handValue, highCard)


class Poker:
    def __init__ (self,numPlayers):
        self.players = [Player() for _ in range(numPlayers)]
        self.deck = Deck()
        self.turn = None
        self.river = None

    def drawCards(self,player,deck):
        player.hand = deck.dealNumCards(2)
    
    def drawTurn(self,deck):
        self.turn = deck.dealNumCards(3)

    def drawRiver(self,deck):
        self.river = deck.dealNumCards(2)

    def checkWinner(self,turn = [],river = []):
        handEval = [player.evalHand(turn+river) for player in self.players]
        handValue = [hand[0] for hand in handEval]
        highCards = [hand[1] for hand in handEval]
        maxHandValue = max(handValue)
        if handValue.count(maxHandValue) == 1:
            return handValue.index(maxHandValue)
        else:
            maxRankValue = max(handValue)
            return handValue.index(maxRankValue)
        
    def game(self):
        self.deck.newDeck()
        for player in self.players:
            self.drawCards(player,self.deck)
        self.drawTurn(self.deck)
        self.drawRiver(self.deck)
        return self.checkWinner(self.turn,self.river)
    
    def monteCarlo(self,numIterations):
        self.drawCards(self.players[0],self.deck)
        print(self.players[0].hand)
        winCount = 0
        for _ in range(numIterations):
            deck = deepcopy(self.deck)
            shuffle(deck.cards)
            for player in self.players[1:]:
                self.drawCards(player,deck)
            self.drawTurn(deck)
            self.drawRiver(deck)
            if self.checkWinner(self.turn,self.river) == 0:
                winCount += 1
        return winCount/numIterations


jogo = Poker(6)
print(jogo.monteCarlo(10000))


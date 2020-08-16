'''

Planning out some features, for a generalised card system which could be used with a variety of different preprogrammed rulesets

CARD CLASS

    ATTRIBUTES - SUIT, RANK, VALUE, FACING

    METHODS - FLIP, ROTATE? other things maybe

DECK CLASS
    
    ATTRIBUTES - SIZE ? use dunder methods maybe

    METHODS - SHUFFLE, SPLIT, DEAL/DRAW(use .pop[0] to get from "top"), ADD(use append[-1] to add one to bottom; .extend to add multiple)

HAND CLASS??? Maybe not necessary, could just fold into player class

    ATTRIBUTES - SIZE, 

    METHODS - PLAY, DISCARD, SHUFFLE, REVEAL

PLAYER CLASS

    ATTTRIBUTES - NAME, TEAM?(Canasta and some other card games have teams), SCORE

    METHODS - EXAMINE

PILE CLASS?

    ATTRIBUTES - 

BOARD/TABLE CLASS?

    ATTRIBUTES - ZONES, PILES,

    METHODS - 

TOKEN CLASS?? For betting games?

    ATTRIBUTES - COLOUR, VALUE

    METHOD - WAGER/BET

'''
#For now just assign attributes/methods that are necessary for blackjack, add others later
from random import shuffle

class Card():

    def __init__(self, suit, rank):                 #initialises card attributes and sets card to automatically be created "face up" and to draw their value from a dictionary called card_values (set in each games rulesets)

        self.suit = suit
        self.rank = rank
        self.face = True
        self.value = card_values[self.rank]

    def __str__(self):
        if self.face == True:
            return f"{self.rank} of {self.suit}"
        else:
            return "This card is face down"

    def flip(self):
        self.face = not self.face

class Deck():

    def __init__(self):

        self._cards = []

    def __str__(self):

        for cards in self._cards:
            print(cards)
        return "These are the cards in the deck."

    def __len__(self):
        return len(self._cards)

    def __getitem__(self,card_num):
        return self._cards[card_num]

    def add(self, card):        #adds card to the bottom of the deck
        self._cards.append(card)

    def shuffle(self):          #shuffles the deck obviously
        shuffle(self._cards)

    def deal(self):             #removes a card from the top of the deck and returns it for other methods to take in
        return self._cards.pop(0)

class Participants():           # Just a base class for the dealer and player classes to inherit from

    def __init__(self):

        self.hand = []
        self.score = 0
        self.name = ""

    def __str__(self):

        return f"{self.name} has a score of {self.score}"

    def draw(self, deck):        #adds card to hand from a deck

        self.hand.append(deck.deal())

    def show(self):

        print(f"{self.name} has the following cards: {', '.join(str(card) for card in self.hand)}")

    def score_check(self):      # A method to refresh the score attribute
        total = 0
        for cards in self.hand:
            total += cards.value
        return total

class Dealer(Participants):

    def __init__(self):

        Participants.__init__(self)
        self.name = "Dealer"

class Player(Participants):

    def __init__(self):

        Participants.__init__(self)
        self.name = input("Please input your name :")

def std_deck():         # Function generates a new deck instance with 52 cards (no jokers) compatible for most card games
    newdeck = Deck()
    suits = ["Hearts","Diamonds","Clubs","Spades"]
    ranks = ["Ace","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King"]
    for suit in suits:
        for rank in ranks:
            newdeck.add(Card(suit,rank))
    return newdeck


''' make rulesets classes?
class Blackjack():

    def __init__(self, )
'''

#Blackjack ruleset initialisation, all games should have their own initialisation to define the card values
#Maybe all rulesets should define board layout in case of graphicalisation later

def player_update(players):         # a function used to refresh the players score after drawing and show the new hand, making sure to hide the dealers score if used for the dealer
    if players == dealer:
        players.score = players.score_check()
        players.show()
    else:
        player_list[players].score = player_list[players].score_check()
        print(player_list[players])
        player_list[players].show()

def ace_check(players):             # a function to count how many aces are in hand for the purposes of score readjustment when going over 21 
    count = 0
    for cards in player_list[players].hand:
        if cards.rank == "Ace":
            count += 1
    return count

card_values = {"Ace":11,"Two":2,"Three":3,"Four":4,"Five":5,"Six":6,"Seven":7,"Eight":8,"Nine":9,"Ten":10,"Jack":10,"Queen":10,"King":10}   #used to provide values for each card, will be different for different games which is why this isn't an attribute
new_deck = std_deck()                   #creates a new instance of the Deck class
new_deck.shuffle()                      #then shuffles it
dealer = Dealer()
player_list = {}                        #dictionary used to contain the player classes and their keys

for nums in range(1,(int(input("How many players will be playing against the dealer?: ")))+1):              #asking for input for how many players will be playing the game

    player_list["Player"+f"{nums}"] = Player()                                                              #adds the requested number of players to the dictionary

for players in player_list:

    for _ in range(2): player_list[players].draw(new_deck)                                                  #adds two cards to every players hand from the deck

for _ in range(2): dealer.draw(new_deck)                                                                    #adds two cards to the dealers hand

dealer.hand[0].flip()                                                                                       #flips the first card in the dealers hand so it can't be seen when viewing the dealers hand
player_update(dealer)                                                                                       #updates the dealer's score and prints out the second card in their hand

for players in player_list:

    player_update(players)                                                                                  #updates the player's score and shows their hand

    while player_list[players].score < 21:                                                                  #core gameplay loop, checking whether or not the player's score is over 21

        action = input(f"{player_list[players].name}, what would you like to do hit or stick?: ")           #asks player to choose an action, hit or stick

        if action == "hit":                                                                                 #draws card then updates player score and shows hand
            player_list[players].draw(new_deck)
            player_update(players)

        elif action == "stick":                                                                             #exits loop to move to next player
            break

        if player_list[players].score > 21 and ace_check(players) != 0:                                     #this is used to handle players who have gone over 21 with aces in hand, in order to reduce their score by turning ace into 1

            for nums in range(0,ace_check(players)):                                                        #checks how many aces there are and reduces score by 10 for each ace but only until score is 21 or lower, so as not to unnecessarily reduce ace values
                player_list[players].score -= 10
                if player_list[players].score < 22:
                    break

            print(player_list[players])                                                                     #shows player score
            player_list[players].show()                                                                     #and their hand

    if player_list[players].score > 21:                                                                     #announces the end of the players round by saying whether they stuck or went bust
        print(f"{player_list[players].name} has gone bust!")
    else:
        print(f"{player_list[players].name} is sticking with {player_list[players].score}.")

print("Now the dealer will take their turn.")                                                               #starting dealer turn by revealing second card and showing hand
dealer.hand[0].flip()
dealer.show()

while dealer.score < 17:                                                                                    #dealer plays by standard casino rules, drawing until at 17 or above

    dealer.draw(new_deck)                                                                                   #same as with player loop, draws card and updates score
    print("The dealer is drawing another card.")
    player_update(dealer)

if dealer.score > 21:                                                                                       #announces end of dealers turn by saying whether they went bust or stuck
    print("The dealer has gone bust!")

else:
    print(f"The dealer is sticking with a score of {dealer.score}.")

for players in player_list:                                                                                 #final win condition check

    if player_list[players].score > 21:                                                                                                         #first checks if player has gone bust
        print(f"{player_list[players].name} went bust with {player_list[players].score}. Better luck next time.")

    else:
        if dealer.score > 21:                                                                                                                   #then checks if dealer has gone bust
            print(f"{player_list[players].name} won by default with {player_list[players].score} because the dealer went bust. Lucky break.")
        else:                                                                                                                                   #then checks who has higher, lower or equal score, and prints message accordingly
            if player_list[players].score > dealer.score:                                                                       
                print(f"{player_list[players].name} beat the dealer's {dealer.score} with a score of {player_list[players].score}. Congratulations!")
            elif player_list[players].score == dealer.score:
                print(f"{player_list[players].name} drew with the dealer at {dealer.score}. Nobody wins.")
            else:
                print(f"{player_list[players].name} lost to the dealer's {dealer.score} with a score of {player_list[players].score}. The house always wins.")





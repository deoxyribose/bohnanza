import numpy as np

nplayers = 4

deck_description = {
'Coffee': ((24),  (4 ,  7,   10,  12)),
'Wax': ((22),  (4 ,  7,   9,   11)),
'Blue': ((20),  (4 ,  6,   8,   10)),
'Chili': ((18), ( 3,   6,   8,   9)),
'Stink':  ((16), ( 3,   5,   7,   8)),
'Green': ((14), ( 3,   5,   6,   7)),
'Soy':   ((12), ( 2,   4,   6,   7)),
'Black-eyed': ((10), ( 2,   4,   5,   6)),
'Red':  ((8),  ( 2,   3,   4,   5)),
'Garden': ((6),  ( 0,   2,   3,   0)),
'Cocoa': ((4),  ( 0,   2,   3,   4)),
}

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.gold = 0
        self.farms = [[],[]]
        self.hand = self.get_hand(deck)
        self.tf = [True,False]

    def buy_third_farm(self):
        if self.gold >= 3 and len(self.farms) == 2:
            self.farms.append([])
        else:
            raise RuntimeError('You either have a farm already, or cannot afford one!')

    def get_hand(self,deck):
        hand = []
        for card in xrange(5):
            hand.append(deck.pop())
        return hand

    def plant(self,card):
        #pdb.set_trace()
        relevant_or_empty_farm = [farm for farm in self.farms if not farm or farm[-1] == card]
        if relevant_or_empty_farm:
            relevant_or_empty_farm[0].append(card)
        else:
            farm_harvested_yet = False
            while not farm_harvested_yet:
                farm_to_harvest = np.random.random_integers(0,len(self.farms)-1)
                if len(self.farms[farm_to_harvest]) > 1:
                    self.harvest(farm_to_harvest)
                    farm_harvested_yet = True
            self.farms[farm_to_harvest].append(card)

    def harvest(self,farmnr):
            nbeans = len(self.farms[farmnr])
            beanspecs = deck_description[self.farms[farmnr][-1]][1]
            #pdb.set_trace()
            bean_harvest = max([nbeans_required if nbeans_required<nbeans else -1 for nbeans_required in beanspecs]) +1
            if bean_harvest > 0:
                self.gold += beanspecs.index(bean_harvest)
            self.farms[farmnr] = []

    def offer(self,player,trading_area): 
    # chooses random cards in trading_area to demand
    # chooses random cards in hand to offer
    # returns (cards_to_buy,cards_to_sell,self)
        np.random.shuffle(self.tf)
        buying = []
        selling = []
        for card in trading_area:
            if self.tf[0]:
                buying.append(card)
            np.random.shuffle(self.tf)
        for card in self.hand:
            if self.tf[0]:
                selling.append(card)
            np.random.shuffle(self.tf)
        return (buying,selling,self)

    def select_offer(self,offers):
        # pick one randomly
        youre_the_one_that_i_want = np.random.random_integers(0,len(offers)-1) # you and not another one - ...ooh! ..ooh! ..ooh!
        return youre_the_one_that_i_want

    def wishes_to_plant_again(self):
        np.random.shuffle(self.tf)
        return self.tf[0]

    def accept_donation(self,card,trading_area):
        np.random.shuffle(self.tf)
        if self.tf[0]:
            self.plant(card)
            return trading_area
        else:
            trading_area.append(card)
            return trading_area



deck = [bean for (bean,(amount,dummy)) in deck_description.items() for i in xrange(amount)]
np.random.shuffle(deck)

Alex = Player('Alex', deck)
Bere = Player('Bere', deck)
Domi = Player('Domi', deck)
players = [Alex,Bere,Domi]

def turn(player,deck):
    print player.hand
    player.plant(player.hand.pop())
    if player.wishes_to_plant_again():
        player.plant(player.hand.pop())
    print player.farms
    trading_area = []
    trading_area.append(deck.pop())
    trading_area.append(deck.pop())
    #pdb.set_trace()
    while trading_area: # first other players present offers in turn, then player decides what to do
        print trading_area
        offers = []
        for other_player in players:
            if other_player != player:
                offers.append(other_player.offer(player,trading_area))
        print offers
        chosen_action = np.random.random_integers(0,len(offers)+1)
        print chosen_action
        if chosen_action == 0:
            player.plant(trading_area.pop())
        elif chosen_action == 1:
            donated_card = trading_area.pop()
            for other_player in players:
                if other_player != player:
                    trading_area = other_player.accept_donation(donated_card,trading_area)
        else:
            (bought,sold,buyer) = offers[player.select_offer(offers)]
            print "%s buys  %s for %s" %(buyer.name, ', '.join(bought), ', '.join(sold))
            for card in bought:
                trading_area.remove(card)
            for card in sold:
                player.plant(card)
        #pdb.set_trace()
    # draw three cards
    for i in xrange(3):
        player.hand = [deck.pop()] + player.hand
    print player.hand
    print player.farms
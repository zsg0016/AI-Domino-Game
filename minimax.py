import domino
from math import *
all_tiles = []


def set_up(a):
    all_tiles = a


def get_hand(hand,tiles_on_field,center_tiles): #find tiles in hand
    at = all_tiles
    ct = center_tiles
    tf = tiles_on_field
    if len(hand) == 0:
        hand = set(all_tiles) - set(center_tiles + tiles_on_field)
        return hand
    new_hand = set(all_tiles) - set(center_tiles + hand + tiles_on_field)
    return new_hand

def points(hand): #count points won
    points = 0
    for i in hand:
        points += i.bottomval
        points += i.topval
    return points

def get_playable(hand): #get playable tiles
    doubles = []
    regs = []
    for i in hand:
        if i.bottomval == i.topval:
            doubles.append(i)
        else:
            regs.append(i)
    if len(doubles):
        return doubles
    return regs

def minimax(game_state, hand, player, tiles_on_field, center_tiles, tile = None): #minimax function for decision making
    if tile: #place tile in game_state
        if tile.bottomval == game_state[-1].openval:
            t = domino.place_t(tile.topval,0,0)
            game_state.insert(0,t)
         
        elif tile.bottomval == game_state[0].openval:
            t = domino.place_t(tile.topval,0,0)
            game_state.append(t)
          
        elif tile.topval == game_state[-1].openval:
            t = domino.place_t(tile.bottomval,0,0)
            game_state.insert(0,t)
           
        elif tile.topval == game_state[0].openval:
            t = domino.place_t(tile.bottomval,0,0)
            game_state.append(t)
          
        tiles_on_field.append(tile)
    if len(hand) == 0: #winning state
        if player == 'O': #if player
            _hand = get_hand(hand,tiles_on_field,center_tiles)
            return -1 * points(_hand)
        else: #if AI
            _hand = get_hand(hand,tiles_on_field,center_tiles)
            return points(_hand)
    
    hand2 = [] #playable tiles
    for i in hand: 
        if i.bottomval == game_state[-1].openval:
            hand2.append(i)
        elif i.bottomval == game_state[0].openval:
            hand2.append(i)
        elif i.topval == game_state[-1].openval:
            hand2.append(i)
        elif i.topval == game_state[0].openval:
            hand2.append(i)
    if len(hand2) == 0: #no playable tiles
        if player == 'O':
            return -1 * (len(hand) + 1)
        else:
            return (len(hand) + 1)
    play = get_playable(hand2)
    if player == 'o': #player is opponent
        minimum = +inf
        for p in play:
            new_hand = get_hand(hand,tiles_on_field,center_tiles)
            mini = minimax(game_state, new_hand, 'a', tiles_on_field, center_tiles, p)
            minimum = min(mini, minimum)
        return minimum
    else: #player is AI
        maximum = -inf
        for p in play:
            new_hand = get_hand(hand,tiles_on_field,center_tiles)
            maxi = minimax(game_state, new_hand, 'o', tiles_on_field, center_tiles, p)
            maximum = max(maxi, maximum)
        return maximum
    
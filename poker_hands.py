""" 
This module contains the functions to search each player's hands to determine if any matches can be found.
find_straights() is called within find_matches() to check for card continuity before moving on to the more common matches found within the
find_matches() function
"""

royal_flush_set = {"Ace", 10, "Jack", "Queen", "King"}

def find_straights(ranks, unique_suits):
    """
    ranks: a list of the 5 ranks defined from each card's rank in the player's hand
    unique_suits: a list of all unique suits from the player's hand. Used to determine if player has a Straight Flush
    return: just like it's parent function find_matches() it will return a tuple: The name of the hand, an internal point value,
    and the highest card rank. If find_straights() fails it will only return "No Straight"
    """
    high_card_rank = ranks[4]

     # Check for straight continuity within the ranks by checking if user has an Ace (a 14).

    if ranks[4] == 14: 
    #Since the ace can be low OR high, we must check if the first values are 2 to 5, or 10 to King (10 to 13)
        low_ace_straight = ranks[0] == 2 and ranks[1] == 3 and ranks[2] == 4 and ranks[3] == 5
        high_ace_straight = ranks[0] == 10 and ranks[1] == 11 and ranks[2] == 12 and ranks[3] == 13
        if (low_ace_straight or high_ace_straight) and unique_suits == 1: #if hand has both a straight AND only one suit 
            return ("Straight Flush", 120, high_card_rank)
        elif low_ace_straight or high_ace_straight:
            return ("Straight", 60, high_card_rank)
        else:
            return "No Straight" # return from function to move on to find_matches()
    else:
        testNum = ranks[0] + 1 # will check for continuity based of the first rank 
        for i in range(1,5):
            if ranks[i] is not testNum: # if the next rank doesn't equal the testNum, there's no straight
                return "No Straight"
            testNum += 1 # increment to check for next card
        return ("Straight", 60, high_card_rank)

def find_matches(hand):
    """ 
    return: A tuple that contains the winning hand, if any, a score attributed to each hand, and
    the highest card value to help break ties if hands match. 
    Function includes a function call to find_straights() that will check if there's continuity
    within the hand before moving on to any other winning hands. 
    """
    values = []
    ranks = []
    for card in hand:
        values.append(card.value)
        ranks.append(card.rank)
    ranks.sort() # sort ranks to check for increasing values
    high_card_rank = ranks[4] # assign the largest rank to high_card_rank
    unique_values = []
    duplicate_values = []
    unique_suits = []

    for card in hand:
        if card.suit not in unique_suits:
            unique_suits.append(card.suit)
        if card.value not in unique_values:
            unique_values.append(card.value)
        else:
            duplicate_values.append(card.value)

    """Check for single suit matches first, (Royal Flush and Flush)"""

    if len(unique_values) == 5: # if there's five individual values...
        """Check for flushes"""
        if len(unique_suits) == 1:
            if set(unique_values) == royal_flush_set: # if all values match royal_flush_set
                return ("Royal Flush", 135, high_card_rank)
            else:
                return ("Flush", 75, high_card_rank) # all cards match suit

    """Check for Straights"""
    
    straight_result = find_straights(ranks, unique_suits)
    if straight_result != "No Straight": # if the hand revealed a straight, no need to check for other hands.
        return straight_result

    else:   
        """Check if there are any other matches"""
        if len(unique_values) == 4: # Check for two of a kind (four unique numbers, plus one duplicate)
            return ("One Pair", 15, high_card_rank)

        elif len(unique_values) == 3: # Check for three of a kind, or two pair
            if duplicate_values[0] == duplicate_values[1]: 
                return ("Three of a Kind", 45, high_card_rank)
            else:
                return ("Two Pair", 30, high_card_rank) # both duplicate_values are different e.g (3,4,4,6,6)

        elif len(unique_values) == 2: # Check for full house or four of a kind
            if duplicate_values[0] == duplicate_values[1] == duplicate_values[2]: # if the three duplicate_values are the same
                return ("Four of a kind", 105, high_card_rank) # two unique numbers, plus three duplicate_values
            else:
                return ("Full House", 90) # one pair and three duplicate_values
        return ("No Matches", 0, high_card_rank) # return matches and ranks to compute high card

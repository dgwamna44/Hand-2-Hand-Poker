"""
Program: hand2handpoker.py
Author: Duroje Gwamna
Date Last Modified: 12/9/2021

This Program will allow users to play shuffled poker hands against the dealer. Each hand dealt is analyzed to determine strength
through the poker_hands module, and a winner is announced at the end of each round. Users can decide to play another round or to resign
altogether. All the game data from each user's session is shown under the Stats page, including a win/loss record. At the very end, the user 
is prompted to enter his/her information that will be added into a database through the poker_database module.

For new players, the welcome page has a list of hands that can be accessed that shows all the valid poker hands as a jpeg.

"""

import tkinter
from tkinter import *
from tkinter import messagebox
from os import write
from PIL import ImageTk, Image
import datetime, time
import random, winsound
from poker_hands import find_matches
from poker_database import *


def rank_to_face_card(rank):
    cards = {
        11: "Jack",
        12: "Queen",
        13: "King",
        14: "Ace"
    }
    return cards.get(rank)

def face_card_to_rank(face_card):
    cards = {
        "Jack": 11,
        "Queen": 12,
        "King": 13,
        "Ace": 14,
    }
    return cards.get(face_card)

class Card:
    """initialize by card value, suit, and an image file"""
    def __init__(self, value, suit, image_path):
        self.value = value
        self.suit = suit
        self.image_path = image_path
        if type(self.value) != int:
            self.rank = face_card_to_rank(self.value)
        else:
            self.rank = self.value

class Deck:
    """will generate a new deck of Card objects by iterating through 13 values for each of the """
    def __init__(self):  
        self.cards = []
        suit_names = ['club', 'diamond', 'heart', 'spade']
        values = [2,3,4,5,6,7,8,9,10,'Jack','Queen','King','Ace']
        for suit in suit_names:
            for value in values:
                file_name = "cards\\" + str(suit)+"_"+str(value) + ".png" 
                c = Card(value, suit, file_name) # create card object
                self.cards.append(c) # append to cards

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()
    
    def return_cards(self, hand): # collect cards from player and reshuffle the deck
        self.cards.append(hand)
        self.shuffle()


def increment(placement): #increments placement of next card
    x = placement[0] + 200
    y = placement[1] 
    return [x,y]


def initialize():
    board.pack()
    start.place(x=600,y=100)
    resign.place(x=100,y=700)
    player_high_card_label.place(x=50, y=300)
    player_high_card.place(x=50, y=375)
    dealer_high_card_label.place(x=1300, y=300)
    dealer_high_card.place(x=1300, y=375)
    player_result.place(x=350, y=475)
    dealer_result.place(x=850, y=475)
    game_result.place(x=1000, y=100)
    root.withdraw()
    start_time = datetime.datetime.now()
    times.append(start_time)
    start_game()

def deal_cards(card_placement, board, deck, hand, card_images):
    """
    card_placement: a mutable list of coordinates
    board: Tkinter canvas object
    deck: Deck object used to draw cards
    hand: list of five Card objects
    card_images: list of PhotoImage objects for rendering to board
    """
    for i in range(5):
        hand.append(deck.deal()) # adds card object from dealer's deck to player
        card_image = ImageTk.PhotoImage(file=hand[i].image_path) # convert to photoImage. 
        card_images.append(card_image)
        board.create_image(card_placement, anchor=SW, image=card_images[i]) # add images to canvas
        card_placement = increment(card_placement) #increment placement for next card
        winsound.PlaySound(card_sound, winsound.SND_ASYNC) # plays card_sound
        board.update()
        time.sleep(.4)
 

def start_game():
    """Clear board and all tkinter objects"""
    game_window.deiconify()
    board.delete("all") 
    player_hand = []
    dealer_hand = []
    card_images = []
    dealer_images = []
    player_score = 0
    dealer_score = 0
    player_high_card.config(text = "")
    dealer_high_card.config(text = "")
    player_result.config(text = "", bg="white")
    dealer_result.config(text = "", bg="white")
    game_result.config(text = "")
    new_deck = Deck()
    new_deck.shuffle()
    start["state"] = DISABLED
    resign["state"] = DISABLED
    
    winsound.PlaySound(start_new_game, winsound.SND_ASYNC)
    board.update()
    time.sleep(.75)

    """ Player's turn """

    deal_cards(card_placement, board, new_deck, player_hand, card_images)
    player_matches = find_matches(player_hand) # assign tuple to player_matches (result, player_hand score, and high card)
    player_high_card_rank = player_matches[2] # high_card_rank is 3rd item of tuple
    if player_high_card_rank > 10: # if card is a face_card or an ace, then convert face card value to string
        player_high_card_string = rank_to_face_card(player_high_card_rank) #high_card_string equals the highest value in string form
    else:
        player_high_card_string = str(player_high_card_rank) # convert number to string
    player_result_text = player_matches[0]
    hand_score = player_matches[1] 
    player_score = hand_score + player_high_card_rank # combine high_card_rank value to hand_score
    if player_score >= 45:
        winsound.PlaySound(great_hand, winsound.SND_ASYNC)
    elif player_score < 45 and player_score >= 15:
        winsound.PlaySound(ok_hand, winsound.SND_ASYNC)
    player_result.config(text=player_result_text)
    player_high_card.config(text=player_high_card_string)
    board.update()
    time.sleep(1) # slight break to show result

    """ Computer's turn """

    deal_cards(dealer_card_placement, board, new_deck, dealer_hand, dealer_images)
    dealer_matches = find_matches(dealer_hand) # assign tuple to player_matches (result, hand score, and high card)
    dealer_high_card_rank = dealer_matches[2] # high_card_rank is 3rd item of tuple
    if dealer_high_card_rank > 10: # if card is a face_card or an ace, then convert face card value to string
        dealer_high_card_string = rank_to_face_card(dealer_high_card_rank) #high_card_string equals the highest value in string form
    else:
        dealer_high_card_string = str(dealer_high_card_rank) # convert number to string
    dealer_result_text = dealer_matches[0]
    hand_score = dealer_matches[1] 
    dealer_score = hand_score + dealer_high_card_rank # combine dealer_high_card_rank value to hand_score
    dealer_result.config(text=dealer_result_text)
    dealer_high_card.config(text=dealer_high_card_string)
    board.update()
    time.sleep(.5)

    """find winner by accessing the second item from player_matches and dealer_matches"""

    if player_score > dealer_score:
        win_loss_record[0] += 1 # increment wins
        game_result_text="You win!"
        player_result.config(bg="yellow")
        color = "blue"
        sound = you_win
    elif player_score < dealer_score:
        win_loss_record[1] += 1 # increment losses
        game_result_text="Dealer wins..."
        color = "red"
        dealer_result.config(bg="yellow")
        sound = dealer_wins
    else:
        """Will result in a draw game if both player and dealer have the same matches AND high card"""
        win_loss_record[2] += 1 # increment draws
        game_result_text = "Draw Game"
        color = "black"
        sound = draw_game

    round_data = [player_result_text, player_high_card_string, dealer_result_text, dealer_high_card_string, game_result_text, 
    win_loss_record[0], win_loss_record[1], win_loss_record[2]]
    session_data.append(round_data)  
    game_result.config(text=game_result_text, fg=color)
    start["state"] = NORMAL # activate start/resign buttons once round is over
    resign["state"] = NORMAL
    winsound.PlaySound(sound, winsound.SND_ASYNC) # play appropriate result sound
    root.mainloop()

def resign():
    """Collects the player's name, and includes the win/loss information. Will only collect data and quit if user provides a name"""

    def format_time(delta, fmt):
        """
        delta: datetime.timedelta() object
        fmt: parameter to format string
        collects time difference that's a timedelta object, and returns the formatted string"""
        d = {"days": delta.days}
        d["hours"], rem = divmod(delta.seconds, 3600)
        d["minutes"], d["seconds"] = divmod(rem, 60)
        return fmt.format(**d)

    def submit():
        if fname.get() == "":
            messagebox.showwarning("First Name required", "Please Enter a First Name")
        elif lname.get() == "":
            messagebox.showwarning("Last Name required", "Please Enter a Last Name")
        else:
            first_name = fname.get() 
            last_name = lname.get()
            for data in session_data:
                add_game(conn, first_name, last_name, data[5], data[6], data[7])
            write_to_file(first_name, last_name, session_data)
               
    def write_to_file(first_name, last_name, session_data):
        try:
            f=open(str(first_name) + "'s_poker_session.txt", 'w')
            f.writelines(str(first_name) + " " + str(last_name))
            f.write("\n")
            f.write("\n")
            for data in session_data:
                f.writelines(first_name +"'s Hand: " + data[0])
                f.write("\n")
                f.writelines(first_name + "'s High Card: " + data[1])
                f.write("\n")
                f.writelines("Dealer's Hand: " + data[2])
                f.write("\n")
                f.writelines("Dealer's High Card: " + data[3])
                f.write("\n")
                f.writelines("Result: " + data[4])
                f.write("\n")
                f.write("\n")
            f.writelines("Total Games: ")
            f.writelines(str(len(session_data)))
            f.write("\n")
            f.writelines("Win Loss Record: " + "W" +str(win_loss_record[0]) + " - L" + str(win_loss_record[1]) + " - D" + str(win_loss_record[2]))
        except IOError:
            messagebox.showerror("File Error", "Unable to create file")

        finally:
            f.close() # close file
            root.destroy() # close program 

    def stats():
        """ Will tabulate each hand the player produced during the session."""

        def done():
            stats_window.withdraw() # Closes stats window
            post_game_window.deiconify() #opens post game window
        """ Pop up an error if there's no first or last name"""
        if fname.get() == "":
            messagebox.showwarning("First Name required", "Please Enter a First Name")
        elif lname.get() == "":
            messagebox.showwarning("Last Name required", "Please Enter a Last Name")
        else:
            first_name = fname.get() 
            last_name = lname.get()
            """creates a list of hands to match against the player's results"""
            hands = ["No Matches", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush",
        "Full House", "Four of a Kind", "Straight Flush", "Royal Flush" ]
            post_game_window.withdraw()
            stats_window = Toplevel(root)
            title = first_name + "'s Game Stats"
            stats_window.title(title)
            stats_window.geometry("500x700")
            players_results = []
            for round in session_data:
                """Append the first index of each round's data to player's results, then iterate through the 
                hands list to match each result to the list """
                players_results.append(round[0])
            for i in range(len(hands)):
                num_hands = players_results.count(hands[i]) # each hand will have its respective number of hands displayed (hand_label)
                hand_label = Label(stats_window, text=hands[i] + ": " + str(num_hands), anchor=W, font=game_font)
                hand_label.grid(row=i)
            record_text = "W" +str(win_loss_record[0]) + " - L" + str(win_loss_record[1]) + " - D" + str(win_loss_record[2])
            win_percentage = 100 * (win_loss_record[0]/(win_loss_record[0]+win_loss_record[1]+win_loss_record[2]))
            if win_percentage > 50:
                win_color = "green"
            else:
                win_color = "black"
            record = Label(stats_window, text=record_text, font=game_font) # prints record in W-L-D form
            record.grid(row=10)
            record_2 = Label(stats_window, text="Win percentage: " + 
                    str("%.2f" % win_percentage) + "%", font=game_font, fg=win_color ) 
            record_2.grid(row=11)
            Button(stats_window, text="OK", font=game_font, bg="green", command=done).place(x=350, y=300)
            time_label = Label(stats_window, text="Total Playing Time: " + playing_time, font=game_font)
            time_label.grid(row=12)

    end_time = datetime.datetime.now()
    times.append(end_time)
    time_delta = times[1] - times[0] # get difference between starting and ending times.
    playing_time = format_time(time_delta, "{hours:02d}:{minutes:02d}:{seconds:02d}") # format times to hh:mm:ss
    game_window.withdraw() # close game_window
    post_game_window = Toplevel(root) # open post_window 
    post_game_window.title("Thanks for playing!")
    post_game_window.geometry("800x300")
    winsound.PlaySound(thanks_for_playing, winsound.SND_ASYNC)
    Label(post_game_window, text="Thank you for playing Hand 2 Hand Poker! \n Please enter your full name to be added to our database.", font=game_font).pack()
    Label(post_game_window, text = "First Name").pack()
    fname = Entry(post_game_window, width=30)
    fname.pack()
    Label(post_game_window,text = "Last Name").pack()
    lname = Entry(post_game_window, width=30)
    lname.pack()
    stats = tkinter.Button(post_game_window, text="See Stats", bg="yellow", command=stats, font=game_font)
    stats.place(x=180, y=200)
    submit = tkinter.Button(post_game_window, text="Submit Data", bg="skyblue", command=submit, font=game_font)
    submit.place(x=450, y=200)

def list_of_hands():
    """ Shows a list of all winning hands starting at the top from Royal Flush 
        image from https://www.wsop.com/poker-hands/ """

    def back_to_game():
        hand_list.withdraw()
        root.deiconify()

    root.withdraw()
    hand_list = Toplevel(root)
    hand_list.title("List of Hands")
    hand_list.geometry("1000x1000")
    frame = Frame(hand_list, width=1000, height=1000)
    frame.pack()
    btn = Button(hand_list, text="Back to Title", bg="yellow", font=game_font, command=back_to_game)
    btn.place(x=700, y=500)
    load = Image.open("list_of_hands.jpg")
    render = ImageTk.PhotoImage(load)
    image = Label(hand_list, image=render)
    image.image = render
    image.place(x=0, y=0)

if __name__ == "__main__":
    card_placement = [275, 450] # players hand coordinates
    dealer_card_placement = [275, 800] # dealers coordinates
    session_data = []
    times = []
    win_loss_record = [0,0,0]

    db = "hand2handpoker.db"
    conn = create_connection(db)
    create_table(conn, db)

    game_font = ("Segoe Print",20)
    result_font = ("Segoe Print", 36)
    high_card_font = ("Segoe Print", 24)
    
    card_sound = 'card_sound.wav'
    you_win = 'you_win.wav'
    dealer_wins = 'you_lose.wav'
    draw_game = "draw.wav"
    ok_hand = "ok_hand.wav"
    great_hand = "great_hand.wav"
    start_new_game = "start_new_game.wav"
    thanks_for_playing = "thanks_for_playing.wav"

    """ Create tkinter objects"""

    root = Tk()        
    root.title("Welcome")
    logo = Toplevel(root)
    logo.geometry("700x500")
    root.withdraw()
    root.geometry("400x300")

    load = Image.open("logo.png")
    render = ImageTk.PhotoImage(load)
    image = Label(logo, image=render)
    image.image = render
    image.place(x=0, y=0)
    
    root.withdraw()
    logo.deiconify()
    logo.update()
    time.sleep(1)
    logo.withdraw()
    root.deiconify()

    initialize_and_start = Button(root, text="Start Game!", bg="green", font=game_font, command=initialize)
    initialize_and_start.place(x=100, y=50)
    list_of_hands = Button(root, text="List Of Hands", bg="red", font=game_font, command=list_of_hands)
    list_of_hands.place(x=90, y=150)

    game_window = Toplevel(root)
    game_window.withdraw()
    board = tkinter.Canvas(game_window, width=1600, height=900, bg="white")
    start = Button(board, text="Start Another Round", command=start_game, bg="skyblue", font=game_font)
    resign = Button(board, text="Resign", command=resign, bg="lightgreen", font=game_font)
    player_high_card_label = Label(board, text="High Card:", font=high_card_font)
    player_high_card = Label(board, text="", font=high_card_font)
    dealer_high_card_label = Label(board, text="High Card:", font=high_card_font)
    dealer_high_card = Label(board, text="", font=high_card_font)
    player_result = Label(board, text="", font=game_font)
    dealer_result = Label(board, text="", font=game_font)
    game_result = Label(board, text="", font=result_font)
    root.mainloop()
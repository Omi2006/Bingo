import sys
import termcolor
import copy
import random
import math
import os
import time

INITIAL = [[], [], [], []]

class Card():

    def __init__(self, words, initial, x, y, name):
        self.words = words
        self.name = name
        self.board = copy.deepcopy(initial)
        self.x = x
        self.y = y
        index = 0
        for i in range(self.x):
            for j in range(self.y):
                self.board[i].append(self.words[index])
                index += 1
    
    def make_move(self, word):
        """
        Given a word, mark it as X in the board and remove from the word list
        """
        index = self.get_index(word)
        self.words.remove(word)
        self.board[index[0]][index[1]] = "X"
    
    def get_index(self, word):
        """
        Get the index of a word in the 2d board
        """
        for i, x in enumerate(self.board):
            if word in x:
                return (i, x.index(word))
    
    def print_board(self):
        """
        Print the board in a bingo fasion
        """
        for word_group in self.board:
            print(("+" + "- " * self.y) * self.x + "+")
            print("|", end="")
            
            for word in word_group:
                print(" " * math.floor((self.y - len(word)/2)), end="")
                print(word, end="")
                print(" " * math.floor((self.y - len(word)/2)), end="")
                print("|", end="")
            print()
        
        print(("+" + "- " * self.y) * self.x + "+")
        print()


    def won(self):
        "Determine if a player has won by counting the X's in their board"
        for row in self.board:
            if row.count("X") != self.x:
                return False

        return True
        
class Bingo():
    def __init__(self, player_count, word_file):
        self.player_count = player_count
        self.cards = []
        self.players = []
        all_player_words = []

        #Declare the words
        with open(os.path.join(word_file)) as f:
            self.words = f.read().splitlines()
        
        #Make a deepcopy of the words to distribute among players
        words = copy.deepcopy(self.words)
        #Iterate through the player count and ask for their name while defining a new word list
        for i in range(int(self.player_count)):

            player_name = input(f"Player {i+1} name: ")
            self.players.append(player_name)
            player_words = random.sample(words, 16)
            if "" in player_words:
                index = player_words.index("")
                player_words[index] = "X"
            all_player_words.append(player_words)
            words = [x for x in words if x not in player_words]
        
        #Have a player choose a list of words and assign it to them
        for player in self.players:
            print()

            for i, card in enumerate(all_player_words):
                print(f"Words {i + 1}: {card}")
                print()
            
            try:
                player_number = input(f"{player} choose your word list from the previous words: ")
            except:
                sys.exit("You must choose a number in the word list.")

            player_card = all_player_words[int(player_number) - 1]
            all_player_words.pop(int(player_number) - 1)

            self.cards.append(Card(player_card, INITIAL, 4, 4, player))
        
        print()
        print("Thses are the cards: ")
        print()

        #Display all the cards
        for card in self.cards:
            print(f"{card.name} has the following card: ")
            card.print_board()
    
    def play_turn(self):
        """
        Play a turn of bingo by choosing a word, marking the user who has it, check if someone has won and displaying the boards again
        """
        #Choose a random word and print it to the terminal
        word = random.choice(self.words)
        termcolor.cprint(f"The word is {word}", "blue")
        print()
        #Flag to determine if someone had the word
        appears = False

        for card in self.cards:

            if word in card.words:
                appears = True
                #Make the move for the player who has the word
                card.make_move(word)
                #Congratulate the player who won
                if card.won():
                    termcolor.cprint(f"The winner is {card.name} with the following board:", "green")
                    card.print_board()
                    self.cards.remove(card)

                else:
                    print(f"Player {card.name} had the word {word} in his card.")

                break

        if not appears:
            print(f"Nobody had the word {word}")
        
        #Show all player boards
        print("The players have the following cards:")
        self.print_stats()
        print()

        self.words.remove(word)
    
    def print_stats(self):
        """
        Print to terminal all the player cards
        """
        for card in self.cards:
            print(f"Player {card.name} has this card:")
            card.print_board()
            print()

def main():
    #Check for correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python bingo.py word_directory")

    #Extract the words
    word_file = sys.argv[1]
    player_count = input("Welcome to Bingo! How many people will play? ")
    #define the bingo game
    Game = Bingo(player_count, word_file)
    "Alright, time to start!"
    time.sleep(0.5)
    #Keep playing with pauses in between turns until someone wins
    while len(Game.cards) == int(player_count):
        Game.play_turn()
        time.sleep(3.5)

if __name__ == "__main__":
    main()
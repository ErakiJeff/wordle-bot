from enum import Enum
from wordlist_helper import get_word_list
from random import randrange

def get_random_word():
    index = randrange(0, len(WordleGame.word_list))
    return WordleGame.word_list[index]
    

def score_word(guess, acutal):
    returned_info = [GuessFeedback.GRAY] * len(acutal)
    word_copy = list(acutal)
    for i in range(len(guess)):
        if guess[i] == word_copy[i]:
            returned_info[i] = GuessFeedback.GREEN
            word_copy[i] = None
    for i in range(len(guess)):
        if returned_info[i] != GuessFeedback.GREEN and guess[i] in word_copy:
            yellow_letter_index = word_copy.index(guess[i])
            returned_info[i] = GuessFeedback.YELLOW
            word_copy[yellow_letter_index] = None
    return returned_info

class GuessFeedback(Enum):
    GRAY = 1
    YELLOW = 2
    GREEN = 3


class Player:
    def make_guess(self, board_info):
        pass


class HumanPlayer(Player):
    def make_guess(self, board_info):
        print(WordleGame.prettify_board(board_info))
        guess = input("Please enter your guess: ")
        return guess


class KevinsPogAI(Player):
    def __init__(self):
        self.available_words = WordleGame.word_list[:]
        self.guessed_words = []
    
    def make_guess(self, board_info):
        if board_info == []:
            self.guessed_words.append('crane')
            return 'crane'
        last_guess = self.guessed_words[-1]
        last_guess_results = list(zip(last_guess, board_info[-1]))
        new_word_list = []
        #breakpoint()
        for word in self.available_words:
            valid_word = True
            comparison_results = list(zip(word, score_word(word, last_guess)))
            for index, (letter, response) in enumerate(last_guess_results):
                if valid_word == False:
                    break
                if response == GuessFeedback.GREEN:
                    if comparison_results[index] != (letter, response):
                        valid_word = False
                    else:
                        comparison_results[index] = None
            for letter, response in last_guess_results:
                if valid_word == False:
                    break
                match response:
                    case GuessFeedback.YELLOW:
                        other_tuple_index = None
                        try:
                            other_tuple_index = comparison_results.index((letter, response))
                        except ValueError:
                            valid_word = False
                            break
                        comparison_results[other_tuple_index] = None
                    case GuessFeedback.GRAY:
                        if letter in [x[0] for x in comparison_results if x != None]:
                            valid_word = False
            if valid_word:
                new_word_list.append(word)
        #breakpoint()

        self.available_words = new_word_list[1:]
        self.guessed_words.append(new_word_list[0])
        return new_word_list[0]
        


class Kevins2BraincellAI(Player):
    def make_guess(self, board_info):
        return "hello"


class WordleGame:
    word_list = get_word_list()
    def __init__(self, word, player=HumanPlayer(), max_guesses=6):
        self.word = word.lower()
        self.player = player
        self.guesses = []
        self.board = []
        self.max_guesses = max_guesses

    def game_loop(self):
        while not self.is_game_over():
            guess = self.get_guess()
            self.guesses.append(guess)
            scored_word = self.score_word(guess)
            self.board.append(scored_word)
            if scored_word == [GuessFeedback.GREEN] * 5:
                return guess, self.guesses
        return self.word, self.guesses

    def get_guess(self):
        guess = self.player.make_guess(self.board)
        while not self.is_valid_guess(guess):
            print('invalid guess')
            guess = self.player.make_guess(self.board)
        return guess.lower()


    def score_word(self, guess):
        return score_word(guess, self.word)


    def is_game_over(self):
        return len(self.guesses) >= self.max_guesses

    def is_valid_guess(self, guess):
        if guess not in WordleGame.word_list or len(guess) != len(self.word) or any(char.isdigit() for char in guess):
            return False
        return True

    @staticmethod
    def prettify_board(board):
        pretty_board = []
        for row in board:
            pretty_row = ""
            for color in row:
                representation = ""
                match color:
                    case GuessFeedback.GREEN:
                        representation = "G"
                    case GuessFeedback.YELLOW:
                        representation = "y"
                    case GuessFeedback.GRAY:
                        representation = "g"
                pretty_row = pretty_row + representation
            pretty_board.append(pretty_row)
        return pretty_board


def playWordle():
    #word = "motto"
    word = get_random_word()
    #player = Kevins2BraincellAI()
    #player = HumanPlayer()
    player = KevinsPogAI()
    game = WordleGame(word=word, player=player)
    return game.game_loop()


def tests():
    bemma_game = WordleGame(word="bemma")
    assert bemma_game.score_word("mmmmm") == [
        GuessFeedback.GRAY,
        GuessFeedback.GRAY,
        GuessFeedback.GREEN,
        GuessFeedback.GREEN,
        GuessFeedback.GRAY,
    ]
    mmmmm_game = WordleGame(word="mmmmm")
    assert mmmmm_game.score_word("bemma") == [
        GuessFeedback.GRAY,
        GuessFeedback.GRAY,
        GuessFeedback.GREEN,
        GuessFeedback.GREEN,
        GuessFeedback.GRAY,
    ]
    stomp_game = WordleGame(word="stomp")
    assert stomp_game.score_word("early") == [
        GuessFeedback.GRAY,
        GuessFeedback.GRAY,
        GuessFeedback.GRAY,
        GuessFeedback.GRAY,
        GuessFeedback.GRAY,
    ]
    #breakpoint()
    assert stomp_game.score_word("stops") == [
        GuessFeedback.GREEN,
        GuessFeedback.GREEN,
        GuessFeedback.GREEN,
        GuessFeedback.YELLOW,
        GuessFeedback.GRAY,
    ]
    assert stomp_game.score_word("stock") == [
        GuessFeedback.GREEN,
        GuessFeedback.GREEN,
        GuessFeedback.GREEN,
        GuessFeedback.GRAY,
        GuessFeedback.GRAY,
    ]
    assert stomp_game.score_word("stout") == [
        GuessFeedback.GREEN,
        GuessFeedback.GREEN,
        GuessFeedback.GREEN,
        GuessFeedback.GRAY,
        GuessFeedback.GRAY,
    ]
    assert stomp_game.score_word("stoop") == [
        GuessFeedback.GREEN,
        GuessFeedback.GREEN,
        GuessFeedback.GREEN,
        GuessFeedback.GRAY,
        GuessFeedback.GREEN,
    ]
    assert stomp_game.score_word("stowp") == [
        GuessFeedback.GREEN,
        GuessFeedback.GREEN,
        GuessFeedback.GREEN,
        GuessFeedback.GRAY,
        GuessFeedback.GREEN,
    ]
    assert score_word('books', 'motto') == [
        GuessFeedback.GRAY,
        GuessFeedback.GREEN,
        GuessFeedback.YELLOW,
        GuessFeedback.GRAY,
        GuessFeedback.GRAY,
    ]

def test_wordle():
    wins = 0
    total_guesses = 0
    for i in range(1000):
        word, guesses = playWordle()
        total_guesses += len(guesses)
        print(word, guesses)
        if word == guesses[-1]:
            wins += 1
    print(f'Win %: {float(wins) / 1000}')
    print(f'Average guesse: {float(total_guesses) / 1000}')

if __name__ == "__main__":
    tests()
    test_wordle()
    #print(playWordle())

import pathlib
from enum import Enum
from collections import Counter
from random import choice
import re
from xmlrpc.client import Boolean

from unidecode import unidecode

class Result(Enum):
    FAIL = 0,
    OK_LETTER = 1,
    OK = 2

class Game:
    def __init__(self, word : str):
        self.__word = word
        self.__guesses_results = []

    def __iter__(self):
        for game in self.__guesses_results:
            yield(game)
    
    @staticmethod
    def eval_position(guess : str, word : str) -> list[Result]:
        result = [
                Result.OK if cur_letter == correct_letter else Result.FAIL 
            for cur_letter, correct_letter in zip(guess, word)
        ]

        non_corrects = (
            (letter for res_pos, letter in zip(result, word) if res_pos != Result.OK)
        )

        letter_counter = Counter(non_corrects)
        
        for idx, letter in enumerate(guess):
            if result[idx] != Result.OK and letter_counter[letter] > 0:
                letter_counter[letter] -= 1
                result[idx] = Result.OK_LETTER

        return result

    def eval_guess(self, guess : str) -> None:
        next_guess = self.eval_position(guess, self.__word)

        self.__guesses_results.append(next_guess)

        return self.__guesses_results[-1]


def print_position(last_guess : list[Result]) -> None:
    for letter_result in last_guess:
        match letter_result:
            case Result.OK:
                print('O', end='')
            case Result.OK_LETTER:
                print('P', end='')
            case Result.FAIL:
                print('X', end='')

def has_ended(guess : list[Result]) -> bool:
    return all(letter_result == Result.OK for letter_result in guess)

def play_game(word : str, max_rounds : int) -> tuple[Boolean, Game]:
    game = Game(word)

    round_num = 0
    while round_num < max_rounds:
        guess_word = input().strip()

        if re.match(r'\s', guess_word) is not None:
            print('\nOnly one word per line!\n')
            continue

        guess_word = unidecode(guess_word).upper()

        if len(guess_word) != len(word):
            print(f'\The word needs to have {len(word)} letters!\n')
            continue 
        
        round_result = game.eval_guess(guess_word)

        print_position(round_result)
        print('\n')

        if has_ended(round_result):
            return True, game

        round_num += 1

    return False, game

def main():
    dict_file = pathlib.Path('Lista-de-Palavras.txt')

    with open(dict_file, 'r') as dist_lines:
        wordlist = [line.rstrip() for line in dist_lines.readlines()]

    word_len = 5
    max_rounds = 6

    words = (word for word in wordlist if len(word) == word_len)
    words = (word for word in words if re.search(r'[^A-Z]', word) is None)

    selected_word = choice(list(words))
    print(selected_word)

    play_game(selected_word, max_rounds)

if __name__ == '__main__':
    main()



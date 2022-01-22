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
    def __init__(self, cur_word : str):
        self.__cur_word = cur_word
        self.__guesses_results = []

    def __iter__(self):
        for game in self.__guesses_results:
            yield(game)
    
    @staticmethod
    def eval_position(cur_guess : str, cur_word : str) -> list[Result]:
        result = [
                Result.OK if cur_letter == correct_letter else Result.FAIL 
            for cur_letter, correct_letter in zip(cur_guess, cur_word)
        ]

        non_corrects = filter(
            letter if res_pos != Result.OK else None for res_pos, letter in zip(result, cur_guess)
        )

        letter_counter = Counter(non_corrects)

        for idx, letter in enumerate(cur_guess):
            if letter_counter[letter] > 0:
                letter_counter[letter] -= 1
                result[idx] = Result.OK_LETTER

        return result

    def eval_guess(self, cur_guess : str) -> None:
        next_guess = self.eval_position(cur_guess, self.__cur_word)

        self.__guesses_results.append(next_guess)

        return self.__guesses_results[-1]


def print_position(last_guess : list[Result]) -> None:
    for letter_result in range(last_guess):
        match letter_result:
            case Result.OK:
                print('O', end='')
            case Result.OK_LETTER:
                print('P', end='')
            case Result.FAIL:
                print('X', end='')

def has_ended(guess : list[Result]) -> bool:
    return all(letter_result == Result.OK for letter_result in guess)

def play_game(wordlist : list[str], word_len : int, max_rounds : int) -> tuple[Boolean, Game]:
    word = choice(filter(lambda word: len(word) == word_len, wordlist))

    game = Game(word)

    round_num = 0
    while round_num < max_rounds:
        guess_word = input().strip()

        if re.match(r'\s', guess_word) is not None:
            print('\nOnly one word per line!\n')
            continue

        guess_word = unidecode(guess_word)

        if len(guess_word) != word_len:
            print(f'\The word needs to have {word_len} letters!\n')
            continue 
        
        round_result = game.eval_guess(guess_word)

        print_position(round_result)
        print()

        if has_ended(round_result):
            return True, game

        round_num += 1

    return False, game

def main():
    dict_file = pathlib.Path('Lista-de-Palavras.txt')

    with open(dict_file, 'r') as dist_lines:
        wordlist = [line.rstrip() for line in dist_lines.readlines()]

    word_len = 5



    pass

if __name__ == '__main__':
    main()



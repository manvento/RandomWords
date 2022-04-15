import argparse
import math
import string
from random import random, randint, choice
from typing import List, Dict

from random_words import RandomWords

SPECIAL_CHARS = ['', ' ', '!', '#', '$', '%', '&', "'", '(', ')', '+', ',', '-', '.', '/', ':', ';', '=', '?', '@', '[',
                 '\\', ']']


def randomcase(s: str) -> str:
    result = ''
    for c in s:
        case = randint(0, 1)
        if case == 0:
            result += c.upper()
        else:
            result += c.lower()
    return result


def get_random_words(count: int = 100, case_dict: Dict[str, float] = None) -> List[str]:
    """
    Return random words from nouns.dat.
    :param count: Number of words to return.
    :param case_dict: if setted allows to change cases in upper, lower and mixed.
    The dict contains the ratio for random changes. E.g.:
    { 'lower': 0.25, 'upper': 0.25, 'mixed': 0.5 }
    means the 25% of words will be lowercase, 25% upper and 50% mixed.
    :return: a list of words.
    """
    words = RandomWords().random_words(count=count)
    generated_words = {'lower': 0, 'upper': 0, 'mixed': 0}

    if case_dict:
        lower_ratio = case_dict.get('lower')
        upper_ratio = case_dict.get('upper')
        mixed_ratio = case_dict.get('mixed')
        assert lower_ratio >= 0 and upper_ratio >= 0 and mixed_ratio >= 0
        assert 0.99 <= lower_ratio + upper_ratio + mixed_ratio <= 1.0
        upper_ratio += lower_ratio
        # change cases
        for i in range(len(words)):
            r = random()
            if r <= lower_ratio:
                generated_words['lower'] += 1
                words[i] = words[i].lower()
            elif r <= upper_ratio:
                generated_words['upper'] += 1
                words[i] = words[i].upper()
            else:
                generated_words['mixed'] += 1
                words[i] = randomcase(words[i])

    print(f"generated {len(words)} words. "
          f"{generated_words['lower']} lowercase, "
          f"{generated_words['upper']} uppercase and "
          f"{generated_words['mixed']} mixed")
    return words


def get_random_numbers(count: int = 100, min_length=3, max_length=15,
                       max_text_length=5, add_special_char: bool = False,
                       with_text_dict: Dict[str, float] = None) -> List[str]:
    """
    Return random words from lorem_ipsum.dat.
    :param min_length: min length for final string
    :param max_length: max length for final string
    :param max_text_length: max text size (non digits). Valid if with_text_dict is not None.
    :param count: Number of words to return.
    :param with_text_dict: if setted allows to add text to numbers.
    :param add_special_char: if true, adds a special character from the list.
    The dict contains the ratio for the changes. E.g.:
    { 'no': 0.5, 'after': 0.2, 'before': 0.2, 'inside': 0.1}
    means the 25% of words will be lowercase, 25% upper and 50% mixed.
    :return: a list of words.
    """
    max_num_length = max_length - max_text_length if with_text_dict else max_length
    words = []
    generated_words = {'no': 0, 'after': 0, 'before': 0, 'inside': 0}
    for i in range(0, count):
        digits = randint(min_length, max_num_length)
        text_size = randint(1, max_text_length)
        number = randint(10 ** (digits - 1), (10 ** digits) - 1)
        words.append(str(number))
        if with_text_dict:
            no_ratio = with_text_dict.get('no')
            after_ratio = with_text_dict.get('after')
            before_ratio = with_text_dict.get('before')
            inside_ratio = with_text_dict.get('inside')
            assert no_ratio >= 0 and after_ratio >= 0 and before_ratio >= 0 and inside_ratio >= 0
            assert 0.99 <= no_ratio + after_ratio + before_ratio + inside_ratio <= 1
            inside_ratio += before_ratio
            after_ratio += inside_ratio
            r = random()
            text = ''.join(choice(string.ascii_letters) for _ in range(text_size))
            sep1 = choice(SPECIAL_CHARS) if add_special_char else ''
            sep2 = choice(SPECIAL_CHARS) if add_special_char else ''

            if r <= before_ratio:
                generated_words['before'] += 1
                words[i] = f'{text}{sep1}{words[i]}{sep2}'
            elif r <= inside_ratio:
                generated_words['inside'] += 1
                n = len(words[i])
                middle = math.floor(n / 2)
                p1 = words[i][0:middle]
                p2 = words[i][middle:n]
                words[i] = f'{p1}{sep1}{text}{sep2}{p2}'
            elif r <= after_ratio:
                generated_words['after'] += 1
                words[i] = f'{sep1}{words[i]}{text}{sep2}'
            else:  # don't change anything
                generated_words['no'] += 1

            words[i] = words[i].strip()

    print(f"generated {len(words)} words. "
          f"{generated_words['no']} consisting in only digits, "
          f"{generated_words['before']} consisting in digits preceded by text, "
          f"{generated_words['after']} consisting in digits followed by text and "
          f"{generated_words['inside']} consisting in digits with text inside")
    return words


def main(filename: str, add_special_char: bool):
    words = get_random_words(count=5000, case_dict={
        'lower': 0.33,
        'upper': 0.33,
        'mixed': 0.34
    })
    words.extend(get_random_numbers(count=5000,
                                    min_length=3,
                                    max_length=20,
                                    max_text_length=5,
                                    add_special_char=add_special_char,
                                    with_text_dict={
                                        'no': 0.5,
                                        'after': 0.2,
                                        'before': 0.2,
                                        'inside': 0.1
                                    }))
    words.sort(key=len)
    # print dictionary to file
    with open(filename, 'w') as f:
        for w in words:
            f.write(w)
            f.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Makes a random dictionary.')
    parser.add_argument('filename', type=str, help='output file')
    parser.add_argument('--special-characters', '-s', action='store_true',
                        help='if set, adds special characters')

    args = parser.parse_args()
    main(args.filename, args.special_characters)

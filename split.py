from sklearn.model_selection import train_test_split
from typing import List
import argparse


def get_chars_in_text(text: str) -> List[str]:
    return get_unique_values([char for char in text])


def get_unique_values(items: List[str]):
    return list(dict.fromkeys(items))


def split(filename: str, validation_ratio: float = 0.2):
    with open(filename) as f:
        lines = f.readlines()

    # label parts should be in uppercase
    alphabet = []
    for i in range(len(lines)):
        parts = lines[i].split('\t', 1)
        label = parts[1].lower()
        alphabet.extend(get_chars_in_text(label))
        alphabet = get_unique_values(alphabet)
        lines[i] = f'{parts[0]}\t{parts[1].lower()}'

    # randomise order
    train, test = train_test_split(lines, test_size=validation_ratio, shuffle=True)

    f_parts = filename.rsplit('.', 1)

    with open(f'{f_parts[0]}_train.{f_parts[1]}', 'w') as f:
        f.writelines(train)
        print(f'Wrote train dataset to {f.name}')

    with open(f'{f_parts[0]}_val.{f_parts[1]}', 'w') as f:
        f.writelines(test)
        print(f'Wrote validation dataset to {f.name}')

    alphabet.remove('\n')
    alphabet.sort()
    print(f'Dictionary alphabet is: {alphabet}')


def main():
    parser = argparse.ArgumentParser(description='Split text files by lines.')
    parser.add_argument('filename', type=str,
                        help='file to split')
    parser.add_argument('--validation-ratio', '-v', type=float, default=0.2,
                        help='validation ratio (e.g. 0.2 keeps 80% of input file '
                             'for training and 20% for validation')

    args = parser.parse_args()

    split(filename=args.filename, validation_ratio=args.validation_ratio)


if __name__ == "__main__":
    main()

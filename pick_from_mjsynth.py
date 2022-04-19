import argparse
import os
import shutil
import string
from random import shuffle
from typing import List, Dict, Union

SPECIAL_CHARS = [' ', '+', '-', '.', ':', '=', ',', ';']


def pick_rows(filename: str, rows: int) -> List[Dict[str, Union[str, int]]]:
    """
    Opens the file and picks randomly a number rows.
    :param filename: mjsynth input file
    :param rows: rows to extract.
    :return: extracted data in this format:
    - path: folder where the file should be found;
    - name: name of the file;
    - text: text contained in the image.
    """
    alphabet = string.digits + string.ascii_letters + ''.join(SPECIAL_CHARS)
    lines = []
    result = []
    with open(filename, 'r', newline='\n') as f:
        lines = f.readlines()

    shuffle(lines)
    i = 0

    for line in lines:
        if len(result) >= rows:
            break
        line = line.strip()
        full_path = line.split(' ', 2)[0].strip()
        if not full_path:
            continue
        split_path = os.path.split(full_path)
        path = split_path[0]
        name = split_path[-1]
        text = name.split('_')[1]
        extra_alphabet_chars = list(filter(lambda x: x not in alphabet, list(text)))
        if extra_alphabet_chars:
            print(f'Found text not compliant to alphabet: {text}')
            print(f'Non compliant characters are: {extra_alphabet_chars}')
        else:
            result.append({
                'id': i,
                'path': path,
                'name': name,
                'text': text
            })
            i += 1

    return result


def copy_images(records: List[Dict[str, Union[str, int]]], output_path: str):
    output_path = os.path.join(output_path, 'images')
    os.makedirs(output_path)

    for record in records:
        src_image = os.path.join(record['path'], record['name'])
        target_image = os.path.join(output_path, f"img_{record.get('id'):06}.jpg")
        assert os.path.exists(src_image) and os.path.isfile(src_image), \
            f'{src_image} does not exist or is not a file.\nRecord: {record}'
        shutil.copy2(src_image, target_image)


def save_pairs(records: List[Dict[str, Union[str, int]]], output_path: str):
    filename = os.path.join(output_path, 'pairs.txt')
    with open(filename, 'w', newline='') as f:
        for record in records:
            f.write('#REPLACE_WITH_PATH#')
            f.write(f"img_{record.get('id', -1):06}.jpg")
            f.write('\t')
            f.write(record.get('text'))
            f.write('\n')


def main(filename: str, output_path: str, num_rows: int):
    if os.path.exists(output_path):
        assert os.path.isdir(output_path)
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    records = pick_rows(filename, num_rows)
    save_pairs(records, output_path)
    copy_images(records, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Pick from mjsynth dataset, using common keras ocr format')
    parser.add_argument('input_filename', type=str, help='mjsynth input text file')
    parser.add_argument('output_path', type=str, help='path where extraction should be stored.')
    parser.add_argument('--num-items', '-n', type=int, default=100,
                        help='Number of items to pick.')

    args = parser.parse_args()
    main(args.input_filename, args.output_path, args.num_items)

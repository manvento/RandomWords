import argparse
import codecs
import re
import shutil
import os

import split

PAIRS_FILE_NAME = 'pairs.txt'
IMAGES_FOLDER_NAME = 'images'


def copy_data(input_folder: str, output_folder: str):
    print(f'merging {input_folder}')
    # first copy the files
    assert os.path.exists(input_folder) and os.path.isdir(input_folder), "input folder missing or it's a regular file"
    input_content = os.listdir(input_folder)
    assert PAIRS_FILE_NAME in input_content and IMAGES_FOLDER_NAME in input_content
    input_img_folder = os.path.join(input_folder, IMAGES_FOLDER_NAME)
    output_img_folder = os.path.join(output_folder, IMAGES_FOLDER_NAME)
    os.makedirs(output_img_folder, exist_ok=True)
    shutil.copytree(input_img_folder, output_img_folder, dirs_exist_ok=True)

    with codecs.open(os.path.join(input_folder, PAIRS_FILE_NAME), 'r', encoding='utf-8') as in_stream:
        lines = in_stream.read().splitlines(keepends=False)

    # collapse multiple spaces
    lines = [re.sub(' +', ' ', x) for x in lines]
    # remove empty rows
    lines = [x for x in lines if len(x.strip()) > 0]

    with codecs.open(os.path.join(output_folder, PAIRS_FILE_NAME), 'a', encoding='utf-8') as out_stream:
        out_stream.write('\n'.join(lines))
        out_stream.write('\n')


def main():
    parser = argparse.ArgumentParser(description='Merge datasets.'
                                                 'Each folder should contain a pairs.txt file '
                                                 'and an images folder.')
    parser.add_argument('output_folder', type=str,
                        help='folder where merged dataset should be put.')
    parser.add_argument('--input-folders', '-i', type=str, nargs='+', required=True,
                        help='list of input folders.')

    parser.add_argument('--validation-ratio', '-v', type=float, default=0.2,
                        help='validation ratio for split (e.g. 0.2 keeps 80% of input file '
                             'for training and 20% for validation')

    args = parser.parse_args()

    if os.path.exists(args.output_folder):
        shutil.rmtree(args.output_folder)

    for input_folder in args.input_folders:
        copy_data(input_folder, args.output_folder)

    # now, split train/validation
    split.split(filename=os.path.join(args.output_folder, PAIRS_FILE_NAME), validation_ratio=args.validation_ratio)


if __name__ == "__main__":
    main()

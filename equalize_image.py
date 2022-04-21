import argparse
import os
import re
import shutil

import cv2 as cv


def normalize_image(src):
    src = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # create a CLAHE object (Arguments are optional).
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(src)


def normalize(src_path, target_path):
    for root, dirs, files in os.walk(src_path):
        for file in files:
            if re.search("(jpg|png|jpeg|gif)", file, re.IGNORECASE):
                image = cv.imread(os.path.join(root, file))
                image = normalize_image(image)
                cv.imwrite(os.path.join(target_path, file), image)


def main():
    parser = argparse.ArgumentParser(description='Equalizes images.')
    parser.add_argument('--input', '-i', help='Path to input folder.')
    parser.add_argument('--output', '-o', help='Path to output folder.')
    args = parser.parse_args()
    assert os.path.isdir(args.input), "input folder not found"
    assert not os.path.isfile(args.output), "output folder is a regular file"

    if os.path.exists(args.output):
        shutil.rmtree(args.output)
    else:
        os.makedirs(args.output)

    normalize(args.input, args.output)


if __name__ == "__main__":
    main()

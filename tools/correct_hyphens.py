#! /usr/bin/env python3

"""
Remplacer correctement les fins de lignes avec un tiret '-'
"""

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='Text to be corrected', required=True)
parser.add_argument('-d', '--dict', help='Dictionary of words with hyphen', required=True)
parser.add_argument('-o', '--output', help='Output filename')
args = parser.parse_args()


def correct_line(line, next_word, words_with_hyphen):
    if not line.endswith("-") or next_word is None:
        return line + "\n"

    trimed_line = line.rstrip("-")

    try:
        last_word = trimed_line.split()[-1]
    except IndexError:
        last_word = ""

    # Remove apostrophe if any
    last_word = re.split(r"['’\"]", last_word)[-1]
    next_word = re.sub(r"[’'—\.:…\"\?!,\n«»“”()]", "", next_word)

    if f"{last_word.lower()}-{next_word.lower()}" in words_with_hyphen:
        return line
    else:
        return trimed_line


# Read the list of words
with open(args.dict, "r") as fh:
    words = set(line.rstrip().lower() for line in fh.readlines())

# Parse text and remove '-' only if necessary
result = []
with open(args.input, "r") as fh:
    content = fh.read().splitlines()
    for i, line in enumerate(content):
        try:
            next_word = content[i+1].split()[0]
        except IndexError:
            next_word = None
        result.append(correct_line(line, next_word, words))

# Write output at once
if args.output:
    print("".join(result), file=open(args.output, "w"))
else:
    print("".join(result))

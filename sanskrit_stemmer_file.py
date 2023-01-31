#!/usr/bin/env python3

import sys

import json
from tqdm import tqdm

import sh_segmenter as sh

script, input_file_name, output_file_name, stemmer_format = sys.argv

input_file = open(input_file_name, "r")
all_lines_str = input_file.read()
input_file.close()

all_lines = list(filter(None, all_lines_str.split("\n")))

# get the stemmer function using the stemmer format
stemmer_fn = sh.get_stemmer_fn(stemmer_format)

output = {}

for i in tqdm(range(len(all_lines))):
    word = all_lines[i]
    result = sh.run_stemmer_fn(word, stemmer_fn)
    output[word] = json.loads(result)

with open(output_file_name, 'w') as f:
    json.dump(output, f)
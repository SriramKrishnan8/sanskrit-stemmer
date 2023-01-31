#!/usr/bin/env python3

import sys

import sh_segmenter as sh

script, input_text, stemmer_format = sys.argv

output = sh.run_stemmer(input_text, stemmer_format)

print(output)

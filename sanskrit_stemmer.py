#!/usr/bin/env python3

import sys

import sh_segmenter as sh

script, input_text, stemmer_format = sys.argv

output = ""
if stemmer_format == "word":
    output = str(sh.request_word_analysis(input_text))
elif stemmer_format == "sent-iter":
    output = str(sh.request_sentence_analysis_iterative(input_text))
elif stemmer_format == "sent-joint":
    output = str(sh.request_sentence_analysis_joint(input_text))
# The following two cases are under development and hence commented out
#elif stemmer_format == "word-full":
#    output = str(sh.request_word_analysis(input_text))
#elif stemmer_format == "sent-full":
#    output = str(sh.request_word_analysis(input_text))
else:
    output = str(sh.request_word_analysis(input_text))

print(output)

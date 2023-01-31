# Sanskrit Stemmer using Sanskrit Heritage Segmenter

The [Sanskrit Heritage Platform](https://sanskrit.inria.fr/) hosts various tools of which the Segmenter is used to fetch the morphological analysis of a given word. The Segmenter uses its own lexicon and finite state automata for the process of both segmentation and morphological parsing.

There could be multiple possible morphological analysis and hence all of these are produced by the Stemmer.

## Pre-requisites

1. By default, the stemmer fetches the results from the server (https://sanskrit.inria.fr). Alternatively, the entire Sanskrit Heritage Platform can be installed locally and the stemmer can access the local segmenter for the analysis. The global parameter `urlname` in `sh_segmenter.py` should be changed.
2. The following packages are mandatory:
    * requests
	* psutil
	* tqdm

    These can be installed using pip:
    ```
    pip3 install requests psutil tqdm
    ```

## Usage

```
python3 sanskrit_stemmer.py gacCawi word
```

## Result

```
{
	'word': ['gacCawi'],
	'morph': [{
		'derived_stem': 'gam',
		'base': '',
		'derivatioanal_morph': '',
		'inflectional_morphs': ['pr. [1] ac. sg. 3']
	}, {
		'derived_stem': 'gacCaw',
		'base': 'gam',
		'derivatioanal_morph': 'ppr. [1] ac.',
		'inflectional_morphs': ['n. sg. loc.', 'm. sg. loc.']
	}]
}
```
## Input

The Stemmer accepts two arguments: input_text and format.
The input_text is required in WX notation. The following are the accepted formats:

1. word -> analyses the given word and produces the results.
2. sent-iter -> analyses the given sentence word by word and produces the analyses for each of the words separately
3. sent-joint -> analyses the given sentence at one go and produces the analyses for all the words

## Output

There are two parts of the output: word and morph.
1. word -> list of possible word form(s) (includes compound-splits also). For input as sentences, this field would produce the best possible segmentation solutions.
2. morph -> list of possible morphological analyses with each **morph** having the following keys:
    * derived_stem -> prātipadika
    * base -> root (dhātu)
    * derivational_morph -> derivational morphological analysis (primary or secondary)
    * inflectional_morphs -> list of possible inflectional morphological analysis

    The stem / base may contain indices indicating the homonymy index of the stem in the Sanskrit Heritage Lexicon.

## Additional Information

1. An ipython notebook (`Sanskrit Stemmer Instructions`) is provided for basic usage of the stemmer.
2. A sample notebook (`sample_stemming.ipynb`) is provided with examples from the instructions.
3. Sample files with input words and sentences (`sample_input_words.txt`, `sample_input_sents.txt`) are provided for testing the stemmer.
4. A shell script (`sanskrit_stemmer.sh`) with examples is provided to run the scripts. Uncomment each to try out the examples from the terminal.
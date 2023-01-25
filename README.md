# Sanskrit Stemmer using Sanskrit Heritage Segmenter

The Sanskrit Heritage Platform hosts various tools of which the Segmenter is used to fetch the morphological analysis of a given word. The Segmenter uses its own lexicon and finite state automata for the process of both segmentation and morphological parsing.

There could be multiple possible morphological analysis and hence all of these are produced by the Stemmer.

## Usage

```
sh sanskrit_stemmer.sh gacCawi word
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
1. word -> list of possible word form(s) (includes compound-splits also)
2. morph -> list of possible morphological analyses

Each **morph** has the following keys:
* derived_stem -> prātipadika
* base -> root (dhātu)
* derivational_morph -> derivational morphological analysis (primary or secondary)
* inflectional_morphs -> list of possible inflectional morphological analysis

The stem / base may contain indices indicating the homonymy index of the stem in the Sanskrit Heritage Lexicon.
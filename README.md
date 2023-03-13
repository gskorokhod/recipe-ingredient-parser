# recipe-ingredient-parser

## IMPORTANT: Dataset
The dataset could not be shared here because the file is too large.
Please download it from the following link and put the files in /data
https://nextcloud.gskorokhod.com/s/ex7RZTd8GwG56Gd

## Description
This is a CRF (Conditional Random Fields) model, built with [pycrfsuite](https://python-crfsuite.readthedocs.io/en/latest/),
which extracts ingredient names, measurement units, and amounts from recipe phrases.

## Usage
Create an instance of the Parser class from parse.py and use its
parse() method to get python dictionaries with labels for all words in the recipe phrase

## Plans
Maybe I'll write a shell script for parsing lots of phrases in bulk from a file.
Also, a clean up / restructuring of the code is planned

## Example
The following phrase:
"200 grams of potatoes, peeled and coarsely grated"
Will be parsed as:
```
{
  '200': 'B-QTY',
  'grams': 'B-UNIT',
  'of': 'OTHER',
  'potatoes': 'B-NAME',
  ',': 'B-COMMENT',
  'peeled': 'I-COMMENT',
  'and': 'I-COMMENT',
  'coarsely': 'I-COMMENT',
  'grated': 'I-COMMENT'}
```

## Provenance
Inspired by the original work of Erica Greene and Adam McCaig: [link](https://github.com/nytimes/ingredient-phrase-tagger)
(released under the Apache 2.0 license).
The original approach of using CRF to parse recipes is described [here](https://archive.nytimes.com/open.blogs.nytimes.com/2016/04/27/structured-ingredients-data-tagging/).

All code in this repository, unless stated otherwise, is my own original work.

The dataset is based on the original NYT dataset from the above repository, but modified to include a broader range of measurement units
(such as common metric system units).

## Authorship
Written by Georgii Skorokhod
Trained using University of St Andrews hardware
Contact me: skorokhod.g@gmail.com

## References
- https://archive.nytimes.com/open.blogs.nytimes.com/2016/04/27/structured-ingredients-data-tagging/
- https://github.com/nytimes/ingredient-phrase-tagger
- https://albertauyeung.github.io/2017/06/17/python-sequence-labelling-with-crf.html/
- https://python-crfsuite.readthedocs.io/en/latest/

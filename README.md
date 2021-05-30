# clozy v.0.0.1
a script for creating fill-in-the-blank (aka cloze) exercises 

## Introduction
Inspired by the seminar "Intermediate Methods and Programming in Digital Linguistics", I got the idea to create a tool that would help me, as well as perhaps other German teachers, to create cloze exercises for students in my course. The tool uses the SpaCy library for part-of-speech recognition, required for two of the three main functions of the tool.

The output contains the cloze exercise with enumerated blanks, the removed words in randomized order (_Schüttelbox_) and the solution.

## Requirements
The SpaCy small German model is required for using this program.

Install SpaCy:
```bash
pip install spacy

```
Download German model:
```bash
python -m spacy download de_core_news_sm

```

## Usage
Using a command line interface, the user supplies a text-file containing the text to be used for creating the exercise, as well as one or more flags for specifying the type of exercise that should be created. The three exercise types are:

* Remove every n-th word, for instance every 10th word in the text.
* Remove all adjective suffixes.
* Remove all words belonging to a certain part-of-speech. 

### Examples
A program call might look like this:
```bash
python cli.py my_text.txt --nth 8 
```
The input file is a positional argument that must follow first. It is also possible to supply a list of files using wildcards:

```bash
python cli.py texts/*.txt --nth 8 
```

This call would produce a cloze with every 8th word being a blank.

#### Print to file
In order to store the exercises produced in a file instead of printing to the screen (stdout) use the flag `--outfile`. The default filename is `output.txt`, but a custom filename may be specified, e.g. `--outfile outtext.txt`.

#### Part-of-speech blanks
The part-of-speech blank function is called with the `--pos` flag followed by one or more postags to be removed. 
```bash
python cli.py my_text.txt --pos NOUN
```

For a list of postags contained in a text the flag `--poslist` can be used.

```bash
python cli.py my_text.txt --poslist
```
(Will list up to a maximum of five words per postag)


##### Output example:
```bash
Auf, herunter, unter, von, davon, : ADP
einem, ein, Ein, den, der, : DET
Baum, Hahn, Fuchs, Hunger, Friede, : NOUN
saß, vorbeikam, sah, sagte, Komm, : VERB
alter, Allgemeiner, Lieber, wunderbare, Entschuldige, : ADJ
der, er, mich, wir, das, : PRON
gerade, doch, herab, heute, ab, : ADV
und, denn, : CCONJ
da, dass, : SCONJ
hatte, ist, worden, sind, habe, : AUX
Komm, : PROPN
zwei, vier, : NUM
nicht, zu, : PART
```

Sometimes a text will contain a lot of words of the same part-of-speech, too many to be removed in order to create a cloze that makes sense. In that case, the amount of words that will be removed can be limited with the flag `--pospercent` followed by the percentage of words that should be removed, e.g. `--pospercent 70`.


#### Adjective suffix blanks
Adjective declination in German is highly complex. This is why exercises where students are required to fill in the adjective endings are very helpful. Adjective suffix blanks can be created with the `--adj` call.

```bash
python cli.py my_text.txt --adj
```
With this function, no _Schüttelbox_ will be produced.

## Data
Four sample texts can be found in the folder `sample_texts`. These texts can be used to test the program. See [References](#references) for origin.

## Demo
Run `cli.py` with the flag `--demo` or simply run `demo.py` for a quick demo.

## Future features
Some future features that might be included are:
* German UI
* Simplified postags in German that will enable the user to use tags like `NOMEN`, `ADJ` or 'PRAEP'.
* Support for other languages, i.e. English, Dutch

## References
### Sample texts
* text1.txt and text2.txt taken from: Dreyer, Hilke; Schmidt, Eberhard: Lehr- und Übungsbuch der deutschen Grammatik, die Gelbe aktuell, 1. Auflage, Hueber Verlag, Ismaning 2009, S. 300f
* text3.txt - Danger Dan: Das ist alles von der Kunstfreiheit gedeckt, 2021
* text4.txt - https://lingua.com/de/deutsch/lesen/flughafen/

2009. Lehr- und Bahbuch. 1st ed. Ismaning: Hueber Verlag, pp.300-301.
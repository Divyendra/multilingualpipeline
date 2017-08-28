# Multilingual Corpus Pipeline
The aim of this pipeline is to take as input one of the files in the NewsScape dataset and output an XML-style file with sentence splits; lemmas, POS tagging and dependency information for each word.  The pipeline can be summarized in 5 major steps:
- Extracting useful text from the input file - using a custom python script (`preprocess.py`)
- Sentence splitting - using [Pragmatic Segmenter](https://github.com/diasks2/pragmatic_segmenter)
- Tokenization - using [Syntaxnet](https://github.com/tensorflow/models/blob/master/syntaxnet/g3doc/universal.md) for supported languages(German, Portuguese, Polish, Swedish) and [Treetagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/) for some others(Russian)
- POS Tagging and Dependency Parsing - using Syntaxnet
- Lemmatizing - using [CST's Lemmatizer](https://cst.dk/online/lemmatiser/uk/) for supported languages(German, Portuguese, Polish, Russian) and Treetagger for some others (Swedish)


## How to Run:

This pipeline was written to run on a singularity container and hence may not run standalone without all the dependencies. You can download the `syntaxnet_v1.def` file and create a container as described [here](http://www.redhenlab.org/home/tutorials-and-educational-resources/multilingual-corpus-pipeline). After building the container, shell into it and then `cd /opt/models/syntaxnet`. Now, you can run the pipeline as `sh /opt/multilingualpipeline/run.sh <input-file-name> <language-code>`.  
If you want to run this outside a container, follow the steps starting from line 17 in `syntaxnet_v1.def`. Note that you may need to use `sudo` with some of them. You should now be able to run the pipeline as described above.


## Documentation

### preprocess.py
This script takes as input a NewsScape text file and extracts the relevant text from it as output. It also calculates the relative occurrence time of each block of words and includes it in the output - this can be toggled on or off using the `-t` option.  
Usage: `python preprocess.py -inf <input-file-name> -t <0 or 1>`

### ss.rb
This is a sentence splitter script which takes as input a body of text and the corresponding language(use two-letter [ISO 639-1](https://www.tm-town.com/languages) code). The output is sentences from the text, each on a new line. The output from this is used as input to the tokenizer. Note that you will have to install the pragmatic_segmenter package before running this standalone.  
Usage: `cat <input-file-name> | ruby ss.rb <language-code>`

### parser.py
This script is used to unify the output from the lemmatizer and syntaxnet parser into the desired xml format. It takes as input the NewsScape file, lemmatizer output, syntaxnet parser output and tokenizer output(with timing info) to produced the xml file.  
Usage: `python parser.py -i <NewsScape-file-name> -l <lemma_output> -t <tokenized_out_with_time> -s <parser-output>`

### run.sh
This bash script takes a NewsScape file and the corresponding language(use two-letter [ISO 639-1](https://www.tm-town.com/languages) code) as input, runs the complete pipeline in sequence and outputs an xml file.  
This needs to be run from `models/syntaxnet/` folder.
Usage: `sh run.sh <input-file-name> <language-code>`

## To-Do
- Find a good lemmatizer for Norwegian and include it in the pipeline.
- Make a comprehensive list of the morphological features.

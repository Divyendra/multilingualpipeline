#!/usr/bin/env bash

MODELS=syntaxnet/models/other_language_models
SYNT_SCRIPTS=syntaxnet/models/parsey_universal
LEMMATIZER=/opt/Lemmatizer/cstlemma/src
TREETAGGER=/opt/Treetagger
SCRIPTS=/opt/multilingualpipeline

if [ "$2" = "de" ]; then
        alias tokenize='$SYNT_SCRIPTS/tokenize.sh $MODELS/German'
        alias parse='$SYNT_SCRIPTS/parse.sh $MODELS/German'
        alias lemmatize='$LEMMATIZER/./cstlemma -L -f $LEMMATIZER/Rules/German/flexrules -i'
elif [ "$2" = "pt" ]; then
        alias tokenize='$SYNT_SCRIPTS/tokenize.sh $MODELS/Portuguese'
        alias parse='$SYNT_SCRIPTS/parse.sh $MODELS/Portuguese'
        alias lemmatize='$LEMMATIZER/./cstlemma -L -f $LEMMATIZER/Rules/Portuguese/flexrules-supplement-with-dict -d $LEMMATIZER/Rules/Portuguese/dict -i'
elif [ "$2" = "pl" ]; then
        alias tokenize='$SYNT_SCRIPTS/tokenize.sh $MODELS/Polish'
        alias parse='$SYNT_SCRIPTS/parse.sh $MODELS/Polish'
        alias lemmatize='$LEMMATIZER/./cstlemma -L -f $LEMMATIZER/Rules/Polish/flexrules -d $LEMMATIZER/Rules/Polish/dict -i'
elif [ "$2" = "sv" ]; then
        alias tokenize='$SYNT_SCRIPTS/tokenize.sh $MODELS/Swedish'
        alias parse='$SYNT_SCRIPTS/parse.sh $MODELS/Swedish'
        # alias lemmatize='$LEMMATIZER/./cstlemma -L -f $LEMMATIZER/Rules/Swedish/ -d $LEMMATIZER/Rules/Swedish/ -i'
elif [ "$2" = "nb" ]; then #nn,nb
        alias tokenize='$SYNT_SCRIPTS/tokenize.sh $MODELS/Norwegian'
        alias parse='$SYNT_SCRIPTS/parse.sh $MODELS/Norwegian'
        # alias lemmatize='$LEMMATIZER/./cstlemma -L -f $LEMMATIZER/Rules/Norwegian/ -d $LEMMATIZER/Rules/Norwegian/ -i'
elif [ "$2" = "ru" ]; then
        #alias tokenize='$SYNT_SCRIPTS/tokenize.sh $MODELS/Russian'
        alias tokenize='sed -e '\''s/$/ <s>/'\'' | perl $TREETAGGER/cmd/utf8-tokenize.perl | python $TREETAGGER/make_sents.py'
        alias parse='$SYNT_SCRIPTS/parse.sh $MODELS/Russian-SynTagRus'
        alias lemmatize='$LEMMATIZER/./cstlemma -L -f $LEMMATIZER/Rules/Russian/flexrules2 -d $LEMMATIZER/Rules/Russian/dict -i'
elif [ "$2" = "da" ]; then
        #alias tokenize='$SYNT_SCRIPTS/tokenize.sh $MODELS/Danish'
        alias parse='$SYNT_SCRIPTS/parse.sh $MODELS/Danish'
        alias lemmatize='$LEMMATIZER/./cstlemma -L -f $LEMMATIZER/Rules/Danish/flexrules -d $LEMMATIZER/Rules/Danish/dict -i'
fi

#file_name=$(IFS='/' tokens=( "$1" ) && echo ${tokens[-1]})

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

python $SCRIPTS/preprocess.py -inf $1 -t 0 |
ruby $SCRIPTS/ss.rb $2 |
tokenize > /tmp/file_1wot.txt

cat /tmp/file_1wot.txt | parse > /tmp/file_2wot.txt

python $SCRIPTS/preprocess.py -inf $1 -t 1 |
ruby $SCRIPTS/ss.rb $2 |
tokenize > /tmp/file_1wt.txt

if [ "$2" = "sv" ]; then
        cat /tmp/file_1wot.txt | tr " " "\n" | $TREETAGGER/cmd/tree-tagger-swedish > /tmp/lemma_output
else
        lemmatize /tmp/file_1wot.txt > /tmp/lemma_output
fi
python $SCRIPTS/parser.py -i $1 -l /tmp/lemma_output -t /tmp/file_1wt.txt -s /tmp/file_2wot.txt #4 Files to be read
rm /tmp/lemma_output /tmp/file_1wt.txt /tmp/file_1wot.txt /tmp/file_2wot.txt

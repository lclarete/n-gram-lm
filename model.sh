#!/bin/bash

# Part 2: model building

set -eou pipefail

readonly TRAIN=train.txt

model() {
    # complile the FST
    farcompilestrings --fst_type=compact --token_type=byte "${TRAIN}" train.far

    # collecting counts of all n-grams up to order
    ngramcount --order=6 --require_symbols=false train.far 6.cnt

    # converting counts into a WFSA language model
    ngrammake --method=witten_bell 6.cnt 6.fst

    # pruneing the WFSA language model produced by ngrammake
    ngramshrink --method=relative_entropy --target_number_of_ngrams=1000000 6.fst lm.fst
}


model


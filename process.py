#!/usr/bin/env python

""" Read and process file """

import pandas as pd
import re


def download(filename):
    ans = []
    # open .tsv file
    with open(filename) as f:
    
        # Read data line by line
        for line in f:
            
            # split data by tab
            # store it in list
            l=line.split('\t')
            print(l)
            
            # append list to ans
            ans.append(l)
        
        # transform list in a dataframe
        df = pd.DataFrame(ans)
        df.columns = ['score', 'sentence']
    
    return df

def clear_score(col):
    col = re.sub('"', '', col)
    return pd.to_numeric(col)


def main():
    df = download("output.tsv")
    df.score = df.score.apply(clear_score)
    df = df.sort_values('score')
    df.to_csv('output_sorted2.csv', index=False)
    df.head(30).to_csv('head.csv')
    df.tail(30).to_csv('tail.csv')



if __name__ == "__main__":
    main()






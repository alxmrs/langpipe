# langpipe


A CLI for natural language processing via unix-like pipes.

# Description

Getting all the nouns from a corpus of transcripts, for example, is as easy as: 

```bash

langpipe \
	readlines -f ../raw_transcriptions_8000.txt \
	sentences \
		replace -f replacements.csv \
	words \
		filter-length-gte -n 3 \
		remove-stopwords -f stop_words.txt \
		filter-pos -p 'NN' -p 'NNP' -p 'NNS' -p 'NNPS' \
  trace
```

The goal here is to make NLP cleaning piplines reproducable and expressive. 

Users of this tool can think at a high level -- no need to be bogged down by the borning stuff. 

Commands and subcommands can be composable, modular, and flexible. 

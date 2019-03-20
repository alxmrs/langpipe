# langpipe


A CLI for natural language processing via unix-like pipes.

## Description

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


## Installation

`pip install git+https://github.com/alxrsngrtn/langpipe.git#egg=langpipe`


## Documentation

### `langpipe --help`
```
Usage: langpipe [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

  This script processes textfiles through the nltk and similar packages in a
  unix pipe.  One commands feeds into the next.

  Example:

      langpipe  readlines -f ../data_source.txt words remove-stopwords -f
      stop_words.txt trace

Options:
  --help  Show this message and exit.

Commands:
  filter-length-gte
  filter-pos
  readlines          Loads all the lines for one or more files.
  remove-stopwords
  replace            Replaces all instances of a string or regex pattern in...
  sentences          Tokenizes lines into sentences.
  trace              Writes input to stdin.
  words              Tokenizes lines into words.
```

### `langpipe readlines --help`
```Usage: langpipe readlines [OPTIONS]

  Loads all the lines for one or more files. The input parameter can be
  specified multiple items to load more than one text file.

Options:
  -f, --file PATH  The text file to read in.
  --help           Show this message and exit.
```

### `langpipe trace --help`
```Usage: langpipe trace [OPTIONS]

  Writes input to stdin.

Options:
  --help  Show this message and exit.
```

### `langpipe sentences --help`
```Usage: langpipe sentences [OPTIONS]

  Tokenizes lines into sentences. Downloads nltk resources if they don't
  exist.

Options:
  -l, --language TEXT  Language model
  --help               Show this message and exit.
```

### `langpipe words --help`
```Usage: langpipe words [OPTIONS]

  Tokenizes lines into words. Downloads nltk resources if they don't exist.

Options:
  -l, --language TEXT  Language model
  --help               Show this message and exit.
```

### `langpipe replace --help`
```Usage: langpipe replace [OPTIONS]

  Replaces all instances of a string or regex pattern in each input

Options:
  -s, --src, --source TEXT  The source, or target, to replace NOTE: This
                            argument is mutually exclusive with  arguments:
                            [f].
  -d, --dst, --dest TEXT    The destination, or replacement NOTE: This
                            argument is mutually exclusive with  arguments:
                            [f].
  -f, --file PATH           File of substitutions in CSV format NOTE: This
                            argument is mutually exclusive with  arguments:
                            [d, s].
  --help                    Show this message and exit.
```

### `langpipe remove-stopwords --help`
```Usage: langpipe remove-stopwords [OPTIONS]

Options:
  -f, --file PATH  path/to/stopwords/file.txt. One stop-word per line.
  --help           Show this message and exit.
```
### `langpipe filter-pos --help`
WIP
```Usage: langpipe filter-pos [OPTIONS]

Options:
  -p, --pos TEXT  Part-of-speech to allow to pass through. Can specify
                  multiple at once.
  --help          Show this message and exit.
```

### `langpipe filter-length-gte --help`
WIP
```Usage: langpipe filter-length-gte [OPTIONS]

Options:
  -n, --num INTEGER  Minimum length that values need to be.
  --help             Show this message and exit.
```


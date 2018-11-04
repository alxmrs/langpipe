import csv
import typing

import click
import nltk

from langpipe import types


@click.group(chain=True)
def cli():
    """This script processes textfiles through the nltk and similar packages in a unix pipe.
     One commands feeds into the next.

    Example:

        langpipe  readlines -f ../data_source.txt words remove-stopwords -f stop_words.txt trace
    """
    pass


@cli.resultcallback()
def process_commands(processors):
    """This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    """
    # Start with an empty iterable.
    stream = ()

    # Pipe it through all stream processors.
    for processor in processors:
        stream = processor(stream)

    # Evaluate the stream and throw away the items.
    for _ in stream:
        pass


@cli.command('readlines')
@click.option('-f', '--file', 'files', type=click.Path(),
              multiple=True, help='The text file to read in.')
@types.generator
def readlines_cmd(files) -> types.Lines:
    """Loads all the lines for one or more files. The input parameter can be specified
    multiple items to load more than one text file."""
    for file in files:
        try:
            click.echo('Opening "%s"' % file)
            if file == '-':
                for line in click.get_text_stdin():
                    yield line
            else:
                with open(file) as fi:
                    for line in fi.readlines():
                        yield line
        except Exception as e:
            click.echo('Could not open file "%s": %s' % (file, e), err=True)


@cli.command('trace')
@types.processor
def trace_cmd(lines: typing.Iterator) -> typing.Iterator:
    """Writes input to stdin."""
    try:
        for line in lines:
            click.echo(line)
            yield line
    except Exception as e:
        click.echo('Error tracing input. %s' % e, err=True)


@cli.command('sentences')
@click.option('-l', '--language', type=str, help='Language model', default='english')
@types.processor
def sentence_tokenize_cmd(lines: types.Lines, language: str) -> types.Sentences:
    """Tokenizes lines into sentences. Downloads nltk resources if they don't exist."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    line = ''
    try:
        for line in lines:
            for sent in nltk.sent_tokenize(line, language=language):
                yield sent
    except Exception as e:
        click.echo('Could not tokenize line into sentences "%s": %s' % (line[:min(10, len(line))], e), err=True)


@cli.command('words')
@click.option('-l', '--language', type=str, help='Language model', default='english')
@types.processor
def word_tokenize_cmd(lines: types.Lines, language: str) -> types.Words:
    """Tokenizes lines into words. Downloads nltk resources if they don't exist."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    line = ''
    try:
        for line in lines:
            for sent in nltk.word_tokenize(line, language=language):
                yield sent
    except Exception as e:
        click.echo('Could not tokenize line into words "%s": %s' % (line, e), err=True)


@cli.command('replace')
@click.option('-s', '--src', '--source',
              cls=types.MutuallyExclusiveOption, mutually_exclusive=['f'],
              type=str, help='The source, or target, to replace')
@click.option('-d', '--dst', '--dest',
              cls=types.MutuallyExclusiveOption, mutually_exclusive=['f'],
              type=str, default='', help='The destination, or replacement')
@click.option('-f', '--file',
              cls=types.MutuallyExclusiveOption, mutually_exclusive=['s', 'd'],
              type=click.Path(), help='File of substitutions in CSV format')
@types.processor
def replace_cmd(lines: typing.Iterator[typing.AnyStr],
                source: typing.Optional[str] = None,
                dest: typing.Optional[str] = None,
                file: typing.Optional = None) -> typing.Iterator[typing.AnyStr]:
    """Replaces all instances of a string or regex pattern in each input"""

    replacements = []

    if source is not None and dest is not None:
        replacements += [(source, dest)]

    if file:
        with open(file, newline='') as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            replacements += list(csv.reader(csvfile, dialect=dialect))

    src, dst, line = '', '', ''
    try:
        for line in lines:
            for src, dst in replacements:
                line = line.replace(src, dst)
            yield line
    except Exception as e:
        click.echo('Could not apply replacement "%s" --> "%s" on line "%s": %s' % (src, dst, line, e), err=True)


@cli.command('filter-pos')
@click.option('-p', '--pos', 'pos', type=str,
              multiple=True, help='Part-of-speech to allow to pass through. Can specify multiple at once.')
@types.processor
def filter_pos_cmd(words: types.Words, pos: typing.List[str]):

    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')

    parts_of_speech = set(pos)
    try:
        for word in words:
            wd, pos_ = nltk.pos_tag([word])[0]
            if pos_ in parts_of_speech:
                yield word
    except Exception as e:
        click.echo('Problem filtering input by part of speech. %s' % e, err=True)


@cli.command('filter-length-gte')
@click.option('-n', '--num', type=int, help='Minimum length that values need to be.')
@types.processor
def filter_max_length_cmd(items: typing.Iterator[typing.AnyStr], num: int):
    try:
        for item in items:
            if len(item) >= num:
                yield item
    except Exception as e:
        click.echo('Problem filtering input for items less than max of (%d). %s' % (num, e), err=True)


@cli.command('remove-stopwords')
@click.option('-f', '--file', type=click.Path(), help='path/to/stopwords/file.txt. One stop-word per line.')
@types.processor
def remove_stopwords(words: types.Words, file: str) -> types.Words:
    try:
        stopwords = set()
        with open(file, 'r') as stopwords_file:
            for line in stopwords_file:
                swds = line.split()
                for sw in swds:
                    stopwords.add(sw.lower().strip())

        for word in words:
            w_lowered = word.lower()
            if w_lowered not in stopwords:
                yield word

    except Exception as e:
        click.echo('Problem removing stopwords from stream of words. %s' % e, err=True)

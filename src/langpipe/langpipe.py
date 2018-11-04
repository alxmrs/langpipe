import typing

import click

from langpipe import types


@click.group(chain=True)
def cli():
    """This script processes a bunch of images through pillow in a unix
    pipe.  One commands feeds into the next.
    Example:
        TBD
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
    for line in lines:
        try:
            click.echo(line)
            yield line
        except Exception as e:
            pass


"""
This conversion script cleans an HTML file generated with latex such that it can be read easier into the
sitescore

Run *htmlcleaner --help* to get the help message:

.. code-block:: text

    usage: htmlcleaner [-h] [--version] [--output_filename STR] [-v] [-vv] [-w] [-f [PATH ...]]
                       [--clear_find_and_replace_defaults]
                       STR [STR ...]

    Cleans html files and removes hyperrefs

    positional arguments:
      STR                   File name of html input

    options:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --output_filename STR
                            File name of output html file
      -v, --verbose         set loglevel to INFO
      -vv, --very-verbose, --debug
                            set loglevel to DEBUG
      -w, --overwrite       Overwrite the input html. Default = False, which means a new html is created withthe suffix
                            _clean
      -f [PATH ...], --find_and_replace [PATH ...]
                        Define a list of key=value pairs to define string patterns you want to replace
      --clear_find_and_replace_defaults
                            Clear the predefined find and replace patterns

"""

import argparse
import logging
import sys
from pathlib import Path

from latexml_html_cleaner import __version__
from latexml_html_cleaner.clean_html import HTMLCleaner

__author__ = "EVLT"
__copyright__ = "EVLT"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from latexml-html-cleaner.skeleton import fib`,
# when using this Python module as a library.

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Cleans html files and removes hyperrefs"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="latexml_html_cleaner {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "filenames", help="File name of html input", type=str, metavar="STR", nargs="+"
    )
    parser.add_argument(
        "--output_filename",
        help="File name of output html file ",
        type=str,
        metavar="STR",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
        default=logging.WARNING,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        "--debug",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-w",
        "--overwrite",
        help="Overwrite the input html. Default = False, which means a new html is created with"
        "the suffix _clean",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-f",
        "--find_and_replace",
        metavar="PATH",
        nargs="*",
        help="Define a list of key=value pairs to define string patterns you want to replace",
    )
    parser.add_argument(
        "--clear_find_and_replace_defaults",
        help="Clear the predefined find and replace patterns",
        action="store_true",
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    if loglevel == logging.DEBUG:
        logformat = "%(levelname)5s: (%(filename)s/%(lineno)d) %(message)s "
    else:
        logformat = "%(levelname)5s: %(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def parse_var(s):
    """
    Parse a key, value pair, separated by '='
    That's the reverse of ShellArgs.

    On the command line (argparse) a declaration will typically look like:
        foo=hello
    or
        foo="hello world"
    """
    items = s.split("=")
    key = items[0].strip()  # we remove blanks around keys, as is logical
    if len(items) > 1:
        # rejoin the rest:
        value = "=".join(items[1:])
    else:
        value = ""
    return key, value


def parse_vars(items):
    """
    Parse a series of key-value pairs and return a dictionary
    """
    d = {}

    if items:
        for item in items:
            key, value = parse_var(item)
            d[key] = value
    return d


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    if args.find_and_replace is not None:
        find_and_replace_patterns = parse_vars(args.find_and_replace)
    else:
        find_and_replace_patterns = None

    _logger.debug("Starting clean html...")
    for fn in args.filenames:
        filename = Path(fn)
        if filename == Path("."):
            _logger.debug(f"Skipping file {fn}. It is the current folder.")
        elif filename.suffix != ".html":
            _logger.warning(f"Skipping file {fn}. It is not an html")
        else:
            _logger.debug(f"Cleaning file {filename}...")
            HTMLCleaner(
                filename=filename,
                overwrite=args.overwrite,
                find_and_replace_patterns=find_and_replace_patterns,
                clear_default_patterns=args.clear_find_and_replace_defaults,
                output_filename=args.output_filename,
            )
    _logger.debug("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m latexml-html-cleaner.skeleton 42
    #
    run()

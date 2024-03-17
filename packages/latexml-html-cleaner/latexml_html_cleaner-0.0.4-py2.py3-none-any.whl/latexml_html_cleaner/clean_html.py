"""
Class definition of htmlcleaner
"""

import logging
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

_logger = logging.getLogger(__name__)
import contextlib


@contextlib.contextmanager
def smart_open(filename=None):
    """
    Context manager for a smart file opener for reading from file or standard input

    Args:
        filename (Path): Path to the file to open

    Return:
        file: file-like object
    """
    if filename and filename.as_posix() != "-":
        fh = open(filename, mode="w", encoding="utf-8")
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()


def to_lijst(values):
    """Convert a string or a list of strings to a list of strings"""
    if not isinstance(values, list):
        lijst_values = [values]
    else:
        lijst_values = values
    return lijst_values


class HTMLCleaner:
    """
    Class to clean the contents of an html-file

    Args:
        filename (Path): path to the html-file to clean
        skip_tags (bool, optional): do not use the default tags
        overwrite (bool, optional): overwrite the existing file if it exists
        find_and_replace_patterns: (dict, optional): replace these patterns
        clear_default_patterns (bool, optional): clear the default patterns if they exist
        output_filename (Path, optional): filename to write too. If not given, base the name on the input file

    Attributes:
        clean_soup (BeautifulSoup): BeautifulSoup object

    Notes:
        * By default, all attributes starting with ltx are skipped.
        * With ```skip_tags``` we can drop entire ```<>``` environments based on the environments name (the key of
          the dict) and then a list of attributes key/values pairs.
        * If such a key/value pair occurs, the entire ```<>``` tag is discarded.
        * We first define a default list in this example: a tag
          ```<span class="ltx_bibblock ltx_bib_cited">Cited by etc. </span>```
          is discarded in its entirely, including all nested values.
        * We can also specify the values of a key/value pair in a list if there are more than one tags have the same
          key names, but different values.
    """

    def __init__(
        self,
        filename,
        skip_tags=None,
        overwrite=False,
        find_and_replace_patterns=None,
        clear_default_patterns=False,
        output_filename=None,
    ):
        """
        Constructor for HTMLCleaner
        """
        self.filename = Path(filename)
        self.clean_soup = None
        _logger.debug(f"Make filename for {filename}")
        file_basename = self.filename.with_suffix("")
        if not overwrite:
            file_basename = Path("_".join([file_basename.as_posix(), "clean"]))
        if output_filename is None:
            self.output_file = file_basename.with_suffix(".html")
        else:
            self.output_file = Path(output_filename)
        _logger.debug(f"Cleaning from {filename} to {self.output_file}")

        # Default find en place. Always remove all double white lines
        if clear_default_patterns:
            self.find_and_replace_patterns = {}
        else:
            # Start with some default strings that we are going to delete
            self.find_and_replace_patterns = {
                "\n{2,}": "\n\n",
                "<span>•</span>": "",
                "<span><span>–</span></span>": "",
                "title=": "<b>Intermezzo:</b> ",
                "Â": "",
            }

        if find_and_replace_patterns is not None:
            for find, replace in find_and_replace_patterns.items():
                self.find_and_replace_patterns[find] = replace

        if skip_tags is None:
            self.skip_tags = {
                "span": {
                    "class": ["ltx_bibblock ltx_bib_cited", "ltx_tag ltx_tag_item"]
                },
                "link": {"rel": None},
                "meta": {"content": None},
                "div": {"class": "ltx_dates"},
                "footer": {None: None},
                "header": {None: None},
            }
        else:
            self.skip_tags = skip_tags

        self.skip_tag_attributes = {
            "a": {
                "href": ["^(A|Ch)\d+.html$", ".*[\d\w\.%]#[\d\w\.%].*", "^#.*"],
                "title": "",
            },
            "li": {"style": None},
            "span": {"style": None},
            None: {None: "ltx_", "id": None},
        }

        self.clean_html()

    def clean_html(self):
        """
        Read the html file and clean the html code

        """

        with open(file=self.filename, encoding="utf-8") as stream:
            html = stream.read()
        soup = BeautifulSoup(html, "html.parser")
        _logger.debug(f"Start cleaning ")
        _logger.debug(soup)

        # Remove all attributes starting with ltx (which are latexml definitions)
        for tags in soup.findAll(True):
            new_attrs = {}
            for attr_key, attr_value in tags.attrs.items():
                attributes = to_lijst(attr_value)

                skip_this = skip_this_tag(
                    tag=tags,
                    attribute_key=attr_key,
                    attribute_values=attributes,
                    skip_tags=self.skip_tags,
                    combined=True,
                )
                if skip_this:
                    # This tag is skipped entirely
                    _logger.debug(f"Dropping complete tag  {attr_key} {attr_value}")
                    tags.extract()
                    continue

                skip_this = skip_this_tag(
                    tag=tags,
                    attribute_key=attr_key,
                    attribute_values=attributes,
                    skip_tags=self.skip_tag_attributes,
                )

                # We collected the attributes in skip_this. Now remove it from the
                # attributes of the current tag

                # av are the current attributes of our tag
                av = set(attributes)
                try:
                    sv = set(skip_this[attr_key])
                except KeyError:
                    sv = {}
                # sv contains the tags we want to remove. Subtract this from the current one
                new_attrs_values = av.difference(sv)
                if new_attrs_values:
                    # als we nog attributes over houden stoppen we deze in de nieuwe attributes
                    new_attrs[attr_key] = list(new_attrs_values)
                else:
                    # we have nothing left so, we can omit this attr key
                    _logger.debug(f"Dropping {attr_key} from {tags.name}")

            # Overwrite the old attributes with our new ones
            tags.attrs = new_attrs

        # Here we can still remove elements based on normal string matches
        self.clean_soup = str(soup)
        for find, replace in self.find_and_replace_patterns.items():
            _logger.debug(f"replacing {find} with {replace}")
            self.clean_soup = re.sub(find, replace, self.clean_soup)

        _logger.info(f"Cleaning: {self.filename} -> {self.output_file}")

        with smart_open(self.output_file) as stream:
            stream.write(self.clean_soup)


def skip_this_tag(tag, attribute_key, attribute_values, skip_tags, combined=False):
    """
    Collect all the tags and attributes we want to remove

    Args:
        tag (object):  beautiful soup tag to clean
        attribute_key (str): key of the attribute
        attribute_values (list): values of the attribute
        skip_tags (bool): skip the tag if true
        combined (bool, optional): only remove the tag in case we match the combined tag

    Returns:
        list: all the tags and attributes to skip
    """
    attributes = " ".join(attribute_values)
    tags_to_skip = {}
    for skip_tag_name, skip_tag_attributes in skip_tags.items():
        if skip_tag_name == tag.name or skip_tag_name is None:
            for skip_atr_key, skip_atr_value in skip_tag_attributes.items():
                if skip_atr_key == attribute_key or skip_atr_key is None:
                    for skip_value in to_lijst(skip_atr_value):
                        if combined:
                            # If combined is true then your match must apply to the combined
                            # attr string, such as 'ltx_bibblock ltx_bib_cited'
                            if skip_value is None or skip_value == attributes:
                                tags_to_skip[attribute_key] = attribute_values
                        else:
                            # If combined is not true, we get or per item in the list
                            # there is a match based on a regular expression. All matches
                            # are deleted
                            for av in attribute_values:
                                try:
                                    add = (
                                        av is None
                                        or skip_value is None
                                        or re.match(skip_value, av) is not None
                                    )
                                except TypeError:
                                    _logger.warning(
                                        f"Failed to do regular expression for {skip_value}"
                                    )
                                else:
                                    if add:
                                        try:
                                            tags_to_skip[attribute_key].append(av)
                                        except KeyError:
                                            tags_to_skip[attribute_key] = [av]
    return tags_to_skip

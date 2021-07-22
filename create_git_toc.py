#!/usr/bin/env python

import argparse
import os
import re

def convert_to_toc_link(header_string):
    """
    Convert a given header string to a string, which can be used as link to this header
    inside a table of content in Git.

    @param header_string: header string to be converted to a table of content link
    @return a string representing a link to the header string in the table of content
    """
    # reduce number of # in the beginning to 1
    toc_link = re.sub(r'^(\#)\1+', r'\1', header_string)

    # remove any space after the # in the beginning
    toc_link = toc_link.replace(' ', '', 1) if toc_link[1] == ' ' else toc_link

    # replace space by -
    toc_link = toc_link.replace(' ', '-')

    # convert upper-case to lower-case letters
    toc_link = toc_link.lower()

    # remove dots
    toc_link = toc_link.replace('.', '')

    return toc_link

def convert_to_toc_name(header_string):
    """
    Convert a given header string to a string, which can be used as name to this header
    inside a table of content in Git.

    @param header_string: header string to be converted to a table of content name
    @return a string representing a name in the table of content
    """
    # remove all # in the beginning
    toc_name = re.sub(r'^(\#)\1*', r'', header_string)

    # remove any starting space
    toc_name = toc_name.strip()

    return toc_name

def get_toc_components_of_markdown_file(md_file):
    """
    Read through the given markdown-file and extract all relevant components to be used
    in a table of content, i.e. all headers.

    @param md_file: markdown-file where the table of content information is extracted
    @return an array of tuples representing the table of content, each tuple consists
            of the converted markdown-format of a header together with its depth-level
            in the table of content.
    """
    if not os.path.isfile(md_file):
        print("[!] '{}' is not a valid file..".format(md_file))
        return

    toc_array = []

    with open(md_file, 'r') as file:
        for line in file.readlines():
            # headers to be included in a table of content start with a single or several '#'
            if line.startswith('#'):
                header_string = line.strip()
                toc_format = '[{}]({})'.format(convert_to_toc_name(header_string),
                                               convert_to_toc_link(header_string))
                toc_depth = len(re.findall(r'^\#+', header_string)[0]) -1 # start from depth 0

                toc_array.append((toc_format, toc_depth))

    return toc_array

def create_toc(toc_array, max_depth):
    """
    Use a table of content structure to create a markdown-formatted overview, which looks as
    following:
    * [Header0](#header0)
    * [Header1](#header1)
        * [Header1.1](#header11)
            * [Header1.1.1](#header111)
        * [Header1.2](#header12)

    @param toc_array: table of content structure (obtainted by calling get_toc_components_of_markdown_file),
                      which should be formatted
    @param max_depth: maximal depth-level (starting at 0), which should be visible in the overview
    @return a string holding the markdown-formatted table of content
    """
    toc = ''

    for (toc_format, toc_depth) in toc_array:
        if toc_depth > max_depth:
            continue

        toc += ' ' * (toc_depth * 4) # depth of toc component
        toc += '* ' # enumeration type
        toc += toc_format
        toc += '\n'

    return toc.strip() # remove last added '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Github Table of Content Helper')
    parser.add_argument('--md_file', default='.', type=str, required=True, help='Provide the path to the markdown-file where to extract the table of content information from, e.g. \'git_dir/README.md\'')
    parser.add_argument('--max_depth', default=3, type=int, help='Provide the maximal depth-level which should be displayed in the table of content (starting at 0), default value is 3')
    parsed_env = parser.parse_args()

    toc_components = get_toc_components_of_markdown_file(parsed_env.md_file)
    toc_format = create_toc(toc_components, parsed_env.max_depth)

    print('====================================================================================================================')
    print('========================================== Github Table of Content Helper ==========================================')
    print('====================================================================================================================')
    print('Copy following output into your markdown file \'{}\', where the table of content should be displayed:'.format(parsed_env.md_file))
    print('')
    print(toc_format)
    print('')
    print('====================================================================================================================')

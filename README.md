# Create a table of content out of a markdown sheet
Struggling and finding it annoying to create a table of content for a markdown file manually, I decided to let a script do the work for me.
The Python script _create_git_toc.py_ scans a markdown file (e.g. README.md) for all headers (denoted by a leading '_#_') and generates a table of content out of it. 

## How to use it?
Simply call the script and provide the path to the markdown file where the table of content should be generated for (an optional depth-level can be provided, too):
```sh
python create_git_toc.py --md_file <path to my markdown file> [--max_depth <maximal depth-level>]
```
The _depth-level_ defines the number of 'sub'-headers which should be included in the table of content, default value is 3.

## How does it work?
The script scans the given markdown file for all available headers (which are denoted by leading '_#_'). The header text will be used as name which is displayed in the table of content. Together with the name, link to the respective section is generated which needs to fulfill following conditions:  
- one leading '_#_'
- directly following the name of the header in lower-case letters
- spaces are replaced by '_-_'
- dots are removed

## Example
Let's take a file called _toc_example.md_ with following content (this file is also available in the _example/_ directory):
```markdown
# Table of content example
Some meaningful text here..

## Header in level 1
Text, text, text

### Header in level 1.2
More text..

## Another Header in level 1
Text, text, text
```

Invoking the script with ```python create_git_toc.py --md_file example/toc_example.md``` produces following output:
```markdown
* [Table of content example](#table-of-content-example)
    * [Header in level 1](#header-in-level-1)
        * [Header in level 1.2](#header-in-level-12)
    * [Another Header in level 1](#another-header-in-level-1)
```
See _toc_example_with_toc.md_ in the _example/_ directory for how it could look like.

Reducing the depth-level to 1 by invoking the script with ```python create_git_toc.py --md_file example/toc_example.md --max_depth 2``` produces following output:
```markdown
* [Table of content example](#table-of-content-example)
    * [Header in level 1](#header-in-level-1)
    * [Another Header in level 1](#another-header-in-level-1)
```

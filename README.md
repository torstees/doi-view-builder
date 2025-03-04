# doi-view-builder
This script will build a simple DOI Viewer HTML file based on the contents of a DOI JSON file. 

# Basic Installation
The following command will install/update the newest version of the script. 

```bash
pip install --force-reinstall --no-cache-dir git+https://github.com/torstees/doi-view-builder

or for developers working on the script itself,
pip install -e .
```

# Usage
*script name:* doi_view_builder 

As always, running the script, doi_view_builder with the "-h" argument will display the appropriate help:

```bash
$ doi_view_builder -h
usage: doi_view_builder [-h] files [files ...]

Creates HTML file for viewing DOI

positional arguments:
  files       JSON DOI files for HTML viewing

options:
  -h, --help  show this help message and exit
```

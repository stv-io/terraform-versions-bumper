# terraform-versions-bumper

A simple script which aims to help the upkeep of versions in terraform modules

## Usage

```console
usage: terraform-versions-bumper [-h] [--dry-run] [--backup] [--display] [--debug]

Bump terraform required versions and provider versions to latest releases

options:
  -h, --help     show this help message and exit
  --dry-run, -r  Dry run, don't modify files
  --backup, -b   create backup files with a suffix
  --display, -p  display the files generated
  --debug, -d    display matched files and contents
```

## Install

```console
pip install git+https://git@github.com/stv-io/terraform-versions-bumper.git
```

## TODO

- tests, provide a few test scenarios
- Dockerfile
- recursive and directories
- add support for terraform modules

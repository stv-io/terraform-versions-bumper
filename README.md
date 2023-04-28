# terraform-versions-bumper

A simple script which aims to help the upkeep of the required terraform version, as well as the provider versions. The idea behind the script is to make it a single command to update the terraform version to a recent one, as well as the provider versions.

Only works with the public [terraform registry](https://registry.terraform.io/)

## Usage

```console
usage: terraform-versions-bumper [-h] [--backup] [--display] [--debug]

Bump terraform required versions and provider versions to latest releases

options:
  -h, --help     show this help message and exit
  --backup, -b   create backup files with extenstion .bkp
  --display, -p  display the files generated
  --debug, -d    debug level verbosity
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

## Similar (and better) projects

- <https://github.com/keilerkonzept/terraform-module-versions>
- <https://github.com/tfverch/tfvc>

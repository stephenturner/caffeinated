# coffeetime

[![PyPI](https://img.shields.io/pypi/v/coffeetime.svg)](https://pypi.org/project/coffeetime/)
[![Changelog](https://img.shields.io/github/v/release/stephenturner/coffeetime?include_prereleases&label=changelog)](https://github.com/stephenturner/coffeetime/releases)
[![Tests](https://github.com/stephenturner/coffeetime/actions/workflows/test.yml/badge.svg)](https://github.com/stephenturner/coffeetime/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-GPL%203-blue.svg)](https://github.com/stephenturner/coffeetime/blob/master/LICENSE)

Provide statistics about your caffeine level specifically when you'd be going to bed.

## Installation

Install this tool using `pip`:

```bash
pip install coffeetime
```
## Usage

For help, run:

```bash
coffeetime --help
```

You can also use:

```bash
python -m coffeetime --help
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

```bash
cd coffeetime
python -m venv venv
source venv/bin/activate
```

Now install the dependencies and test dependencies:

```bash
pip install -e '.[test]'
```

To run the tests:

```bash
python -m pytest
```

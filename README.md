# caffeinated

[![PyPI](https://img.shields.io/pypi/v/caffeinated.svg)](https://pypi.org/project/caffeinated/)
[![Changelog](https://img.shields.io/github/v/release/stephenturner/caffeinated?include_prereleases&label=changelog)](https://github.com/stephenturner/caffeinated/releases)
[![Tests](https://github.com/stephenturner/caffeinated/actions/workflows/test.yml/badge.svg)](https://github.com/stephenturner/caffeinated/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-GPL%203-blue.svg)](https://github.com/stephenturner/caffeinated/blob/master/LICENSE)

Provide statistics about your caffeine level specifically when you'd be going to bed. This package was inspired by [coffee-o-clock](https://github.com/Eliya-G/coffee-o-clock).

The formula used for calculating the amount of caffeine remaining in your system is:

$$
N(t) = N_0 \left( \frac{1}{2} \right)^{\frac{t}{t_6}}
$$

Where:

- $N(t)$ = Quantity of caffeine remaining  
- $N_0$ = Original amount of caffeine  
- $t$ = Time  
- $t_6$ = Coffee's half-life (6 hours)

## Installation

Install this tool using `pip`:

```bash
pip install caffeinated
```
## Usage

For help, run:

```bash
caffeinated --help
```

Example usage:

```bash
caffeinated --caffeine 200 --bedtime 9pm
```

```
You would have 50.0mg of caffeine in your system if you went to bed at 9:00pm (in 12.0 hours).
That's like having 56% of a cup of coffee before bed.
```

You can also specify the time you're starting to consume caffeine. Both bedtime and start time can be specified in 12-hour or 24-hour format.

```bash
caffeinated --caffeine 200 --bedtime 2100 --start-time 0600
```

```
You would have 35.4mg of caffeine in your system if you went to bed at 9:00pm (in 15.0 hours).
That's like having 39% of a cup of coffee before bed.
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

```bash
cd caffeinated
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

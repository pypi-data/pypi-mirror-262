# DITA File Merger and Splitter Utility

This utility is designed to merge multiple DITA files into single XML files and split merged XML files back into
individual DITA files. This facilitates easier handling and translation of large sets of DITA documents.

## Table of Contents

- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Usage](#usage)
- [Running the Tests](#running-the-tests)

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and
testing purposes.

### Prerequisites

- Python 3.12 or newer

### Installation

You can install the `dita-parser` package directly from PyPI using pip:

```bash
pip install dita-parser
```

If you want to contribute to the project or modify it, you can clone the repository to your local machine:

1. Clone the repository to your local machine:

```
git clone git@git.crosslang.dev:crosslang/dita_parser.git
```

2. Navigate to the project dir:

```
cd dita_parser
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

### Usage

Print help:

```
python src/app.py -h
```

To merge DITA files:

```
python src/app.py merge path/to/input path/to/output
```

To split XML files:

```
python src/app.py split path/to/input path/to/output
```

### Running the Tests

Navigate to the tests directory and run the unittest module:

```
cd tests
python -m unittest
```


Within the root of your project in the terminal type: `./start.sh` 🙏

# Refactor code after deployment

- write some tests
- create modules within a `coininfo` directory that make logical sense or are modular
- adjust tests accordingly (create a `tests` folder in the root from which to test)
- change version numbers when code is changed

## Extra ideas

- Adapt and use another name for the module if you choose (😈)

## Installation

`pip install setuptools wheel twine`

## Commonly used commands

Build distribution files:

`python setup.py sdist bdist_wheel`

Upload to Pypi

`twine upload dist/*`

# Tests for Linux `cp` command

## Task
Using the Python language write code to test the functionality of “cp” Linux
command.

This might be raw python code, but using of some test frameworks would be a
plus.

## Notes
The `cp` command has an extended list op options including their combination.
This testing repo contains a small subset of them and has an ability to extend
over time.

Only few simple flags were tested here just to demonstrate the testing approach.

## Installation

This repo is a try to get more familiar with the poetry. To run poetry locally
follow [installation instructions](https://python-poetry.org/docs/#installation).

### How to run code from here:

1. Clone this repo.
```
git clone https://github.com/aborovyi/test_linux_cp.git
```

2. Install project dependenicies:
```
poetry install
```

3. Grant user to run chattr command w/o password, to execute chattr tests

```
sudo /bin/bash -c "echo $(whoami) ALL=NOPASSWD: $(which chattr) >> /etc/sudoers"
```

4. Run tests:
```
poetry run pytest
```

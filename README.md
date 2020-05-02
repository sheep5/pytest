
# pytest

pytest is a simple Python-based program tester. It is aimed towards testing executable files that accepts an input from `stdin` and produces output to `stdout`.

## Getting Started

### Prerequisites

pytest requires the following Python libraries to work properly:
- [PyYAML](https://pypi.org/project/PyYAML/)
- [termcolor](https://pypi.org/project/termcolor/)

They can be manually installed using `pip`.  
Alternatively, pytest will automatically install them during installation.

### Installation

1. Clone this repo however you'd like.
  ```bash
  git clone https://github.com/sheep5/pytest.git
  ```

  ```bash
  curl -sL https://github.com/sheep5/pytest/archive/master.zip `
  ```

  ```bash
  wget https://github.com/sheep5/pytest/archive/master.zip
  ```

2. Install via `pip`.
  ```bash
  pip install master.zip
  ```

## Usage

### Making a valid YAML tests file
pytest runs on a YAML file that contains tests. The test file is composed of commands along with their arguments.

#### Supported Commands

| Command | Description |
| :--- | :--- |
| `description` | describes the test; printed in test results if present |
| `run`* | CLI command to run |
| `stdin` | what keyboard input to simulate |
| `stdout`* | what `run` should output to stdout |
| `exit` | what exit code `run` should exit with (defaults to `0`) |
| `timeout` | how many seconds `run` is allowed to execute (defaults to `2`) |
| `shell` | enable shell functions for `run` execution (defaults to `False`) |

\* required

#### Sample

```yaml
pytest:
  tests:
    hello:
      description: Correctly prints “hello world”
      run: ./hello
      stdout: Hello, world!\n
    multiline hello:
      description: Correctly prints multiline hello world
      run: ./hello_multiline
      stdout: |
        Hello,
        world!
```

### Running pytest

pytest is called from the command-line using the following form:

```bash
python pytest [-f FILENAME] [-d] [-l] [-t TARGET] [-v] [-h]
```

Where the following options are understood:

- `-f FILENAME`, `--filename=FILENAME`
  specify the name of a test file (defaults to tests.yaml)

- `-d`, `--dev`
  run pytest in development mode (implies `--verbose`)
  
- `-l`, `--log`
  display tests' raw execution log (`stdin`, `stdout`, `exitcode`, etc.)

- `-t TARGET`, `--target TARGET`
  target a specific test to run

- `-v`, `--verbose`
  display full tracebacks of any errors (also implies `--log`)

- `-h`, `--help`
  prints a short usage message and exits

## Acknowledgements

- [check50](https://github.com/cs50/check50)
  main inspiration of this project (both idea-wise and code-wise)

- [r/learnpython](https://www.reddit.com/r/learnpython/)
  people on this sub write very nice answers to coding questions

- [Stack Overflow](https://stackoverflow.com/)
  pretty much taught me everything I didn't know about Python along the duration of this project


"""
Functions that pertain to loading tests from valid YAML files.
"""

""" Python library imports """
import yaml, re
from pathlib import Path

""" Constant declarations """
APPLICATION_NAME = "pytest"
TEST_CONTAINER = "tests"
SUPPORTED_COMMANDS = {"description", "run", "stdin", "stdout", "exit", "timeout", "shell"}
REQUIRED_COMMANDS = {"run", "stdout"}

""" Object declarations """
class Test:
    # Import runner functions
    from runner import execute

    def __init__(self, name, commands):
        ALLOWED_ATTRIBUTES = {"name"}
        ALLOWED_ATTRIBUTES.update(SUPPORTED_COMMANDS)
        
        # Initialize all allowed attributes to None
        self.__dict__.update((attr, None) for attr in ALLOWED_ATTRIBUTES)
                
        # Update attributes by given values
        self.name = name
        self.__dict__.update((attr, val) for attr, val in commands.items()
                                         if attr in ALLOWED_ATTRIBUTES)


""" Function declarations. """
def compile_tests(filename, target=None):
    """
    Compiles a given file into Test objects.
    Returns a list of Test objects if present, or None otherwise.
    """
    test_list = []
    
    # Read tests in file
    unparsed_tests = read(filename)
    
    # Check if any targets are specified
    if target is not None:
        # Parse targeted test
        parsed_test = parse(target, unparsed_tests[target])
        test_list.append(Test(parsed_test["name"], parsed_test["commands"]))
    else: 
        # Parse all tests
        for test in unparsed_tests:
            parsed_test = parse(test, unparsed_tests[test])
            test_list.append(Test(parsed_test["name"], parsed_test["commands"]))
    
    if test_list:
        return test_list
    else:
        return None

def read(filename):
    """
    Reads and verifies that given file is a valid test file.
    Returns tests from file as a dictionary if present, or None otherwise.
    """
    
    # Check if file is a YAML file
    if (Path(filename).suffix.lower() not in [".yaml", ".yml"]):
        raise InvalidFile(f"{filename} is not a valid YAML file.")

    # Read file contents into memory
    with open(filename) as f:
        contents = yaml.safe_load(f)
    
    # Check if file is a valid test file
    if (not (contents.get(APPLICATION_NAME) and
             contents[APPLICATION_NAME].get(TEST_CONTAINER))):
        raise InvalidFile(f"{filename} is not a valid {APPLICATION_NAME} file.")
    
    return contents.get(APPLICATION_NAME).get(TEST_CONTAINER)

""" Parser functions for each valid command. """
def _description(arg):
    return str(arg)

def _run(arg):
    # Split arguments into a list of strings
    return arg.split(' ')

def _stdin(arg):
    return str(arg)

def _stdout(arg):
    return str(arg)

def _exit(arg):
    # Add default exit value if unspecified
    if arg is None:
        return 0
    
    # Check if arg is an integer
    try:
        assert type(arg) is int
    except AssertionError:
        raise InvalidArgument(f"exit command only accepts integers, not {arg}")
    
    return arg

def _timeout(arg):
    # Add default timeout if unspecified
    if arg is None:
        return 2

    # Check if arg is an integer
    try:
        assert type(arg) == int
    except AssertionError:
        raise InvalidArgument(f"timeout command only accepts integers, not {arg}")
    
    return arg
    

def _shell(arg):
    # Add default shell value if unspecified
    if arg is None:
        return False
    
    return bool(arg)


COMMANDS = {"description": _description,
            "run": _run, "stdin": _stdin, "stdout": _stdout, "exit": _exit, "timeout": _timeout, "shell": _shell}

def parse(name, commands):
    """
    Receives and parses a test.
    Returns parsed test's name and dictionary of commands.
    """ 
    # Check if test name is valid
    if not re.match("\w+", name):
        raise ParseError(f"{name} is not a valid name for a test; test names should consist only of alphanumeric characters, underscores, and spaces")
         
    # Allow test names to contain spaces and hyphens, but replace them with underscores
    name = name.replace(' ', '_').replace('-', '_')
        
    # Allow test names to begin with a number by prepending them with underscores
    if name[0].isdigit():
        name = f"_{name}"
        
    # Validate test
    validate(name, commands)

    # Append commands with no args if unspecified
    if "exit" not in commands:
        commands["exit"] = None
    if "timeout" not in commands:
        commands["timeout"] = None
    if "shell" not in commands:
        commands["shell"] = None

    # Parse each command
    parsed_commands = {}
    for command in commands:
        args = commands.get(command)
        parsed_commands[command] = COMMANDS[command](args)
    
    return {"name": name, "commands": parsed_commands}

def validate(name, test):
    """
    Receives and validates a test.
    """
    # Verifies that all supplied commands are valid
    for command in test:
        if command not in SUPPORTED_COMMANDS:
            raise UnsupportedCommand(f"{command} is not a valid command in test {name}, use only: {SUPPORTED_COMMANDS}")
        
    # Verifies that all required commands are supplied
    for required_command in REQUIRED_COMMANDS:
        if required_command not in test:
            raise MissingCommand(f"Missing {required_command} in test {name}")

    return None


"""
Exception declarations.
"""
class CompileError(Exception):
    pass

class ReadError(CompileError):
    pass
class InvalidFile(ReadError):
    pass

class ValidateError(CompileError):
    pass
class UnsupportedCommand(ValidateError):
    pass
class MissingCommand(ValidateError):
    pass

class ParseError(CompileError):
    pass
class InvalidArgument(ParseError):
    pass

class LoadError(CompileError):
    pass

class NotEnoughParameters(Exception):
    pass

if __name__ == "__main__":
    tests = compile_tests("test.yaml")
    for test in tests:
        # Print test details
        print(f"Test name: {test.name}")
        [print(f"{key}: {val}")
         for key, val in test.__dict__.items()
         if key != "name"]
        print()

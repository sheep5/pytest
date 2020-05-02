""" Python library imports """
import argparse
import sys

""" Module imports """
from parser import *
from runner import *
from renderer import *

""" Constant declarations """
APPLICATION_NAME = "pytest"
DEFAULT_FILENAME = "tests.yaml"

""" Function declarations """
def exception_handler(exception_type, exception, traceback, except_hook=sys.excepthook):
    if exception_handler.verbose:
        # Print full exception with traceback
        except_hook(exception_type, exception, traceback)
    else:
        # Simplify printing of exceptions
        print(f"{exception_type.__name__}: {exception}")

    sys.exit(1)

# Assume that we should print tracebacks until we get command line arguments
exception_handler.verbose = True
sys.excepthook = exception_handler


""" Main body of code """
def main():
    # Define valid command line arguments
    parser = argparse.ArgumentParser(prog=APPLICATION_NAME)
    
    parser.add_argument("-f", "--filename",
                        action="store",
                        nargs="?",
                        default=DEFAULT_FILENAME,
                        type=str,
                        help=f"specify name of a test file (defaults to {DEFAULT_FILENAME})")
    parser.add_argument("-d", "--dev",
                        action="store_true",
                        help=f"run {APPLICATION_NAME} in development mode (implies --verbose)")
    parser.add_argument("-l", "--log",
                        action="store_true",
                        help="display tests' raw execution log")
    parser.add_argument("-t", "--target",
                        action="store",
                        nargs="?",
                        default=None,
                        help="target a specific test to run")
    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="display full tracebacks of any errors (also implies --log)")

    # Parse command line arguments
    args = parser.parse_args()
    
    # Set implied flags
    if args.dev:
        args.verbose = True

    if args.verbose:
        args.log = True
     
    # Set exception handler attributes
    exception_handler.verbose = args.verbose
    
    test_results = []
    
    # Compile tests
    if args.target is not None:
        args.target = ' '.join(args.target)
    tests = compile_tests(args.filename, target=args.target)
    
    # Check if compiling target yields any results
    if tests is None:
       raise CompileError(f"No tests compiled with target {args.target}")

    # Execute and store test results
    for test in tests:
        test_results.append(TestResult().from_test(test))
    

    # Render test results
    print(to_ansi(test_results, log=args.log))
    
    return 0

if __name__ == "__main__":
    main()

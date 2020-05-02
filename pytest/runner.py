""" Python library imports """
import subprocess
import timeit

""" Test class methods """
def execute(self):
    try:
        result = subprocess.run(args=self.run,
                                input=self.stdin,
                                capture_output=True,
                                timeout=self.timeout,
                                check=True,
                                text=True,
                                shell=self.shell)
    except subprocess.TimeoutExpired as exception:
        result = exception
    except subprocess.CalledProcessError as exception:
        result = exception

    # Replace all special characters in output with string literals
    result_dict = result.__dict__
    for key in {"output", "stderr", "stdout"}:
        if result_dict.get(key) is not None:
            result_dict[key] = str(result_dict[key]).replace("\n", r"\n").replace("\t", r"\t").replace('"', '\"')
    
    return result


""" Class declarations """
class TestResult: 
    def __init__(self):
        ALLOWED_ATTRIBUTES = {"name", "description", "passed", "cause", "log"}
        
        # Initialize all allowed attributes to None
        self.__dict__.update((attr, None) for attr in ALLOWED_ATTRIBUTES)

    def from_test(self, test_obj):
        """ Possible objects that are returned after a test execution. """
        def _CompletedProcess(result_dict):
            # Check if test is passed
            if ((result_dict["stderr"] == '') and
                (result_dict["stdout"] == test_obj.stdout)):
                self.passed = True
                self.cause = f"produced expected output {test_obj.stdout}"
            else:
                self.passed = False
                self.cause = f"output {result_dict['stdout']}; expected {test_obj.stdout}"
            
        def _CalledProcessError(result_dict):
            self.cause = f"interrupted with error {result_dict['stderr']}"

        def _TimeoutExpired(result_dict):
            self.cause = f"timed out after {result_dict['timeout']} seconds"

        RESULTS = {subprocess.CompletedProcess: _CompletedProcess,
                   subprocess.CalledProcessError: _CalledProcessError,
                   subprocess.TimeoutExpired: _TimeoutExpired}

        test_result = test_obj.execute()
        result_dict = test_result.__dict__
        
        # Set basic information
        self.name = test_obj.name
        self.description = test_obj.description
        self.log = result_dict
        
        # Process result based on return object type
        RESULTS.get(type(test_result))(result_dict)

        return self

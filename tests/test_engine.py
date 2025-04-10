class TestResult:
    def __init__(self, test_name: str, result: bool, failures = None):
        self.test_name = test_name
        self.result = result
        self.failures = failures

class Test:
    def __init__(self, name: str, test=None):
        self.name = name
        self.test = test
        self.completion = 0 
        
    def run(self) -> TestResult:
        return self.test(self.name, self.set_completion, self.print_status)
    
    def set_completion(self, n):
        self.completion = n
    
    def print_status(self):
        if self.completion == 100:
            print(f"{self.name} -> |{self.completion * '='}{(100-self.completion) * '-'}| {self.completion}%")
        else:
            print(f"{self.name} -> |{self.completion * '='}{(100-self.completion) * '-'}| {self.completion}%\r", end=r"", flush=True)

    
class Tester:
    def __init__(self):
        self.tests = []
    
    def run_tests(self):
        print("Testing Started")
        results = []
        for test in self.tests:
            results.append(test.run())
            
        self.print_final_results(results)
    
    def add_test(self, test: Test):
        self.tests.append(test)
        
    def print_final_results(self, results: list[TestResult]):
        fail_count = 0
        for test in results:
            if test.result == False:
                fail_count += 1
                print(f"Test failed: {test.test_name}")
                for failure in test.failures:
                    print(f"\t{failure}")
                    
        print(f"Success: {len(results)-fail_count} Failed: {fail_count}")
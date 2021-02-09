#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

from enum import Enum

from cybld import cybld_helpers

# --------------------------------------------------------------------------

class CyBldRunnerResultType(Enum):
    unknown = 1
    success = 2
    fail    = 3

# --------------------------------------------------------------------------

class CyBldRunnerSingleResult:

    def __init__(self, command, param):
        self.result  = CyBldRunnerResultType.unknown
        self.command = command
        self.param   = param
        self.runtime = 0

    def set_result(self, result: CyBldRunnerResultType, runtime: int):
        self.result  = result
        self.runtime = runtime

    def get_param(self):
        return self.param

    def is_success(self):
        return self.result == CyBldRunnerResultType.success

    def is_fail(self):
        return self.result == CyBldRunnerResultType.fail

# --------------------------------------------------------------------------

class CyBldRunnerResults:

    def __init__(self):
        self.previous_results = []
        self.current_results  = []

    def add_result(self, result: CyBldRunnerSingleResult):
        """
        Add the result to the current_results list.

        :param result: The result to add
        :type result: CyBldRunnerSingleResult
        """
        self.current_results.append(result)

    def finish(self):
        self.previous_results = self.current_results
        self.current_results  = []

    def print_results(self):
        for result in self.current_results:
            if result.is_success():
                cybld_helpers.print_text_with_bg(result.get_param(), True)
            elif result.is_fail():
                cybld_helpers.print_text_with_bg(result.get_param(), False)
            else:
                cybld_helpers.print_text_with_bg(result.get_param(), None)

    def print_comparison(self):
        if len(self.current_results) == 0:
            return
        if len(self.current_results) > 0 and len(self.previous_results) == 0:
            return

        new_good_tests = []
        new_bad_tests  = []

        cybld_helpers.print_seperator_lines(1)
        cybld_helpers.print_centered_text("PREVIOUS TEST RESULTS", None)

        for result_iter in self.current_results:
            previous_result = CyBldRunnerResultType.unknown
            for prev_result_iter in self.previous_results:
                if prev_result_iter.get_param() == result_iter.get_param():
                    if prev_result_iter.is_success():
                        previous_result = CyBldRunnerResultType.success
                    elif prev_result_iter.is_fail():
                        previous_result = CyBldRunnerResultType.fail

            if (result_iter.is_success() and previous_result == CyBldRunnerResultType.fail):
                new_good_tests.append(result_iter.get_param())
            elif (result_iter.is_fail() and previous_result == CyBldRunnerResultType.success):
                new_bad_tests.append(result_iter.get_param())

        if len(new_good_tests) == 0 and len(new_bad_tests) == 0:
            cybld_helpers.print_centered_text("No changes detected", None)
            return

        if len(new_good_tests) > 0:
            cybld_helpers.print_centered_text("The following tests went GOOD", True)
            for new_test in new_good_tests:
                cybld_helpers.print_text_with_bg(new_test, True)
        else:
            cybld_helpers.print_centered_text("No additional tests went GOOD", True)

        if len(new_bad_tests) > 0:
            cybld_helpers.print_centered_text("The following tests went BAD", False)
            for new_test in new_bad_tests:
                cybld_helpers.print_text_with_bg(new_test, False)
        else:
            cybld_helpers.print_centered_text("No additional tests went BAD", False)

# --------------------------------------------------------------------------

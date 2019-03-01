"""
A source code linting analyzer for checking PEP8 and Pyflakes warnings
"""
import os
import subprocess

from analyzer.report import Grade


class LintError(object):
    """A struct for lint error message

    location: File path location of error or warning
    line:     The number of line where the error or warning occurred
    message:  Lint error or warning message
    """

    def __init__(self, location, line, message):
        self.location = location
        self.line = line
        self.message = message

    def to_document(self):
        """Make document dict of instance to store to db"""
        return {
            'location': self.location,
            'line': self.line,
            'message': self.message
        }


class LintAnalyzer(Grade):
    """A common analyzer struct
    
    lint_error_list: LintError list for linting
    """
    document_name = ''
    message_column = 2

    def __init__(self):
        self.lint_error_list = []

    def _parse_lint_message(self, line):
        """Parse a lint message line

        Args:
            line: A line of lint message

        Returns:
            A tuple of location, line, message of LintError
        """
        tokenized_by_colon = line.split(':')
        location = tokenized_by_colon[0]
        if location.startswith("./"):
            location = location[2:]
        line = tokenized_by_colon[1]
        message = tokenized_by_colon[self.message_column:]
        return location, line, ''.join(message)

    def _save_lint_results(self, output):
        """Save the linting results
        
        Args:
            output: Output result of linter command
        """
        if output:
            for line in output.decode().split('\n')[:-1]:
                self.lint_error_list.append(LintError(*self._parse_lint_message(line)))

    def calculate_score(self, total_line_count):
        """Calculate the linting score"""
        self.score = int(100 * ((total_line_count - len(self.lint_error_list)) / total_line_count))

    def to_document(self):
        """Make document dict of instance to store to db"""
        error_list = [err.to_document() for err in self.lint_error_list]
        document = {
            self.document_name: {'error_list': error_list, 'score': self.score}
        }
        return document


class PEP8LintAnalyzer(LintAnalyzer):
    """An analyzer for PEP8 linting"""
    document_name = 'pep8_lint'
    weight = 0.5
    message_column = 3

    def run(self, path):
        """Run pep8 command for all python source files
        
        path: Cloned repository path
        """
        proc = subprocess.Popen(['pep8', '.'],
                                stdout=subprocess.PIPE,
                                cwd=path)
        output, _ = proc.communicate()
        self._save_lint_results(output)


class PyflakesLintAnalyzer(LintAnalyzer):
    """An analyzer for Pyflakes linting"""
    document_name = 'pyflakes_lint'
    weight = 0.5

    def run(self, path):
        """Run pyflakes command for all python source files
        
        path: Cloned repository path
        """
        proc = subprocess.Popen(['pyflakes', '.'],
                                stdout=subprocess.PIPE,
                                cwd=path)
        output, _ = proc.communicate()
        self._save_lint_results(output)


class MyPyAnalyser(LintAnalyzer):
    """An analyzer for MyPy linting"""
    document_name = 'mypy_lint'
    weight = 0.5

    def run(self, path):
        """Run mypy command for all python source files

        path: Cloned repository path
        """
        cmd = ['mypy', '--ignore-missing-imports', '--allow-untyped-globals']
        for folder, _, filenames in os.walk(path):
            for filename in filenames:
                if filename.lower().endswith(".py"):
                    cmd.append("/".join((folder, filename)))

        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                cwd=path)
        output, _ = proc.communicate()
        self._save_lint_results(output)


class CountAnalyzer(object):
    """An analyzer for counting the lines
    
    file_count:         The number of all python files
    total_line_count:   The number of lines of all python files
    average_line_count: The average number of lines of all python files 
    """

    def __init__(self):
        self.file_count = 0
        self.total_line_count = 0
        self.average_line_count = 0

    def _count_files(self, path):
        """Count the all python files
        
        path: Cloned repository path
        """
        proc = subprocess.Popen(['find', '.', '-name', '*.py'],
                                stdout=subprocess.PIPE,
                                cwd=path)
        output = subprocess.check_output(['wc', '-l'], stdin=proc.stdout)
        file_count = int(output.decode().split()[0])
        return file_count

    def _count_lines(self, path):
        """Count the lines of all python files
        
        path: Cloned repository path
        """
        proc = subprocess.Popen(['find', '.', '-name', '*.py', '-exec', 'cat', '{}', '+'],
                                stdout=subprocess.PIPE,
                                cwd=path)
        output = subprocess.check_output(['wc', '-l'], stdin=proc.stdout)
        line_count = int(output.decode().split()[0])
        return line_count

    def run(self, path):
        """Run count-related command for counting the files and lines
        
        path: Cloned repository path
        """
        self.file_count = self._count_files(path)
        self.total_line_count = self._count_lines(path)
        self.average_line_count = round(self.total_line_count / self.file_count)

    def to_document(self):
        """Make document dict of instance to store to db"""
        return {
            'count': {
                'file_count': self.file_count,
                'line_count': self.total_line_count,
                'avg_line_count': self.average_line_count
            }
        }

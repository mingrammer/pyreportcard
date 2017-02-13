"""
A source code linting analyzer for checking PEP8 and Pyflakes warnings
"""
from glob import glob
import os
import subprocess

from .report import Grade


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
        line = tokenized_by_colon[1]
        # In PEP8 case, tokenized_by_colon[2] refers to column number of a line
        message = tokenized_by_colon[-1]
        return location, line, message
    
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
        raise NotImplementedError('Must implement this method')


class PEP8LintAnalyzer(LintAnalyzer):
    """An analyzer for PEP8 linting"""
    def __init__(self):
        super().__init__()
        self.weight = 0.5

    def run(self, path):
        """Run pep8 command for all python source files
        
        path: Cloned repository path
        """
        all_python_files = glob(os.path.join(path,  "*.py")) + glob(os.path.join(path,  "**/*.py"))
        proc = subprocess.Popen(['pep8'] + all_python_files,
                                  stdout=subprocess.PIPE)
        output, _ = proc.communicate()
        self._save_lint_results(output)

    def to_document(self):
        document = {'pep8_lint': {'error_list': [], 'score': 0}}
        for lint_error in self.lint_error_list:
            document['pep8_lint']['error_list'].append(lint_error.to_document())
        document['pep8_lint']['score'] = self.score
        return document


class PyflakesLintAnalyzer(LintAnalyzer):
    """An analyzer for Pyflakes linting"""
    def __init__(self):
        super().__init__()
        self.weight = 0.5

    def run(self, path):
        """Run pyflakes command for all python source files
        
        path: Cloned repository path
        """
        all_python_files = glob(os.path.join(path,  "*.py")) + glob(os.path.join(path,  "**/*.py"))
        proc = subprocess.Popen(['pyflakes'] + all_python_files,
                                  stdout=subprocess.PIPE)
        output, _ = proc.communicate()
        self._save_lint_results(output)
    
    def to_document(self):
        document = {'pyflakes_lint': {'error_list': [], 'score': 0}}
        for lint_error in self.lint_error_list:
            document['pyflakes_lint']['error_list'].append(lint_error.to_document())
        document['pyflakes_lint']['score'] = self.score
        return document


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
        all_python_files = glob(os.path.join(path,  "*.py")) + glob(os.path.join(path,  "**/*.py"))
        proc = subprocess.Popen(['ls'] + all_python_files,
                                stdout=subprocess.PIPE)
        output = subprocess.check_output(['wc', '-l'], stdin=proc.stdout)
        file_count = int(output.decode().split()[0])
        return file_count

    def _count_lines(self, path):
        """Count the lines of all python files
        
        path: Cloned repository path
        """
        all_python_files = glob(os.path.join(path,  "*.py")) + glob(os.path.join(path,  "**/*.py"))
        proc = subprocess.Popen(['cat'] + all_python_files,
                                stdout=subprocess.PIPE)
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

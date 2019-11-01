import os

from analyzer.report import Grade


class LicenseAnalyzer(Grade):
    """An analyzer for checking license
    
    has_license: Whether if license file exists or not
    """

    LICENSE_PATTERN = ('license', 'license.md', 'license.rst', 'license.txt')

    weight = 0.01

    def __init__(self):
        self.has_license = False

    def calculate_score(self):
        """Calculate the analyzer score"""
        self.score = 100 if self.has_license else 0

    def run(self, path):
        """Check if license file exists
        
        path: Cloned repository path
        """
        for _, _, filenames in os.walk(path):
            for filename in filenames:
                if filename.lower() in self.LICENSE_PATTERN:
                    self.has_license = True
                    return

    def to_document(self):
        """Make document dict of instance to store to db"""
        return {
            'license': {
                'has_license': self.has_license
            }
        }

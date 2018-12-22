import os


class ReadmeAnalyzer(object):
    """An analyzer for checking readme

    has_readme: Whether if readme file exists or not
    """

    README_PATTERN = ('readme', 'readme.md', 'readme.rst', 'readme.txt')

    def __init__(self):
        self.has_readme = False

    def run(self, path):
        """Check if readme file exists

        path: Cloned repository path
        """
        for _, _, filenames in os.walk(path):
            for filename in filenames:
                if filename.lower() in self.README_PATTERN:
                    self.has_readme = True
                    return

    def to_document(self):
        """Make document dict of instance to store to db"""
        return {
            'readme': {
                'has_readme': self.has_readme
            }
        }

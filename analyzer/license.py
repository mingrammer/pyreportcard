import os


class LicenseAnalyzer(object):
    """An analyzer for checking license
    
    has_license: Whether if license file exists or not
    """

    LICENSE_PATTERN = ('license', 'license.md', 'license.rst', 'license.txt')

    def __init__(self):
        self.has_license = False

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

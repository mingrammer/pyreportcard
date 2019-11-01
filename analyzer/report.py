"""
A collection of classes or functions for reporting
"""


class Grade:
    """Common grade struct for measurable features

    weight: Weight value in (0.0, 1.0). Sum of all weights must be 1.0
    score:  Score value for each result in [0, 100]
    """
    weight = 0.0
    score = 0

    def get_weighted_score(self):
        """Returns real score correspoding to weight value"""
        return self.score * self.weight


def calculate_report_grade(*results):
    """Calculate a total grade by summing the analyzed results

    The grade value would be one of [A+, A, B, C, D, E, F]

    Args:
        results: A list of Grade-based results to calculate a grade

    Returns:
        Grade value as string
    """
    total_score = 0

    for result in results:
        total_score += result.get_weighted_score()

    if total_score > 90:
        return 'A+'
    elif total_score > 80:
        return 'A'
    elif total_score > 70:
        return 'B'
    elif total_score > 60:
        return 'C'
    elif total_score > 50:
        return 'D'
    elif total_score > 40:
        return 'E'
    else:
        return 'F'

"""
Run all analyzers and gather the results
"""

from analyzer.code import (
    CountAnalyzer,
    PEP8LintAnalyzer,
    PyflakesLintAnalyzer,
    MyPyAnalyser,
)
from analyzer.license import LicenseAnalyzer
from analyzer.readme import ReadmeAnalyzer
from analyzer.report import calculate_report_grade


ANALYSER_CLASSES = (
    MyPyAnalyser,
    PEP8LintAnalyzer,
    PyflakesLintAnalyzer,
)

DOC_ANALYSER_CLASSES = (
    LicenseAnalyzer,
    ReadmeAnalyzer,
)


def analyze(path):
    """Run all analyzers and gather the results

    Args:
        path (str): Path to repository

    Returns:
        dict: All results as one dictionary
    """
    count_analyzer = CountAnalyzer()
    count_analyzer.run(path)
    line_count = count_analyzer.total_line_count

    results = count_analyzer.to_document()
    analyzers = []

    for analyzer_class in ANALYSER_CLASSES:
        analyzer = analyzer_class()
        analyzers.append(analyzer)
        analyzer.run(path)
        analyzer.calculate_score(line_count)
        results.update(analyzer.to_document())

    for analyzer_class in DOC_ANALYSER_CLASSES:
        analyzer = analyzer_class()
        analyzers.append(analyzer)
        analyzer.run(path)
        analyzer.calculate_score()
        results.update(analyzer.to_document())

    results["report_grade"] = calculate_report_grade(*analyzers)

    return results

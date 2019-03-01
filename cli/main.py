#!/usr/bin/env python

from argparse import ArgumentParser

from analyzer import analyze
from cli.formatting import format_results

if __name__ == "__main__":
    parser = ArgumentParser(
        description="Analyze the Python code quality with various tools."
    )
    parser.add_argument(
        "--directory",
        "-d",
        type=str,
        default=".",
        help="Root directory of your Python application (default '.')",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", default=False, help="Verbose output"
    )
    arguments = parser.parse_args()
    path = arguments.directory
    results = analyze(path)
    print(format_results(results, verbose=arguments.verbose))

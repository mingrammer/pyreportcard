"""
CLI formatting code
"""

INDENT_PREFIX = "        "


def format_results(results, verbose=False):
    """Return results as a human readable text

    Args:
        results (dict): Dictionary of results
        verbose (bool): List all errors and warnings if True

    Returns:
        str: Human readable CLI output string
    """
    text = "Grade: %s\n" "Files: %d" % (
        results["report_grade"],
        results["count"]["file_count"],
    )

    lines = [text]
    for key, result in sorted(results.items()):
        if key in {"report_grade", "count"}:
            continue

        score = result.get("score")
        if score is None:
            if next(iter(result.values())):
                score = 100
            else:
                score = 0

        lines.append("%s: %d%%" % (key, score))

        if verbose:
            error_list = result.get("error_list", tuple())
            sorted_errors = (
                (err["location"], int(err["line"]), err["message"].strip())
                for err in error_list
            )
            previous_filename = None
            for filename, line_nb, msg in sorted_errors:
                if filename != previous_filename:
                    lines.append("%s%s" % (INDENT_PREFIX, filename))
                    previous_filename = filename
                lines.append(
                    "%s%sLine %d: %s" % (INDENT_PREFIX, INDENT_PREFIX, line_nb, msg)
                )

    return "\n".join(lines)

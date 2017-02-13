from flask import flash, g, redirect, render_template, request, url_for

from app import app, mongo
from analyzer.code import CountAnalyzer, PEP8LintAnalyzer, PyflakesLintAnalyzer
from analyzer.license import LicenseAnalyzer
from analyzer.report import calculate_report_grade
from vcs.repository import (cache,
                            clear,
                            clone,
                            create_repository,
                            is_cached,
                            parse_url)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/check', methods=['POST'])
def check():
    url = request.form['url']
    try:
        parse_url(url)
        return redirect(url_for('report', repo_url=url))
    except:
        flash('Given repository url is not valid')
        return redirect(url_for('index'))


@app.route('/report/<path:repo_url>', methods=['GET'])
def report(repo_url):
    repo = create_repository(repo_url)
    if repo is None:
        flash('Given repository does not exists or could not be accessed')
        return redirect(url_for('index'))

    if is_cached(repo):
        results = mongo.db.repositories.find_one({'url': repo.url})
    else:
        path = clone(repo)

        count_analyzer = CountAnalyzer()
        pep8_analyzer = PEP8LintAnalyzer()
        pyflakes_analyzer = PyflakesLintAnalyzer()
        license_analyzer = LicenseAnalyzer()

        count_analyzer.run(path)
        pep8_analyzer.run(path)
        pyflakes_analyzer.run(path)
        license_analyzer.run(path)

        pep8_analyzer.calculate_score(count_analyzer.total_line_count)
        pyflakes_analyzer.calculate_score(count_analyzer.total_line_count)

        repo.save_analysis_results({
            **count_analyzer.to_document(),
            **pep8_analyzer.to_document(),
            **pyflakes_analyzer.to_document(),
            **license_analyzer.to_document(),
            'report_grade': calculate_report_grade(pep8_analyzer,
                                                pyflakes_analyzer)
        })
        results = repo.to_document()

        cache(repo)
        clear(path)
    return render_template('report/results.html', report=results)
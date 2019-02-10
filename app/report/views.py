from flask import flash, redirect, render_template, request, url_for

from analyzer.code import CountAnalyzer, PEP8LintAnalyzer, PyflakesLintAnalyzer
from analyzer.general import analyze
from analyzer.license import LicenseAnalyzer
from analyzer.readme import ReadmeAnalyzer
from analyzer.report import calculate_report_grade
from app import app, mongo
from vcs.repository import cache, clear, clone, create_repository, is_cached, parse_url


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

        results = analyze(path)
        repo.save_analysis_results(results)

        cache(repo)
        clear(path)

        results = repo.to_document()
    return render_template('report/results.html', report=results)

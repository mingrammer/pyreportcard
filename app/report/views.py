from flask import flash, g, redirect, render_template, request, url_for

from app import app
from vcs.repository import is_valid_github_repository, parse_url_and_get_repo

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/check', methods=['POST'])
def check():
    url = request.form['url']
    if not is_valid_github_repository(url):
        flash('Given repository url is not valid')
        return redirect(url_for('index'))
    return redirect(url_for('report', repo_url=url))


@app.route('/report/<path:repo_url>', methods=['GET'])
def report(repo_url):
    repo = parse_url_and_get_repo(repo_url)
    if repo is None:
        flash('Given repository does not exists')
        return redirect(url_for('index'))
    results = {}
    # Analysis processing
    return render_template('report/results.html', results=results)
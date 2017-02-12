from flask import flash, g, redirect, render_template, request, url_for

from app import app
from vcs.repository import parse_url, create_repository

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
    results = {}
    # Analysis processing
    return render_template('report/results.html', results=results)
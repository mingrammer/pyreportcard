"""
It handles the cloning, cleaning, check caching the repository for
analyzing that to score and to report.
Supports 'git' protocol and 'Github' host now.
"""
import datetime
import os
import shutil
import subprocess

from config import Config
import constants
from helpers.db import get_repo_collection


class GitRepository(object):
    """Scheme for repository information

    url:              Repository URL
    name:             Repository name
    username:         Owner of repository
    last_latest_hash: Last saved latest commit hash
    latest_hash:      Last cloned latest commit hash
    date:             Cached datetime
    analysis_results: A dict of analysis results
    """
    last_latest_hash = None
    latest_hash = None
    analysis_results = {}

    def __init__(self, url=None, username=None, name=None, latest_hash=None):
        self.url = url
        self.username = username
        self.name = name
        self.latest_hash = latest_hash

    def to_document(self):
        """Make document dict of instance to store to db"""
        return {
            'url': self.url,
            'name': self.name,
            'username': self.username,
            'last_latest_hash': self.last_latest_hash,
            'date': datetime.datetime.now(),
            'analysis_results': self.analysis_results
        }

    def save_analysis_results(self, analysis_results):
        self.analysis_results = analysis_results

    def update_last_latest_hash(self):
        self.last_latest_hash = self.latest_hash


def get_latest_commit_hash(url):
    """Get the latest commit hash from a repository url

    Args:
        url: A repository url

    Returns:
        The commit hash string if successful

    Raises:
        subprocess.CalledProcessError: An error occured getting hash from remote git repository
    """
    proc = subprocess.Popen(['git', 'ls-remote', url],
                            stdout=subprocess.PIPE)
    output = subprocess.check_output(['grep', 'HEAD'], stdin=proc.stdout)
    output = subprocess.check_output(['cut', '-f', '1'], input=output)
    hash_string = output.strip().decode('utf-8')
    return hash_string


def parse_url_and_get_repo(url):
    """Tokenize the url to get repository information

    It parses the url and returns following properties

    - name (refers to repository name)
    - username

    Args:
        url: A repository URL

    Returns:
        A GitRepository instance has tokenized values if successful, None otherwise
    """
    try:
        commit_hash = get_latest_commit_hash(url)
        scheme_trimmed_url = url.split('://')[-1]
        host_trimmed_url = scheme_trimmed_url.split(':')[-1]
        username, name = host_trimmed_url.split('/')[-2:]
        git_repo = GitRepository(
            url=url,
            username=username,
            name=name,
            latest_hash=commit_hash
        )
        return git_repo
    except subprocess.CalledProcessError:
        return None


def cache(repo):
    """Cache the given repository to reuse later

    Args:
        repo: A repository instance
    """
    repositories = get_repo_collection()
    repo.update_last_latest_hash()
    repo_doc = repo.to_document()
    repositories.insert_one(repo_doc)


def is_cached(repo):
    """Check if the repository was cached

    Args:
        repo: A repository instance

    Returns:
        Whether if there is cached one or not
    """
    repositories = get_repo_collection()
    repo_doc = repositories.find_one({'name': repo.name, 'username': repo.username})

    if not repo_doc:
        return False
    if repo_doc['last_latest_hash'] != repo.latest_hash:
        return False
    return True


def clone(repo):
    """Clone the repository on temporary place and return location

    Args:
        repo: A repository instance

    Returns:
        A tmp directory of repository if successful, raise exception otherwise
    """
    tmp_dir = Config.CLONE_TMP_DIR
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)

    proc = subprocess.Popen(['git', 'clone', repo.url],
                            stdout=subprocess.PIPE,
                            cwd=tmp_dir)

    try:
        _, err = proc.communicate(timeout=Config.CLONE_TIMEOUT)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise Exception(constants.ERROR_CLONE_TIMEOUT_EXPIRED)

    if err:
        raise Exception(constants.ERROR_CLONE_FAILED)

    return os.path.join(tmp_dir, repo.name)


def clear(path):
    """Clear the cloned repository directory

    Args:
        path: The directory path of cloned repository
    """
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

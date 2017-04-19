"""
It handles the cloning, cleaning, check caching the repository for
analyzing that to score and to report.
Supports 'git' protocol and 'Github' host now.
"""
import datetime
import os
import re
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


def parse_url(url):
    """Tokenize the url to get username and repository name

    It parses the url and returns following properties

    - username
    - name (refers to repository name)

    Args:
        url: A repository URL

    Returns:
        A tuple of username and name if successful

    Raises:
        ValueError: An error occured parsing invalid github repository URL
    """
    check_valid_github_repository = re.match(r'^github.com/[\w-]+/[\w-]+/?$', url)
    if check_valid_github_repository is None:
        raise ValueError('The given repository URL is not valid')
    username, name = url.split('/')[-2:]
    return username, name


def _make_git_protocol_url(url):
    """Make an URL with 'git@github.com' form

    Args:
        url: A repository URL

    Returns:
        Git protocol form URL
    """
    username, name = parse_url(url)
    git_protocol_url = 'git://github.com/{0}/{1}.git'.format(username, name)
    return git_protocol_url


def _get_latest_commit_hash(url):
    """Get the latest commit hash from a repository url

    Args:
        url: A repository url

    Returns:
        The commit hash string if successful

    Raises:
        subprocess.CalledProcessError: An error occured getting hash from remote git repository
    """
    proc = subprocess.Popen(['git', 'ls-remote', _make_git_protocol_url(url)],
                            stdout=subprocess.PIPE)
    output = subprocess.check_output(['grep', 'HEAD'], stdin=proc.stdout)
    output = subprocess.check_output(['cut', '-f', '1'], input=output)
    hash_string = output.strip().decode('utf-8')
    return hash_string


def create_repository(url):
    """Create a repository instance for given repository url

    Args:
        url: A repository URL

    Returns:
        A GitRepository instance if successful, None otherwise
    """
    try:
        commit_hash = _get_latest_commit_hash(url)
        username, name = parse_url(url)
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
    repositories.update({'url': repo.url}, repo.to_document(), upsert=True)


def is_cached(repo):
    """Check if the repository was cached

    Args:
        repo: A repository instance

    Returns:
        Whether if there is cached one or not
    """
    repositories = get_repo_collection()
    repo_doc = repositories.find_one({'url': repo.url})

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

    proc = subprocess.Popen(['git', 'clone', '--depth=1', _make_git_protocol_url(repo.url)],
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

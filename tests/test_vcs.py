import os
import shutil
import unittest

import config
from helper import get_repo_collection
from vcs.repository import (GitRepository,
                            tokenize_url_and_get_repo,
                            cache,
                            is_cached,
                            clone,
                            clear)


class RepositoryTest(unittest.TestCase):
    def setUp(self):
        self.repositories = get_repo_collection()
        self.repo = GitRepository(
            url='https://github.com/mingrammer/sorting',
            name='sorting',
            username='mingrammer'
        )

    def tearDown(self):
        self.repositories.delete_one({'url': self.repo.url})
        if os.path.isdir(config.CLONE_TMP_DIR):
            cloned_path = os.path.join(config.CLONE_TMP_DIR, self.repo.name)
            if os.path.isdir(cloned_path):
                shutil.rmtree(cloned_path)
            else:
                shutil.rmtree(config.CLONE_TMP_DIR)

    def test_tokenize_url_and_get_repo(self):
        testcases = [
            {
                'url': 'https://github.com/mingrammer/sorting',
                'name': 'sorting',
                'username': 'mingrammer',
            },
            {
                'url': 'git@github.com:django/django',
                'name': 'django',
                'username': 'django',
            }
        ]
        for tc in testcases:
            repo = tokenize_url_and_get_repo(tc['url'])
            self.assertEqual(repo.url, tc['url'])
            self.assertEqual(repo.name, tc['name'])
            self.assertEqual(repo.username, tc['username'])

    def test_cache(self):
        cache(self.repo)
        repo_doc = self.repositories.find_one({'url': self.repo.url})
        self.assertEqual(repo_doc['url'], self.repo.url)
        self.assertEqual(repo_doc['name'], self.repo.name)
        self.assertEqual(repo_doc['username'], self.repo.username)
        self.assertNotEqual(repo_doc['last_latest_hash'], None)

    def test_is_cache(self):
        self.assertEqual(is_cached(self.repo), False)
        cache(self.repo)
        self.assertEqual(is_cached(self.repo), True)

    def test_clone(self):
        cloned_path = clone(self.repo)
        self.assertEqual(cloned_path, os.path.join(config.CLONE_TMP_DIR, self.repo.name))

    def test_clone_fail(self):
        self.repo.url = 'https://github.com/mingrammer/null'
        with self.assertRaises(Exception):
            clone(self.repo.url)

    def test_clear(self):
        os.mkdir(config.CLONE_TMP_DIR)
        os.mkdir(os.path.join(config.CLONE_TMP_DIR, config.CLONE_TMP_DIR))
        clear(config.CLONE_TMP_DIR)
        self.assertEqual(os.path.isdir(config.CLONE_TMP_DIR), False)

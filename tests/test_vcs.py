import os
import shutil
import unittest

from config import Config
from helpers.db import get_repo_collection
from vcs.repository import (GitRepository,
                            parse_repository_url,
                            cache,
                            is_cached,
                            clone,
                            clear)


class RepositoryTest(unittest.TestCase):
    def setUp(self):
        self.repositories = get_repo_collection()
        self.repo = parse_repository_url('https://github.com/mingrammer/sorting')

    def tearDown(self):
        self.repositories.delete_one({'url': self.repo.url})
        if os.path.isdir(Config.CLONE_TMP_DIR):
            cloned_path = os.path.join(Config.CLONE_TMP_DIR, self.repo.name)
            if os.path.isdir(cloned_path):
                shutil.rmtree(cloned_path)
            else:
                shutil.rmtree(Config.CLONE_TMP_DIR)

    def test_parse_repository_url(self):
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
            repo = parse_repository_url(tc['url'])
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
        self.assertEqual(cloned_path, os.path.join(Config.CLONE_TMP_DIR, self.repo.name))

    def test_clone_fail(self):
        self.repo.url = 'https://github.com/mingrammer/null'
        with self.assertRaises(Exception):
            clone(self.repo.url)

    def test_clear(self):
        os.mkdir(Config.CLONE_TMP_DIR)
        os.mkdir(os.path.join(Config.CLONE_TMP_DIR, Config.CLONE_TMP_DIR))
        clear(Config.CLONE_TMP_DIR)
        self.assertEqual(os.path.isdir(Config.CLONE_TMP_DIR), False)

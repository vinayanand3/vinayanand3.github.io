import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from scripts.update_repos import fetch_all_repositories, prepare_repositories, write_snapshot


FIXTURE = Path(__file__).parent / "fixtures" / "repositories.json"


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class RepositoryGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.repositories = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_filters_forks_private_and_infrastructure_repositories(self):
        projects = prepare_repositories(self.repositories)
        self.assertEqual([project["name"] for project in projects], ["latest-tool", "older-project"])

    def test_normalizes_missing_metadata_and_sorts_by_push_date(self):
        projects = prepare_repositories(self.repositories)
        self.assertEqual(projects[0]["topics"], ["react", "tools"])
        self.assertEqual(projects[0]["homepageUrl"], "https://latest.example.com")
        self.assertIsNone(projects[1]["description"])
        self.assertIsNone(projects[1]["homepageUrl"])
        self.assertIsNone(projects[1]["language"])

    def test_fetches_every_page(self):
        pages = [self.repositories[:2], self.repositories[2:3]]
        opener = Mock(side_effect=[FakeResponse(page) for page in pages])
        fetched = fetch_all_repositories("vinayanand3", per_page=2, opener=opener)
        self.assertEqual(len(fetched), 3)
        self.assertEqual(opener.call_count, 2)

    def test_snapshot_does_not_rewrite_unchanged_data(self):
        projects = prepare_repositories(self.repositories)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "repos.json"
            self.assertTrue(write_snapshot(projects, output))
            self.assertFalse(write_snapshot(projects, output))


if __name__ == "__main__":
    unittest.main()

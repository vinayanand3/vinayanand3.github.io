#!/usr/bin/env python3
"""Generate the static repository catalog used by the portfolio homepage."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_USERNAME = "vinayanand3"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "data" / "repos.json"
EXCLUDED_REPOSITORIES = {"vinayanand3", "vinayanand3.github.io"}


def fetch_all_repositories(
    username: str,
    token: str | None = None,
    *,
    per_page: int = 100,
    opener: Callable[..., Any] = urlopen,
) -> list[dict[str, Any]]:
    """Fetch all public repositories owned by a GitHub user."""
    repositories: list[dict[str, Any]] = []
    page = 1
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "vinayanand3-portfolio-sync",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    while True:
        url = (
            f"https://api.github.com/users/{username}/repos"
            f"?type=owner&sort=full_name&direction=asc&per_page={per_page}&page={page}"
        )
        request = Request(url, headers=headers)
        try:
            with opener(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            raise RuntimeError(f"GitHub API returned HTTP {error.code}") from error
        except URLError as error:
            raise RuntimeError(f"Unable to reach GitHub: {error.reason}") from error

        if not isinstance(payload, list):
            raise RuntimeError("GitHub API returned an unexpected response")
        repositories.extend(payload)
        if len(payload) < per_page:
            break
        page += 1

    return repositories


def normalize_repository(repository: dict[str, Any]) -> dict[str, Any]:
    """Select and rename the public fields consumed by the frontend."""
    return {
        "name": repository["name"],
        "description": repository.get("description") or None,
        "repositoryUrl": repository["html_url"],
        "homepageUrl": repository.get("homepage") or None,
        "language": repository.get("language") or None,
        "topics": sorted(repository.get("topics") or []),
        "stars": int(repository.get("stargazers_count") or 0),
        "pushedAt": repository.get("pushed_at") or None,
        "updatedAt": repository.get("updated_at") or None,
    }


def prepare_repositories(repositories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Filter non-project repositories and sort the remainder by recent pushes."""
    included = [
        normalize_repository(repository)
        for repository in repositories
        if not repository.get("fork", False)
        and not repository.get("private", False)
        and repository.get("name") not in EXCLUDED_REPOSITORIES
    ]
    return sorted(
        included,
        key=lambda repository: (
            repository.get("pushedAt") or repository.get("updatedAt") or "",
            repository["name"].lower(),
        ),
        reverse=True,
    )


def write_snapshot(repositories: list[dict[str, Any]], output: Path) -> bool:
    """Write deterministic JSON and report whether its contents changed."""
    content = json.dumps(repositories, indent=2, ensure_ascii=False) + "\n"
    if output.exists() and output.read_text(encoding="utf-8") == content:
        return False
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default=DEFAULT_USERNAME)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw_repositories = fetch_all_repositories(args.username, os.environ.get("GITHUB_TOKEN"))
    projects = prepare_repositories(raw_repositories)
    changed = write_snapshot(projects, args.output)
    status = "Updated" if changed else "Unchanged"
    print(f"{status}: {args.output} contains {len(projects)} projects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

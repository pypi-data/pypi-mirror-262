from importlib.metadata import Distribution
from pathlib import Path
from typing import Any

import requests
from cleo.io.io import IO
from poetry.poetry import Poetry
from poetry.utils.env import EnvManager


class PoetryPatcher:
    TIMEOUT = 100

    def __init__(self, poetry: Poetry, io: IO):
        self.poetry = poetry
        self.io = io

    def get_config(self) -> dict[str, Any]:
        tool = self.poetry.pyproject.data["tool"]
        assert isinstance(tool, dict)
        config = tool.get("poetry-patches", {})
        assert isinstance(config, dict)
        return config

    def patch(self) -> None:
        env = EnvManager(self.poetry, self.io).get()
        config = self.get_config()

        for key, value in config.items():
            patches = [value] if isinstance(value, str) else value
            if distribution := env.site_packages.find_distribution(key):
                self.apply_patches(distribution, patches)

    def apply_patches(self, distribution: Distribution, patches: list[str]) -> None:
        for patch in patches:
            self.apply_patch(distribution, patch)

    def apply_patch(self, distribution: Distribution, patch: str):
        patch_content = self.read(patch)

    def read(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return requests.get(path).content.decode()
        else:
            return Path(path).read_text()

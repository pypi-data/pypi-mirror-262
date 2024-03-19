from poetry.console.commands.group_command import GroupCommand

from poetry_patches.patcher import PoetryPatcher


class PatchesRunCommand(GroupCommand):
    name = "patches run"
    description = "Applies the patches to the dependencies."

    def handle(self) -> int:
        PoetryPatcher(self.poetry, self.io).patch()

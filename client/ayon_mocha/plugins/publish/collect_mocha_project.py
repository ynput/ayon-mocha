"""Collect the current Mocha Pro project."""
from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

import pyblish.api
from mocha.project import get_current_project

if TYPE_CHECKING:
    from logging import Logger


class CollectMochaProject(pyblish.api.ContextPlugin):
    """Inject the current working file into context.

    Foo batr baz.
    """

    order = pyblish.api.CollectorOrder - 0.5
    label = "Collect Mocha Pro Project"
    hosts: ClassVar[list[str]] = ["mochapro"]
    log: Logger

    def process(self, context: pyblish.api.Context) -> None:
        """Inject the current working file."""
        context.data["project"] = get_current_project()
        current_file = context.data["project"].project_file
        context.data["currentFile"] = current_file
        if not current_file:
            self.log.warning(
                "Current file is not saved. Save the file before continuing."
            )

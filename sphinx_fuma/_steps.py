"""The ``steps`` directive.

fumadocs renders numbered walkthroughs as a rail of circled step numbers. There
is no Sphinx equivalent, so a thin container directive marks the region and the
stylesheet draws the rail from the headings inside it.
"""

from docutils import nodes
from docutils.parsers.rst import Directive

__all__ = ("setup_steps",)


class StepsDirective(Directive):
    """Wrap nested content so each child heading renders as a numbered step."""

    has_content = True
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        container = nodes.container(classes=["fd-steps"])
        self.state.nested_parse(self.content, self.content_offset, container)
        return [container]


def setup_steps(app) -> None:
    app.add_directive("steps", StepsDirective)

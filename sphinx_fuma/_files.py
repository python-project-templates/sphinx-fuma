"""The ``files`` directive.

Renders a project layout as a file tree. The content is an ordinary nested list,
so authors write plain Markdown or reStructuredText; a trailing ``/`` or the
presence of children marks an entry as a directory.
"""

from docutils import nodes
from docutils.parsers.rst import Directive

__all__ = ("setup_files",)


def _entries(bullet_list: nodes.Element) -> list[nodes.Element]:
    entries = []
    for item in bullet_list.children:
        if not isinstance(item, nodes.list_item):
            continue
        name = ""
        children = None
        for child in item.children:
            if isinstance(child, nodes.bullet_list):
                children = child
            elif not name and isinstance(child, (nodes.paragraph, nodes.Text)):
                name = child.astext().strip()
        if not name:
            continue
        is_folder = children is not None or name.endswith("/")
        label = name.rstrip("/")
        entry = nodes.container(classes=["fd-folder-entry" if is_folder else "fd-file-entry"])
        entry += nodes.inline(label, label, classes=["fd-entry-name"])
        if children is not None:
            nested = nodes.container(classes=["fd-files-children"])
            nested.extend(_entries(children))
            entry += nested
        entries.append(entry)
    return entries


class FilesDirective(Directive):
    """Turn a nested list into a file tree."""

    has_content = True
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self):
        parsed = nodes.Element()
        self.state.nested_parse(self.content, self.content_offset, parsed)
        tree = nodes.container(classes=["fd-files"])
        for child in parsed.children:
            if isinstance(child, nodes.bullet_list):
                tree.extend(_entries(child))
        if not tree.children:
            return [self.state_machine.reporter.warning("`files` expects a nested list", line=self.lineno)]
        return [tree]


def setup_files(app) -> None:
    app.add_directive("files", FilesDirective)

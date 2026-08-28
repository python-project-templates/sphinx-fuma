"""Structured navigation data for the templates.

Sphinx hands themes pre-rendered HTML for the sidebar (``toctree()``) and the
page-local table of contents (``toc``). Both are nested ``<ul>`` markup with no
hook for the collapsible folders and scroll-spy list this theme needs, so the
resolved doctrees are walked here into plain dictionaries the templates render
directly.
"""

from docutils import nodes
from sphinx import addnodes

__all__ = ("breadcrumbs", "page_toc", "sidebar_tree")


def _resolve_global_toctree(app, pagename: str, maxdepth: int):
    env, builder = app.env, app.builder
    # ``titles_only`` keeps in-page headings out of the sidebar; they belong to
    # the page-local table of contents instead.
    options = {"collapse": False, "includehidden": True, "maxdepth": maxdepth, "titles_only": True}
    try:
        from sphinx.environment.adapters.toctree import global_toctree_for_doc

        return global_toctree_for_doc(env, pagename, builder, **options)
    except ImportError:  # pragma: no cover - Sphinx < 7.2 layout
        from sphinx.environment.adapters.toctree import TocTree

        return TocTree(env).get_toctree_for(pagename, builder, **options)


def _reference_of(item: nodes.Element):
    for child in item.children:
        if isinstance(child, addnodes.compact_paragraph):
            return child.next_node(nodes.reference)
        if isinstance(child, nodes.reference):
            return child
    return None


def _sublist_of(item: nodes.Element):
    for child in item.children:
        if isinstance(child, nodes.bullet_list):
            return child
    return None


def _entries(bullet_list: nodes.Element, depth: int, icons: dict[str, str]) -> list[dict]:
    entries = []
    for item in bullet_list.children:
        if not isinstance(item, nodes.list_item):
            continue
        reference = _reference_of(item)
        if reference is None:
            continue
        sublist = _sublist_of(item)
        classes = reference.get("classes", [])
        refuri = reference.get("refuri", "")
        entries.append(
            {
                "title": reference.astext(),
                "url": refuri or "#",
                # ``env.tocs`` keeps the fragment here rather than in ``refuri``.
                "anchor": reference.get("anchorname", ""),
                "external": refuri.startswith(("http://", "https://", "//")),
                "icon": icons.get(refuri, ""),
                # ``current`` marks the active page; ``active`` marks its ancestors.
                "current": "current" in classes,
                "active": "current" in item.get("classes", []),
                "depth": depth,
                "children": _entries(sublist, depth + 1, icons) if sublist is not None else [],
            }
        )
    return entries


def _icons_by_uri(app, pagename: str) -> dict[str, str]:
    """Map each document's URI (as the toctree renders it) to its ``icon`` metadata.

    Resolved toctrees carry relative URIs rather than docnames, so the lookup is
    built from the same relative-URI function the toctree resolver used.
    """
    icons = {}
    for docname, metadata in app.env.metadata.items():
        icon = str(metadata.get("icon", "")).strip()
        if icon:
            icons[app.builder.get_relative_uri(pagename, docname)] = icon
    return icons


def sidebar_tree(app, pagename: str, maxdepth: int = 4) -> list[dict]:
    """Return the global toctree as a list of ``{caption, entries}`` groups."""
    resolved = _resolve_global_toctree(app, pagename, maxdepth)
    if resolved is None:
        return []
    icons = _icons_by_uri(app, pagename)
    groups: list[dict] = []
    caption = ""
    for child in resolved.children:
        # Sphinx renders a toctree ``:caption:`` as a title node ahead of the list.
        if isinstance(child, (nodes.title, nodes.caption)):
            caption = child.astext()
        elif isinstance(child, nodes.bullet_list):
            entries = _entries(child, 1, icons)
            if entries:
                # Not ``items``: Jinja resolves attributes before keys, and
                # ``group.items`` would find the dict method instead.
                groups.append({"caption": caption, "entries": entries})
            caption = ""
    return groups


def page_toc(app, pagename: str) -> list[dict]:
    """Return the page-local headings, excluding the document title."""
    toc = app.env.tocs.get(pagename)
    if toc is None:
        return []
    entries = _entries(toc, 1, {})
    # A single top-level entry is the document title; its children are the real headings.
    while len(entries) == 1 and entries[0]["children"]:
        entries = [dict(child, depth=child["depth"] - 1) for child in entries[0]["children"]]
    return _flatten_toc(entries)


def _flatten_toc(entries: list[dict], depth: int = 1) -> list[dict]:
    """Flatten nested headings so the scroll-spy indicator can track one list."""
    flat = []
    for entry in entries:
        flat.append({"title": entry["title"], "url": entry["anchor"] or "#", "depth": depth})
        flat.extend(_flatten_toc(entry["children"], depth + 1))
    return flat


def breadcrumbs(context: dict) -> list[dict]:
    """Return ancestor pages, dropping the root so it can be rendered separately."""
    parents = context.get("parents") or []
    return [{"title": parent.get("title", ""), "url": parent.get("link", "")} for parent in parents]

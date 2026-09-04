""":mod:`sphinx_fuma` — a Sphinx theme with a fumadocs-style layout.

The visual design system (the ``--color-fd-*`` token set and the named-area
grid) follows fumadocs, which is MIT licensed, Copyright (c) 2023 Fuma. Nothing
here is affiliated with or endorsed by that project.
"""

from pathlib import Path

from ._files import setup_files
from ._nav import breadcrumbs, page_toc, sidebar_tree
from ._options import build_context
from ._steps import setup_steps

__all__ = ("THEME_DIR", "THEME_NAME", "setup")
__version__ = "0.1.2"

THEME_DIR = Path(__file__).parent
THEME_NAME = "fuma"


def _active(app) -> bool:
    return app.config.html_theme == THEME_NAME


def _on_config_inited(app, config) -> None:
    # The theme ships its own dialog, so the bundled searchlite one would double up.
    if config.html_theme == THEME_NAME:
        config.searchlite_ui = False


def _on_builder_inited(app) -> None:
    if not _active(app):
        return
    app.add_js_file("fuma.js", loading_method="defer")
    # Skipping the stylesheet is what makes ``fonts = "system"`` avoid the download.
    if str(app.config.html_theme_options.get("fonts", "bundled")).strip().lower() != "system":
        app.add_css_file("fonts/fuma-fonts.css")


def _on_page_context(app, pagename, templatename, context, doctree) -> None:
    if not _active(app):
        return
    context.update(build_context(context))
    context["fuma_sidebar"] = sidebar_tree(app, pagename)
    context["fuma_toc"] = page_toc(app, pagename)
    context["fuma_breadcrumbs"] = breadcrumbs(context)


def setup(app) -> dict[str, object]:
    app.setup_extension("sphinx_searchlite")
    app.add_html_theme(THEME_NAME, str(THEME_DIR))
    app.connect("config-inited", _on_config_inited)
    app.connect("builder-inited", _on_builder_inited)
    app.connect("html-page-context", _on_page_context)
    setup_steps(app)
    setup_files(app)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

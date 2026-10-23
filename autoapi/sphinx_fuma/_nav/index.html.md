# sphinx_fuma._nav

Structured navigation data for the templates.

Sphinx hands themes pre-rendered HTML for the sidebar (`toctree()`) and the
page-local table of contents (`toc`). Both are nested `<ul>` markup with no
hook for the collapsible folders and scroll-spy list this theme needs, so the
resolved doctrees are walked here into plain dictionaries the templates render
directly.

## Functions

| [`sidebar_tree`](#sphinx_fuma._nav.sidebar_tree)(→ list[dict])   | Return the global toctree as a list of `{caption, entries}` groups.        |
|------------------------------------------------------------------|----------------------------------------------------------------------------|
| [`page_toc`](#sphinx_fuma._nav.page_toc)(→ list[dict])           | Return the page-local headings, excluding the document title.              |
| [`breadcrumbs`](#sphinx_fuma._nav.breadcrumbs)(→ list[dict])     | Return ancestor pages, dropping the root so it can be rendered separately. |

## Module Contents

### sphinx_fuma._nav.sidebar_tree(app, pagename: str, maxdepth: int = 4) → list[dict][[source]](../../../_modules/sphinx_fuma/_nav.html.md#sidebar_tree)

Return the global toctree as a list of `{caption, entries}` groups.

### sphinx_fuma._nav.page_toc(app, pagename: str) → list[dict][[source]](../../../_modules/sphinx_fuma/_nav.html.md#page_toc)

Return the page-local headings, excluding the document title.

### sphinx_fuma._nav.breadcrumbs(context: dict) → list[dict][[source]](../../../_modules/sphinx_fuma/_nav.html.md#breadcrumbs)

Return ancestor pages, dropping the root so it can be rendered separately.

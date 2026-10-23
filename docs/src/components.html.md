# Content component showcase

This page renders theme-native directives and commonly used Sphinx content with sphinx-fuma.

## Theme directives

### Steps

The `steps` directive turns its child headings into a numbered walkthrough.

### Install the package

Add sphinx-fuma to the documentation environment.

### Select the theme

Set `html_theme = "fuma"` in `conf.py`.

### Build the site

Run the normal Sphinx HTML builder.

```markdown
```{steps}
### Install the package

Add sphinx-fuma to the documentation environment.

### Select the theme

Set `html_theme = "fuma"` in `conf.py`.

### Build the site

Run the normal Sphinx HTML builder.
```
```

### File trees

The `files` directive turns a nested list into a compact project tree. A trailing slash or child list marks a folder.

docsconf.pyindex.mdsrcexampleinit.pypyproject.toml
```markdown
```{files}
- docs/
  - conf.py
  - index.md
- src/
  - example/
    - __init__.py
- pyproject.toml
```
```

## Admonitions

#### NOTE
Notes use the neutral informational treatment.

#### TIP
Tips and important messages use the positive accent treatment.

#### WARNING
Warnings, cautions, and attention messages use the warning treatment.

#### DANGER
Danger and error messages use the destructive treatment.

## Code

Inline code such as `html_theme = "fuma"` uses the monospace font. Press <kbd>/</kbd> or <kbd>Cmd</kbd>/<kbd>Ctrl</kbd>+<kbd>K</kbd> to open search.

```python
html_theme_options = {
    "layout": "docs",
    "toc_style": "clerk",
    "color_preset": "amber",
}
```

```diff
-html_theme = "alabaster"
+html_theme = "fuma"
```

## Tables and quotations

| Feature       | Behavior                                              |
|---------------|-------------------------------------------------------|
| Sidebar       | Collapsible on desktop and overlaid on small screens  |
| Page contents | Tracks visible headings while scrolling               |
| Search        | Loads a local sphinx-searchlite index                 |
| Color mode    | Follows system preference and stores explicit choices |
> Documentation should make the structure of a project visible without getting in the reader’s way.

## Cards

[Sphinx Design](https://sphinx-design.readthedocs.io/) cards inherit the theme’s border, surface, and radius tokens. Install and enable `sphinx-design` to use its directives outside Yardang.

The sidebar, header, and table of contents adapt across screen sizes.

The search dialog uses a static index and requires no hosted service.

Light and dark palettes follow system preference and reader choice.

Page icons, section tabs, breadcrumbs, and pagination keep large sites navigable.

## Tabs

Sphinx Design tab sets use a compact framed treatment.

```console
pip install sphinx-fuma
```

```console
conda install -c conda-forge sphinx-fuma
```

## Lists and links

Ordered and unordered lists use the content column’s rhythm:

1. Configure Sphinx.
2. Write documentation.
3. Build HTML.

- Browse the [theme option reference](theme-options.html.md).
- Review the generated [Python API reference](../../autoapi/index.html.md).
- Open the search dialog with <kbd>/</kbd>.

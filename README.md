# sphinx-fuma

A responsive Sphinx theme inspired by [Fumadocs](https://fumadocs.dev).

[![Build Status](https://github.com/python-project-templates/sphinx-fuma/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/python-project-templates/sphinx-fuma/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/python-project-templates/sphinx-fuma/branch/main/graph/badge.svg)](https://codecov.io/gh/python-project-templates/sphinx-fuma)
[![License](https://img.shields.io/github/license/python-project-templates/sphinx-fuma)](https://github.com/python-project-templates/sphinx-fuma)
[![PyPI](https://img.shields.io/pypi/v/sphinx-fuma.svg)](https://pypi.python.org/pypi/sphinx-fuma)

## Features

- Responsive documentation and notebook layouts
- Collapsible page navigation, breadcrumbs, pagination, page icons, and section tabs
- Scroll-aware page table of contents
- Client-side search powered by [sphinx-searchlite](https://github.com/python-project-templates/sphinx-searchlite)
- Light and dark modes, color presets, and CSS variable overrides
- Self-hosted Geist and JetBrains Mono fonts, with a system-font option
- Native `steps` and `files` directives
- Styling for standard Sphinx content and Sphinx Design cards and tabs

## Quick start

Install the theme:

```console
pip install sphinx-fuma
```

Enable the extension and theme in `conf.py`:

```python
extensions = ["sphinx_fuma"]
html_theme = "fuma"
```

Build the documentation as usual:

```console
sphinx-build -M html docs docs/_build
```

## Documentation

- [How to configure sphinx-fuma](docs/src/getting-started.md)
- [Theme option reference](docs/src/theme-options.md)
- [Content component showcase](docs/src/components.md)

The [published documentation](https://python-project-templates.github.io/sphinx-fuma/) is built with sphinx-fuma and demonstrates its navigation, search, color, and content features.

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).

:icon: rocket

# How to configure sphinx-fuma

This guide shows how to install sphinx-fuma, select it in Sphinx, and apply theme options.

## Install the theme

Install sphinx-fuma from PyPI:

```console
pip install sphinx-fuma
```

The installation includes sphinx-searchlite, which provides the client-side search index used by the theme.

## Enable the theme

Add `sphinx_fuma` to the extensions and select `fuma` in `conf.py`:

```python
extensions = [
    "sphinx_fuma",
]

html_theme = "fuma"
```

The extension registers the theme, its `steps` and `files` directives, and its search integration.

## Configure the site

Add an `html_theme_options` dictionary for the parts of the site you want to customize:

```python
html_theme_options = {
    "color_preset": "amber",
    "github_url": "https://github.com/example/project",
    "nav_links": [
        {"title": "PyPI", "url": "https://pypi.org/project/example/"},
    ],
    "toc_style": "clerk",
}
```

Refer to the [theme option reference](theme-options.md) for every option and accepted value.

## Add icons to pages

Set `icon` in a page's MyST front matter:

```markdown
---
icon: rocket
---

# Installation
```

The icon appears beside the page in the left navigation. Available names are listed in the [theme option reference](theme-options.md).

## Build the documentation

Run Sphinx with your normal source and output directories:

```console
sphinx-build -M html docs docs/_build
```

Open `docs/_build/html/index.html` to inspect the result.

## Use the theme with Yardang

Set the theme in `pyproject.toml` when Yardang generates the Sphinx configuration:

```toml
[tool.yardang]
theme = "fuma"

[tool.yardang.html_theme_options]
color_preset = "amber"
github_url = "https://github.com/example/project"
```

Then build the site:

```console
yardang build
```

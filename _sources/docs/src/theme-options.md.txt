:icon: settings

# Theme option reference

Theme options are entries in the Sphinx `html_theme_options` dictionary.

```python
html_theme = "fuma"
html_theme_options = {
    "layout": "docs",
    "color_preset": "amber",
}
```

## Options

| Option                   | Default     | Accepted values                                                     | Description                                                                                  |
| ------------------------ | ----------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `layout`                 | `"docs"`    | `"docs"`, `"notebook"`                                              | Controls whether the header sits beside the sidebar or spans the page.                       |
| `toc_style`              | `"normal"`  | `"normal"`, `"clerk"`                                               | Controls the right-hand table of contents. `clerk` dims headings outside the active section. |
| `color_preset`           | `"neutral"` | `"neutral"`, `"amber"`, `"blue"`, `"emerald"`, `"purple"`, `"rose"` | Sets the primary color in light and dark modes.                                              |
| `search`                 | `true`      | Boolean                                                             | Shows the search buttons and dialog.                                                         |
| `fonts`                  | `"bundled"` | `"bundled"`, `"system"`                                             | Loads the bundled Geist and JetBrains Mono fonts or uses system stacks.                      |
| `sidebar_hide_name`      | `false`     | Boolean                                                             | Hides the project name beside the logo.                                                      |
| `default_open_level`     | `1`         | Integer                                                             | Sets the sidebar tree depth expanded by default.                                             |
| `github_url`             | `""`        | URL string                                                          | Adds GitHub links and derives edit-page links for GitHub repositories.                       |
| `edit_page_url_template` | `""`        | URL template                                                        | Overrides the edit-page URL derived from `github_url`.                                       |
| `nav_links`              | `[]`        | Link mappings, pairs, or a compact string                           | Adds links to the header and sidebar toolbar.                                                |
| `sidebar_tabs`           | `[]`        | Tab mappings                                                        | Adds a section navigator beneath the project name.                                           |
| `announcement`           | `""`        | String                                                              | Adds a banner above the page layout.                                                         |
| `footer_text`            | `""`        | String                                                              | Adds text to the page footer.                                                                |
| `light_css_variables`    | `{}`        | CSS variable mapping                                                | Overrides design tokens in light mode.                                                       |
| `dark_css_variables`     | `{}`        | CSS variable mapping                                                | Overrides design tokens in dark mode and dark system preference.                             |

Unsupported values for enumerated options fall back to their defaults.

## Standard Sphinx settings

The theme also uses standard Sphinx HTML settings:

| Setting                             | Theme behavior                                         |
| ----------------------------------- | ------------------------------------------------------ |
| `html_logo`                         | Displays a project logo beside the project name.       |
| `html_title` and `html_short_title` | Set the site and brand titles.                         |
| `html_show_sourcelink`              | Shows or hides the page source link in the right rail. |
| `html_show_sphinx`                  | Shows or hides the Sphinx attribution in the footer.   |
| `html_last_updated_fmt`             | Adds the last-updated date to the footer.              |
| `copyright`                         | Adds the copyright notice to the footer.               |

## Layout

`docs` uses the three-column documentation layout. The project header is part of the left sidebar on desktop and becomes a compact top bar at smaller widths.

`notebook` keeps the top bar visible across the page. Both layouts retain the responsive sidebar and page table of contents.

## Search

Search uses the static index provided by sphinx-searchlite. Readers can open the dialog from the header or sidebar, with <kbd>/</kbd>, or with <kbd>Cmd</kbd>/<kbd>Ctrl</kbd>+<kbd>K</kbd>. Arrow keys move through results, <kbd>Enter</kbd> follows the selected result, and <kbd>Esc</kbd> closes the dialog.

Set `search` to `false` to hide the search controls and dialog.

## Navigation links

Each `nav_links` mapping has `title` and `url` fields:

```python
html_theme_options = {
    "nav_links": [
        {"title": "PyPI", "url": "https://pypi.org/project/example/"},
        {"title": "Changelog", "url": "changelog.html"},
    ],
}
```

Two-item `(title, url)` sequences are also accepted. Theme configuration strings use the compact form `"PyPI|https://pypi.org/project/example/, Changelog|changelog.html"`.

External links open in a new browser tab and receive the appropriate `rel` attributes.

## Section navigator

Each `sidebar_tabs` mapping accepts these fields:

| Field         | Required | Description                                                                               |
| ------------- | -------- | ----------------------------------------------------------------------------------------- |
| `title`       | Yes      | Label displayed for the section. `name` is an alias.                                      |
| `url`         | No       | Section landing-page URL. `href` is an alias.                                             |
| `description` | No       | Supporting text displayed below the title.                                                |
| `icon`        | No       | Name from the built-in icon set.                                                          |
| `match`       | No       | Docname prefix used to mark the current section. Defaults to the directory part of `url`. |

```python
html_theme_options = {
    "sidebar_tabs": [
        {
            "title": "Guides",
            "url": "guides/index.html",
            "description": "Task-oriented documentation",
            "icon": "rocket",
            "match": "guides",
        },
        {
            "title": "Reference",
            "url": "reference/index.html",
            "description": "Technical details",
            "icon": "book",
            "match": "reference",
        },
    ],
}
```

The first tab is selected when no `match` prefix applies.

## Edit-page links

A GitHub repository URL produces edit links in this form:

```text
https://github.com/OWNER/REPOSITORY/edit/HEAD/{filename}
```

`edit_page_url_template` replaces that default. Supported placeholders are `{filename}`, `{path}`, and `{pagename}`. `{filename}` and `{path}` include the page's source suffix; `{pagename}` does not.

```python
html_theme_options = {
    "edit_page_url_template": "https://example.com/edit/main/{filename}",
}
```

## Color presets and variables

Color presets replace `--color-fd-primary` in both color modes. Entries in `light_css_variables` and `dark_css_variables` override the preset and may replace any theme design token:

```python
html_theme_options = {
    "color_preset": "purple",
    "light_css_variables": {
        "color-fd-background": "#fafafa",
        "color-fd-primary": "#7c3aed",
    },
    "dark_css_variables": {
        "color-fd-background": "#09090b",
        "color-fd-primary": "#c4b5fd",
    },
}
```

Variable names may include or omit the leading `--`. Color tokens are:

- `color-fd-background`
- `color-fd-foreground`
- `color-fd-muted`
- `color-fd-muted-foreground`
- `color-fd-popover`
- `color-fd-popover-foreground`
- `color-fd-card`
- `color-fd-card-foreground`
- `color-fd-border`
- `color-fd-primary`
- `color-fd-primary-foreground`
- `color-fd-secondary`
- `color-fd-secondary-foreground`
- `color-fd-accent`
- `color-fd-accent-foreground`
- `color-fd-ring`

Layout and typography tokens include `fd-sidebar-width`, `fd-toc-width`, `fd-page-width`, `fd-page-max`, `fd-radius`, `fd-font-sans`, and `fd-font-mono`.

## Page icons

The `icon` page metadata value and `sidebar_tabs[].icon` use the same built-in icon set.

```markdown
---
icon: terminal
---
```

Available names, in alphabetical order:

`album`, `blocks`, `book`, `bookmark`, `box`, `braces`, `bug`, `code`, `cog`, `compass`, `database`, `file`, `files`, `flask`, `folder`, `gauge`, `graduation-cap`, `layers`, `lightbulb`, `package`, `play`, `puzzle`, `rocket`, `server`, `settings`, `sparkles`, `terminal`, `test-tube`, `wrench`, `zap`.

Unknown names render no icon.

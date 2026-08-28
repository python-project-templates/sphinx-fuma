"""Normalisation of ``html_theme_options`` into template-friendly context values.

Sphinx passes theme options through as ``theme_<name>`` context entries whose
values are strings when they come from ``theme.conf`` and arbitrary Python
objects when they come from ``html_theme_options``. The templates want a single
normalised shape, so everything is coerced here rather than in Jinja.
"""

from html import escape

__all__ = ("build_context",)

_TRUTHY = {"1", "on", "true", "yes"}
_FALSY = {"0", "off", "false", "no", ""}

_LAYOUTS = ("docs", "notebook")
_TOC_STYLES = ("normal", "clerk")
_FONTS = ("bundled", "system")

# Each preset recolours ``--color-fd-primary`` only; the greys stay as they are.
# ``amber`` is the pairing fumadocs.dev itself uses.
_COLOR_PRESETS: dict[str, dict[str, dict[str, str]]] = {
    "neutral": {},
    "amber": {"light": {"color-fd-primary": "#cc8b00"}, "dark": {"color-fd-primary": "#fff383"}},
    "blue": {"light": {"color-fd-primary": "#1d4ed8"}, "dark": {"color-fd-primary": "#93c5fd"}},
    "emerald": {"light": {"color-fd-primary": "#047857"}, "dark": {"color-fd-primary": "#6ee7b7"}},
    "purple": {"light": {"color-fd-primary": "#6d28d9"}, "dark": {"color-fd-primary": "#c4b5fd"}},
    "rose": {"light": {"color-fd-primary": "#be123c"}, "dark": {"color-fd-primary": "#fda4af"}},
}


def _flag(value, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in _TRUTHY:
        return True
    if text in _FALSY:
        return False
    return default


def _integer(value, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _text(value) -> str:
    return "" if value is None else str(value).strip()


def _choice(value, allowed: tuple[str, ...], default: str) -> str:
    text = _text(value).lower()
    return text if text in allowed else default


def _links(value) -> list[dict[str, str]]:
    """Coerce ``nav_links`` into a list of ``{title, url, external}`` mappings.

    Accepts a list of mappings, a list of ``(title, url)`` pairs, or a
    ``"Title|url, Title|url"`` string for people configuring from TOML.
    """
    if not value:
        return []
    if isinstance(value, str):
        entries = []
        for chunk in value.split(","):
            title, _, url = chunk.partition("|")
            if title.strip() and url.strip():
                entries.append({"title": title.strip(), "url": url.strip()})
    else:
        entries = []
        for item in value:
            if isinstance(item, dict):
                title, url = _text(item.get("title") or item.get("name")), _text(item.get("url") or item.get("href"))
            elif isinstance(item, (list, tuple)) and len(item) == 2:
                title, url = _text(item[0]), _text(item[1])
            else:
                continue
            if title and url:
                entries.append({"title": title, "url": url})
    for entry in entries:
        entry["external"] = entry["url"].startswith(("http://", "https://", "//"))
    return entries


def _tabs(value, pagename: str) -> list[dict]:
    """Coerce ``sidebar_tabs`` into navigator entries and mark the active one.

    Accepts a list of mappings with ``title``, ``url`` and optional ``description``
    / ``icon`` / ``match``. The active tab is the one whose ``match`` prefix (or,
    failing that, the longest matching ``url`` stem) contains the current page.
    """
    if not value or isinstance(value, str):
        return []
    tabs = []
    for item in value:
        if not isinstance(item, dict):
            continue
        title, url = _text(item.get("title") or item.get("name")), _text(item.get("url") or item.get("href"))
        if not title:
            continue
        tabs.append(
            {
                "title": title,
                "url": url,
                "description": _text(item.get("description")),
                "icon": _text(item.get("icon")),
                "match": _text(item.get("match")) or url.rsplit("/", 1)[0],
                "active": False,
            }
        )
    best = None
    for tab in tabs:
        prefix = tab["match"].strip("/")
        if prefix and pagename.startswith(prefix) and (best is None or len(prefix) > len(best["match"].strip("/"))):
            best = tab
    if best is None and tabs:
        best = tabs[0]
    if best is not None:
        best["active"] = True
    return tabs


def _palette(preset_name, light, dark) -> tuple[dict, dict]:
    """Merge a named preset with the user's own variables, which take precedence."""
    preset = _COLOR_PRESETS.get(_text(preset_name).lower(), {})
    merged_light = dict(preset.get("light", {}))
    merged_dark = dict(preset.get("dark", {}))
    if isinstance(light, dict):
        merged_light.update(light)
    if isinstance(dark, dict):
        merged_dark.update(dark)
    return merged_light, merged_dark


def _css_overrides(light, dark) -> str:
    """Render ``light_css_variables``/``dark_css_variables`` as a stylesheet."""

    def block(selector: str, variables) -> str:
        if not isinstance(variables, dict) or not variables:
            return ""
        declarations = "".join(f"  {name if str(name).startswith('--') else f'--{name}'}: {value};\n" for name, value in variables.items())
        return f"{selector} {{\n{declarations}}}\n"

    dark_block = block("html.dark", dark)
    if dark_block:
        # Repeated for readers whose system prefers dark and who have no stored choice.
        dark_block += f"@media (prefers-color-scheme: dark) {{\n{block('html:not(.light)', dark)}}}\n"
    return f"{block(':root', light)}{dark_block}"


def _edit_url(template: str, pagename: str, suffix: str) -> str:
    if not template or not pagename:
        return ""
    filename = f"{pagename}{suffix or '.md'}"
    return template.replace("{filename}", filename).replace("{path}", filename).replace("{pagename}", pagename)


def build_context(context: dict) -> dict[str, object]:
    """Return the ``fuma_*`` context entries derived from the theme options."""
    github_url = _text(context.get("theme_github_url")).rstrip("/")
    edit_template = _text(context.get("theme_edit_page_url_template"))
    if not edit_template and github_url.startswith("https://github.com/"):
        edit_template = f"{github_url}/edit/HEAD/{{filename}}"
    tabs = _tabs(context.get("theme_sidebar_tabs"), _text(context.get("pagename")))
    light, dark = _palette(
        context.get("theme_color_preset"),
        context.get("theme_light_css_variables"),
        context.get("theme_dark_css_variables"),
    )
    return {
        "fuma_layout": _choice(context.get("theme_layout"), _LAYOUTS, "docs"),
        "fuma_toc_style": _choice(context.get("theme_toc_style"), _TOC_STYLES, "normal"),
        "fuma_fonts": _choice(context.get("theme_fonts"), _FONTS, "bundled"),
        "fuma_search": _flag(context.get("theme_search"), True),
        "fuma_sidebar_hide_name": _flag(context.get("theme_sidebar_hide_name")),
        "fuma_default_open_level": _integer(context.get("theme_default_open_level"), 1),
        "fuma_nav_links": _links(context.get("theme_nav_links")),
        "fuma_tabs": tabs,
        "fuma_active_tab": next((tab for tab in tabs if tab["active"]), {"title": "", "description": "", "icon": ""}),
        "fuma_github_url": github_url,
        "fuma_announcement": _text(context.get("theme_announcement")),
        "fuma_footer_text": _text(context.get("theme_footer_text")),
        "fuma_edit_url": escape(_edit_url(edit_template, _text(context.get("pagename")), _text(context.get("page_source_suffix"))), quote=True),
        "fuma_css_overrides": _css_overrides(light, dark),
    }

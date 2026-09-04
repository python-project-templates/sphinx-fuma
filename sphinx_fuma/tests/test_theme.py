from pathlib import Path

import pytest
from sphinx.application import Sphinx

from sphinx_fuma._options import build_context

CONF_PY = """
extensions = ["myst_parser", "sphinx_fuma"]
myst_enable_extensions = []
project = "Demo"
html_theme = "fuma"
html_theme_options = {
    "github_url": "https://github.com/example/demo",
    "nav_links": [{"title": "Blog", "url": "https://example.com/blog"}],
    "light_css_variables": {"color-fd-primary": "red"},
    "sidebar_tabs": [
        {"title": "Guides", "url": "guide.html", "description": "How to", "icon": "rocket", "match": "guide"},
        {"title": "Reference", "url": "index.html", "description": "Details", "icon": "book", "match": "index"},
    ],
}
"""

INDEX_MD = """
# Demo

Intro text.

```{toctree}
:caption: Guides

guide
```
"""

GUIDE_MD = """---
icon: rocket
---

# Guide

## First section

Content about widgets.

### Nested heading

More detail.

## Second section

Other content.

```{steps}
### Install it

Pull it down from the index.

### Run it

Start the server.
```

```{files}
- src/
  - app.py
- pyproject.toml
```
"""


@pytest.fixture(scope="module")
def built(tmp_path_factory) -> Path:
    src = tmp_path_factory.mktemp("src")
    (src / "conf.py").write_text(CONF_PY)
    (src / "index.md").write_text(INDEX_MD)
    (src / "guide.md").write_text(GUIDE_MD)
    out = src / "_build"
    Sphinx(str(src), str(src), str(out), str(out / ".doctrees"), "html", freshenv=True, status=None).build()
    return out


@pytest.fixture(scope="module")
def built_system_fonts(tmp_path_factory) -> Path:
    src = tmp_path_factory.mktemp("src_system_fonts")
    (src / "conf.py").write_text(
        'extensions = ["myst_parser", "sphinx_fuma"]\nproject = "Demo"\nhtml_theme = "fuma"\nhtml_theme_options = {"fonts": "system"}\n'
    )
    (src / "index.md").write_text("# Demo\n\nText.\n")
    out = src / "_build"
    Sphinx(str(src), str(src), str(out), str(out / ".doctrees"), "html", freshenv=True, status=None).build()
    return out


class TestBuildContext:
    def test_defaults(self):
        context = build_context({})
        assert context["fuma_layout"] == "docs"
        assert context["fuma_toc_style"] == "normal"
        assert context["fuma_search"] is True
        assert context["fuma_nav_links"] == []

    def test_invalid_choices_fall_back(self):
        context = build_context({"theme_layout": "spaceship", "theme_toc_style": "fancy"})
        assert context["fuma_layout"] == "docs"
        assert context["fuma_toc_style"] == "normal"

    def test_flags_accept_theme_conf_strings(self):
        assert build_context({"theme_search": "false"})["fuma_search"] is False
        assert build_context({"theme_sidebar_hide_name": "true"})["fuma_sidebar_hide_name"] is True

    def test_nav_links_from_string(self):
        links = build_context({"theme_nav_links": "Blog|https://example.com, Docs|/docs"})["fuma_nav_links"]
        assert links == [
            {"title": "Blog", "url": "https://example.com", "external": True},
            {"title": "Docs", "url": "/docs", "external": False},
        ]

    def test_nav_links_from_mappings(self):
        links = build_context({"theme_nav_links": [{"name": "API", "href": "/api"}]})["fuma_nav_links"]
        assert links == [{"title": "API", "url": "/api", "external": False}]

    def test_css_overrides_render_both_modes(self):
        css = build_context(
            {
                "theme_light_css_variables": {"color-fd-primary": "red"},
                "theme_dark_css_variables": {"--color-fd-primary": "blue"},
            }
        )["fuma_css_overrides"]
        assert ":root {\n  --color-fd-primary: red;\n}\n" in css
        assert "html.dark {\n  --color-fd-primary: blue;\n}\n" in css

    def test_dark_overrides_also_cover_system_preference(self):
        css = build_context({"theme_dark_css_variables": {"color-fd-primary": "blue"}})["fuma_css_overrides"]
        assert "@media (prefers-color-scheme: dark) {\nhtml:not(.light) {" in css

    def test_no_media_block_without_dark_overrides(self):
        css = build_context({"theme_light_css_variables": {"color-fd-primary": "red"}})["fuma_css_overrides"]
        assert "prefers-color-scheme" not in css

    def test_edit_url_derived_from_github_url(self):
        context = build_context(
            {
                "theme_github_url": "https://github.com/example/demo",
                "pagename": "guide",
                "page_source_suffix": ".md",
            }
        )
        assert context["fuma_edit_url"] == "https://github.com/example/demo/edit/HEAD/guide.md"

    def test_no_edit_url_without_a_page(self):
        assert build_context({"theme_github_url": "https://example.com/x"})["fuma_edit_url"] == ""


class TestRenderedOutput:
    def test_static_assets_are_copied(self, built):
        static = built / "_static"
        assert (static / "fuma.css").is_file()
        assert (static / "fuma-code.css").is_file()
        assert (static / "fuma.js").is_file()

    def test_bundled_fonts_are_shipped_and_linked(self, built):
        fonts = built / "_static" / "fonts"
        assert (fonts / "geist-latin-variable.woff2").is_file()
        assert (fonts / "jetbrains-mono-latin-variable.woff2").is_file()
        assert "fonts/fuma-fonts.css" in (built / "guide.html").read_text()

    def test_font_licences_travel_with_the_fonts(self, built):
        fonts = built / "_static" / "fonts"
        for name in ("Geist-LICENSE.txt", "JetBrainsMono-LICENSE.txt"):
            assert "SIL Open Font License" in (fonts / name).read_text()

    def test_layout_landmarks_are_present(self, built):
        html = (built / "guide.html").read_text()
        for landmark in ('id="fd-layout"', 'id="fd-subnav"', 'id="fd-sidebar"', 'id="fd-toc"', 'id="fd-main"'):
            assert landmark in html

    def test_navigation_lives_in_the_sidebar(self, built):
        html = (built / "guide.html").read_text()
        sidebar = html.split('id="fd-sidebar"', 1)[1].split("</aside>", 1)[0]
        assert "fd-brand" in sidebar
        assert "fd-search-trigger" in sidebar
        assert "fd-theme-switch" in sidebar

    def test_theme_switch_offers_both_modes(self, built):
        html = (built / "guide.html").read_text()
        assert 'data-fd-theme="light"' in html
        assert 'data-fd-theme="dark"' in html

    def test_page_icon_metadata_renders_in_the_sidebar(self, built):
        html = (built / "index.html").read_text()
        sidebar = html.split('id="fd-sidebar"', 1)[1].split("</aside>", 1)[0]
        assert "fd-link-icon" in sidebar

    def test_navigator_lists_tabs_and_marks_the_active_one(self, built):
        html = (built / "guide.html").read_text()
        assert "fd-navigator" in html
        assert "How to" in html and "Details" in html
        active = html.split('class="fd-navigator-option', 1)[1][:20]
        assert "fd-current" in active

    def test_toc_rail_is_an_svg_with_track_and_thumb(self, built):
        html = (built / "guide.html").read_text()
        assert 'class="fd-toc-rail"' in html
        assert 'class="fd-toc-track"' in html
        assert 'class="fd-toc-thumb"' in html

    def test_toc_scroll_spy_observes_headings_across_the_viewport(self, built):
        script = (built / "_static" / "fuma.js").read_text()
        assert 'anchor.querySelector("h1, h2, h3, h4, h5, h6")' in script
        assert "threshold: 0.9" in script
        assert "rootMargin:" not in script

    def test_toc_scroll_spy_marks_every_visible_item_active(self, built):
        script = (built / "_static" / "fuma.js").read_text()
        assert 'entry.item.classList.add("fd-active")' in script
        assert 'active[0].item.classList.add("fd-active")' not in script

    def test_tight_list_paragraphs_do_not_expand_item_spacing(self, built):
        stylesheet = (built / "_static" / "fuma.css").read_text()
        assert (".fd-prose ul.simple > li > p,\n.fd-prose ol.simple > li > p {\n  margin: 0;\n}") in stylesheet


class TestSteps:
    def test_directive_wraps_content_in_a_steps_container(self, built):
        assert 'class="fd-steps' in (built / "guide.html").read_text()

    def test_each_heading_becomes_a_step(self, built):
        html = (built / "guide.html").read_text()
        steps = html.split('class="fd-steps', 1)[1].split("</div>", 1)[0]
        assert steps.count('class="rubric"') == 2

    def test_step_bodies_are_preserved(self, built):
        html = (built / "guide.html").read_text()
        steps = html.split('class="fd-steps', 1)[1].split("</div>", 1)[0]
        assert "Pull it down" in steps


class TestFiles:
    def test_directive_builds_a_tree(self, built):
        assert 'class="fd-files' in (built / "guide.html").read_text()

    def test_trailing_slash_and_children_mark_folders(self, built):
        html = (built / "guide.html").read_text()
        tree = html.split("fd-files", 1)[1]
        assert tree.count("fd-folder-entry") == 1
        assert tree.count("fd-file-entry") == 2

    def test_folder_slash_is_stripped_from_the_label(self, built):
        html = (built / "guide.html").read_text()
        assert ">src<" in html
        assert ">src/<" not in html


class TestColorPresets:
    def test_amber_matches_the_fumadocs_pairing(self):
        css = build_context({"theme_color_preset": "amber"})["fuma_css_overrides"]
        assert "--color-fd-primary: #cc8b00;" in css
        assert "--color-fd-primary: #fff383;" in css

    def test_unknown_preset_changes_nothing(self):
        assert build_context({"theme_color_preset": "chartreuse"})["fuma_css_overrides"] == ""

    def test_default_is_the_neutral_greys(self):
        assert build_context({})["fuma_css_overrides"] == ""

    def test_explicit_variables_win_over_the_preset(self):
        css = build_context(
            {
                "theme_color_preset": "amber",
                "theme_dark_css_variables": {"color-fd-primary": "#ff0000"},
            }
        )["fuma_css_overrides"]
        assert "--color-fd-primary: #ff0000;" in css
        assert "#fff383" not in css

    def test_preset_still_supplies_the_other_mode(self):
        css = build_context(
            {
                "theme_color_preset": "amber",
                "theme_dark_css_variables": {"color-fd-primary": "#ff0000"},
            }
        )["fuma_css_overrides"]
        assert "--color-fd-primary: #cc8b00;" in css


class TestSystemFonts:
    def test_stylesheet_is_omitted(self, built_system_fonts):
        assert "fuma-fonts.css" not in (built_system_fonts / "index.html").read_text()

    def test_option_is_normalised(self):
        assert build_context({"theme_fonts": "system"})["fuma_fonts"] == "system"
        assert build_context({"theme_fonts": "nonsense"})["fuma_fonts"] == "bundled"
        assert build_context({})["fuma_fonts"] == "bundled"

    def test_sidebar_renders_the_toctree_caption_and_entries(self, built):
        html = (built / "index.html").read_text()
        assert 'class="fd-sidebar-caption">Guides<' in html
        assert 'href="guide.html"' in html

    def test_sidebar_lists_pages_not_headings(self, built):
        html = (built / "guide.html").read_text()
        sidebar = html.split('id="fd-sidebar"', 1)[1].split("</aside>", 1)[0]
        assert "First section" not in sidebar

    def test_active_page_is_marked_in_the_sidebar(self, built):
        assert "fd-link fd-current" in (built / "guide.html").read_text()

    def test_page_toc_uses_fragment_anchors(self, built):
        html = (built / "guide.html").read_text()
        assert 'href="#first-section"' in html
        assert 'href="#nested-section"' in html or 'href="#nested-heading"' in html

    def test_page_title_is_excluded_from_the_toc(self, built):
        html = (built / "guide.html").read_text()
        assert '<a href="#guide">' not in html

    def test_theme_options_reach_the_templates(self, built):
        html = (built / "guide.html").read_text()
        assert "https://github.com/example/demo" in html
        assert "https://example.com/blog" in html
        assert "--color-fd-primary: red;" in html

    def test_pagination_links_neighbouring_pages(self, built):
        assert 'class="fd-pagination"' in (built / "guide.html").read_text()

    def test_search_uses_searchlite_rather_than_its_own_index(self, built):
        assert (built / "_static" / "searchlite-index.json").is_file()
        assert not (built / "_static" / "fuma-search-index.json").exists()

    def test_theme_supplies_its_own_dialog(self, built):
        html = (built / "guide.html").read_text()
        assert 'id="fd-search-dialog"' in html
        # The bundled searchlite dialog would duplicate it.
        assert "searchlite-ui.js" not in html

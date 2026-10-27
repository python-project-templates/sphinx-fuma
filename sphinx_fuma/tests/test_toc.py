from pathlib import Path

import pytest
from sphinx.application import Sphinx


@pytest.fixture(scope="module", params=["docs", "notebook"])
def toc_site(tmp_path_factory, request) -> Path:
    src = tmp_path_factory.mktemp("toc")
    (src / "conf.py").write_text(
        'extensions = ["myst_parser", "sphinx_fuma"]\nproject = "Demo"\nhtml_theme = "fuma"\n'
        f'html_theme_options = {{"layout": "{request.param}", "github_url": "https://github.com/example/demo"}}\n'
    )
    pages = {
        "index.md": "# Demo\n\n## Welcome\n\n```{toctree}\n\nhidden\nvisible\nhidden-rst\n```\n",
        "hidden.md": "---\nhide-toc: true\n---\n\n# Hidden\n\n## Details\n\nContent.\n",
        "visible.md": "---\nhide-toc: false\n---\n\n# Visible\n\n## Details\n\nContent.\n",
        "hidden-rst.rst": ":hide-toc:\n\nHidden RST\n==========\n\nDetails\n-------\n\nContent.\n",
    }
    for name, content in pages.items():
        (src / name).write_text(content)
    out = src / "_build"
    Sphinx(str(src), str(src), str(out), str(out / ".doctrees"), "html", freshenv=True, status=None).build()
    return out


@pytest.mark.parametrize("page", ["hidden", "hidden-rst"])
def test_metadata_hides_desktop_and_mobile_navigation(toc_site, page):
    html = (toc_site / f"{page}.html").read_text()
    assert 'data-hide-toc="true"' in html
    for element in ("fd-toc", "fd-toc-restore", "fd-toc-popover", "fd-toc-mobile"):
        assert f'id="{element}"' not in html
    assert 'class="fd-toc-collapse"' not in html
    assert 'class="fd-toc-actions"' not in html
    assert 'id="details"' in html
    assert 'id="fd-sidebar"' in html


@pytest.mark.parametrize("page", ["index", "visible"])
def test_navigation_is_visible_by_default_and_when_explicitly_enabled(toc_site, page):
    html = (toc_site / f"{page}.html").read_text()
    assert 'data-hide-toc="true"' not in html
    for element in ("fd-toc", "fd-toc-restore", "fd-toc-popover", "fd-toc-mobile"):
        assert f'id="{element}"' in html
    assert 'fd-toc-collapse"' in html
    assert 'aria-label="Collapse page navigation"' in html
    assert 'aria-label="Expand page navigation"' in html
    assert 'aria-controls="fd-toc"' in html
    assert 'class="fd-toc-actions"' in html

import re
from pathlib import Path

import pytest
from sphinx.application import Sphinx


@pytest.fixture(scope="module", params=[None, 1, 2])
def sidebar_site(tmp_path_factory, request) -> tuple[Path, int | None]:
    src = tmp_path_factory.mktemp("sidebar")
    options = {} if request.param is None else {"default_open_level": request.param}
    (src / "conf.py").write_text(f'extensions = ["sphinx_fuma"]\nproject = "Demo"\nhtml_theme = "fuma"\nhtml_theme_options = {options!r}\n')
    pages = {
        "index": "Demo\n====\n\n.. toctree::\n\n   guides/index\n   autoapi/index\n",
        "guides/index": "Guides\n======\n\n.. toctree::\n\n   start\n",
        "guides/start": "Getting started\n===============\n\nInstall the package.\n",
        "autoapi/index": "API Reference\n=============\n\n.. toctree::\n\n   package/index\n",
        "autoapi/package/index": "Package\n=======\n\n.. toctree::\n\n   module\n",
        "autoapi/package/module": "Module\n======\n\nModule API.\n",
    }
    for name, content in pages.items():
        source = src / f"{name}.rst"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(content)
    out = src / "_build"
    Sphinx(str(src), str(src), str(out), str(out / ".doctrees"), "html", freshenv=True, status=None).build()
    return out, request.param


@pytest.mark.parametrize("page", ["index", "guides/start", "autoapi/index", "autoapi/package/module"])
def test_only_active_sidebar_sections_open_by_default(sidebar_site, page):
    out, open_level = sidebar_site
    html = (out / f"{page}.html").read_text()
    sidebar = html.split('id="fd-sidebar"', 1)[1].split("</aside>", 1)[0]
    folders = re.findall(r'<details class="fd-folder"([^>]*)>\s*<summary[^>]*>(.*?)</summary>', sidebar, re.DOTALL)
    state = {}
    for attrs, summary in folders:
        title = re.search(r'<span class="fd-link-text">([^<]+)</span>', summary)
        assert title is not None
        state[title.group(1)] = "open" in attrs
    assert state == {
        "Guides": page.startswith("guides/") or (open_level or 0) >= 1,
        "API Reference": page.startswith("autoapi/") or (open_level or 0) >= 1,
        "Package": page.startswith("autoapi/package/") or (open_level or 0) >= 2,
    }

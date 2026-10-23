import re
from pathlib import Path

import pytest
from sphinx.application import Sphinx


@pytest.fixture(scope="module", params=[True, False])
def built_llms(tmp_path_factory, request) -> tuple[Path, bool]:
    src = tmp_path_factory.mktemp("llms")
    (src / "conf.py").write_text(
        'extensions = ["myst_parser", "sphinx_fuma", "yardang.sphinx.llms"]\n'
        'project = "Demo"\nhtml_theme = "fuma"\n'
        f"yardang_llms_full_build = {request.param}\n"
    )
    (src / "index.md").write_text("# Demo\n\n```{toctree}\n\nguides/start\n```\n")
    (src / "guides").mkdir()
    (src / "guides/start.md").write_text("# Getting started\n\nInstall the package.\n")
    out = src / "_build"
    Sphinx(str(src), str(src), str(out), str(out / ".doctrees"), "html", freshenv=True, status=None).build()
    return out, request.param


@pytest.mark.parametrize("page", ["index.html", "guides/start.html"])
@pytest.mark.parametrize("region", ["fd-subnav", "fd-sidebar"])
def test_llms_menu_links_to_generated_files(built_llms, page, region):
    out, full_build = built_llms
    html = (out / page).read_text()
    region_html = html.split(f'id="{region}"', 1)[1].split("</header>" if region == "fd-subnav" else "</aside>", 1)[0]
    menu = re.search(r'<details class="fd-llms">(.*?)</details>', region_html, re.DOTALL)
    assert menu is not None
    assert 'aria-label="LLM documentation"' in menu.group(1)
    assert 'title="LLM documentation"' in menu.group(1)
    assert "fd-icon-bot" in menu.group(1)
    links = re.findall(r'<a href="([^"]+)">([^<]+)</a>', menu.group(1))
    filenames = ["llms.txt", "llms-full.txt"] if full_build else ["llms.txt"]
    assert [label for _, label in links] == filenames
    for href, label in links:
        assert (out / page).parent.joinpath(href).resolve() == out / label
        assert (out / label).is_file()

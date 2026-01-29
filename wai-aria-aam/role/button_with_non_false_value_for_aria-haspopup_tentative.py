import pytest
from sys import platform

TEST_HTML = [
    "<div id=test role=button aria-haspopup=true>click me</div>",
    "<div id=test role=button aria-haspopup=menu>click me</div>",
    "<div id=test role=button aria-haspopup=listbox>click me</div>",
    "<div id=test role=button aria-haspopup=tree>click me</div>",
    "<div id=test role=button aria-haspopup=grid>click me</div>",
    "<div id=test role=button aria-haspopup=dialog>click me</div>"
]

@pytest.mark.parametrize("html", TEST_HTML)
def test_atspi(atspi, session, inline, html):
    if not atspi:
        return

    session.url = inline(html)

    node = atspi.find_node("test", session.url)
    assert atspi.Accessible.get_role_name(node) == "button"

@pytest.mark.parametrize("html", TEST_HTML)
def test_axapi(axapi, session, inline, html):
    if not axapi:
        return

    session.url = inline(html)

    # Todo: Add test for AX API.

@pytest.mark.parametrize("html", TEST_HTML)
def test_ia2(ia2, session, inline, html):
    if not ia2:
        return

    session.url = inline(html)

    # Todo: Add test for IA2.

@pytest.mark.parametrize("html", TEST_HTML)
def test_uia(uia, session, inline, html):
    if not uia:
        return

    session.url = inline(html)

    # Todo: Add test for UIA.


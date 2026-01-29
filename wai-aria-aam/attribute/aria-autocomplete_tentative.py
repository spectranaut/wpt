import pytest
from sys import platform

TEST_HTML_BOTH = "<input role='combobox' id='test' aria-autocomplete='both'>"
TEST_HTML_INLINE = "<input role='combobox' id='test' aria-autocomplete='inline'>"
TEST_HTML_LIST = "<input role='combobox' id='test' aria-autocomplete='list'>"

def test_atspi_both(atspi, session, inline):
    if not atspi:
        return

    session.url = inline(TEST_HTML_BOTH)

    node = atspi.find_node("test", session.url)
    assert "autocomplete:both" in atspi.Accessible.get_attributes_as_array(node)
    assert "STATE_SUPPORTS_AUTOCOMPLETION" in atspi.get_state_list_helper(node)

def test_atspi_inline(atspi, session, inline):
    if not atspi:
        return

    session.url = inline(TEST_HTML_INLINE)

    node = atspi.find_node("test", session.url)
    assert "autocomplete:inline" in atspi.Accessible.get_attributes_as_array(node)
    assert "STATE_SUPPORTS_AUTOCOMPLETION" in atspi.get_state_list_helper(node)


def test_atspi_list(atspi, session, inline):
    if not atspi:
        return

    session.url = inline(TEST_HTML_LIST)

    node = atspi.find_node("test", session.url)
    assert "autocomplete:list" in atspi.Accessible.get_attributes_as_array(node)
    assert "STATE_SUPPORTS_AUTOCOMPLETION" in atspi.get_state_list_helper(node)


# Intentionally no AX API test, AX API does not map.

def test_ia2(ia2, session, inline):
    if not ia2:
        return

    session.url = inline(TEST_HTML_BOTH)

    # Todo: Add test for IA2.


# Intentionally no UIA test, UIA does not map.

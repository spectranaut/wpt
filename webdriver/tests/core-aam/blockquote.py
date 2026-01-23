import pytest


class TestAPI:

    # Note, the scope of this "function", which means it will run before each test function is called.
    # to run once for the class, we would need to specify: @pytest.fixture(autouse=True, scope="class")
    # HOWEVER, "session" is scoped to function, so it will through an error.
    # Todo, create a "session" scoped to class for this purpose?
    # otherwise... seems like a lot of extra work.
    @pytest.fixture(autouse=True)
    def setup(self, session, inline, full_configuration):
        self.session = session
        self.inline = inline
        self.full_configuration = full_configuration

    def test_atspi(self):
        print(f"Config capabilities: {self.full_configuration['capabilities']}")
        print(f"Session capabilities: {self.session.capabilities}")

        # Access the capabilities returned by the WebDriver session
        capabilities = self.session.capabilities

        # Check if goog:processID exists
        assert "goog:processID" in capabilities, "goog:processID not found in capabilities"

        # Check if it's a number (could be int or string of digits)
        process_id = capabilities["goog:processID"]
        if isinstance(process_id, str):
            assert process_id.isdigit(), f"goog:processID is not numeric: {process_id}"
        else:
            assert isinstance(process_id, int), f"goog:processID is not an int: {process_id}"

        print(f"goog:processID = {process_id}")

        # Todo, in base class, some kind of API impl based on OS
        # then expose:
        accessible = self.getAtspiAccessible()  # of type "Any"


# then windows will have others??? like get IAccessible2_2 ?
# then axapi will have something like getAXUIElement.... then also a bunch of other helper functions?
# and all of these are just not implemented on the othe platform?

from hammadcore.modules.text import Text
from hammadcore.modules.loaders import Spinner, ProgressBar

"""
hammadpy.core.core

The core module for the hammadpy package. Contains base hammadpy tools, and all
hammadpy-sm tools.

Example:
    core = Core()

Attributes:
    Core: A class for the core module.
"""

class Core:
    """
    A class for the core module.

    Attributes:
        text: A Text object for styling CLI output text.
    """
    def __init__(self):

        # Text Styling
        text = Text()
        self.say = text.say
        self.list = text.list

        # Loaders
        self.spinner = Spinner
        self.loader = ProgressBar

        pass

if __name__ == "__main__":
    core = Core()

    # Text Styling
    core.say("This has an underline!", underline=True)
    core.say("This is ITALIC!", italic=True)
    list_items = ["This is a list", "With some items", "And some colors"]
    core.list(list_items, color="blue", bg="white", bold=True)

    # Loaders
    with core.spinner(message="Loading", duration=5):
        # Perform some operation
        pass



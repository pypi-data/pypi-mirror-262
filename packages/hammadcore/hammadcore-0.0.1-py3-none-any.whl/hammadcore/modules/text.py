import libhammadpy_text

"""
hammadpy.core.text

This module provides a class for styling CLI output text. A wrapper on top of libhammadpy-text, a 
module built on rust.

Example:
    styles = Text()
    styles.say("This has an underline!", underline=True)
    styles.say("This is ITALIC!", italic=True)
    styles.say("This is blue", color="blue")
    styles.say("This is red", color="red")
    styles.say("This is red on blue", color="red", bg="blue")
    styles.say("This is also red on blue", color="red", bg="blue")
    styles.say("You can use RGB values too!", color="rgb(0, 255, 136)")
    styles.say("Background RGB truecolor also works :O", color="white", bg="rgb(135, 28, 167)")
    styles.say("You can also make bold comments", color="white", bold=True)
    styles.say("Or use any string type", color="cyan")
    styles.say("Or change advice. This is red", color="red")
    styles.say("Or clear things up. This is default color and style", color="red", bold=True)
    styles.say("Purple and magenta are the same", color="purple")
    styles.say("Bright colors are also allowed", color="bright_blue", bg="bright_white")
    styles.say("You can specify color by string", color="blue", bg="red")
    styles.say("And so are normal and clear", color="white")
    styles.say("This also works!", color="green", bold=True)

    padded_message = "Format works as expected. This will be padded".ljust(30)
    styles.say(padded_message, color="blue")

    truncated_message = "And this will be green but truncated to 3 chars"[:3]
    styles.say(truncated_message, color="green")

    list_items = ["This is a list", "With some items", "And some colors"]
    styles.list(list_items, color="blue", bg="white", bold=True)

Attributes:
    Text: A class for styling CLI output text.
"""

class Text:
    """
    A class for styling CLI output text.
    
    Attributes:
        say: A method to style and print a single line of text.
        list: A method to style and print a list of items.
    """
    def say(self, message, color="white", bg=None, bold=False, italic=False, underline=False):
        """
        Style and print a single line of text.

        Args:
            message (str): The message to be styled and printed.
            color (str, optional): The color of the text. Defaults to "white".
            bg (str, optional): The background color of the text. Defaults to None.
            bold (bool, optional): Whether the text should be bold. Defaults to False.
            italic (bool, optional): Whether the text should be italic. Defaults to False.
            underline (bool, optional): Whether the text should be underlined. Defaults to False.

        Returns:
            None
        """
        styled_message = libhammadpy_text.format_text(message, color, bg, bold, italic, underline)
        print(styled_message)

    def list(self, items, color="white", bg=None, bold=False, italic=False, underline=False):
        """
        Style and print a list of items.

        Args:
            items (list): The items to be styled and printed.
            color (str, optional): The color of the text. Defaults to "white".
            bg (str, optional): The background color of the text. Defaults to None.
            bold (bool, optional): Whether the text should be bold. Defaults to False.
            italic (bool, optional): Whether the text should be italic. Defaults to False.
            underline (bool, optional): Whether the text should be underlined. Defaults to False.

        Returns:
            None
        """
        styled_items = libhammadpy_text.format_list(items, color, bg, bold, italic, underline)
        for item in styled_items:
            print(item)

if __name__ == "__main__":
    styles = Text()
    styles.say("This has an underline!", underline=True)
    styles.say("This is ITALIC!", italic=True)
    styles.say("This is blue", color="blue")
    styles.say("This is red", color="red")
    styles.say("This is red on blue", color="red", bg="blue")
    styles.say("This is also red on blue", color="red", bg="blue")
    styles.say("You can use RGB values too!", color="rgb(0, 255, 136)")
    styles.say("Background RGB truecolor also works :O", color="white", bg="rgb(135, 28, 167)")
    styles.say("You can also make bold comments", color="white", bold=True)
    styles.say("Or use any string type", color="cyan")
    styles.say("Or change advice. This is red", color="red")
    styles.say("Or clear things up. This is default color and style", color="red", bold=True)
    styles.say("Purple and magenta are the same", color="purple")
    styles.say("Bright colors are also allowed", color="bright_blue", bg="bright_white")
    styles.say("You can specify color by string", color="blue", bg="red")
    styles.say("And so are normal and clear", color="white")
    styles.say("This also works!", color="green", bold=True)

    padded_message = "Format works as expected. This will be padded".ljust(30)
    styles.say(padded_message, color="blue")

    truncated_message = "And this will be green but truncated to 3 chars"[:3]
    styles.say(truncated_message, color="green")

    list_items = ["This is a list", "With some items", "And some colors"]
    styles.list(list_items, color="blue", bg="white", bold=True)
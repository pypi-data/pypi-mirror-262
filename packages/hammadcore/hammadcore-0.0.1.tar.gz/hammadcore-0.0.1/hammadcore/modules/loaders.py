import libhammadpy_loaders

"""
hammadpy.core.loaders

This module provides classes for displaying progress bars and spinners in the CLI.
It is a wrapper on top of libhammadpy_loaders, a module built with Rust.

Example:
    # Progress Bar
    total_items = 100
    with ProgressBar(message="Processing items", total=total_items) as progress:
        for i in range(total_items):
            # Perform some operation
            progress.update()

    # Spinner
    with Spinner(message="Loading", duration=5):
        # Perform some operation
        pass

Attributes:
    ProgressBar: A class for displaying a progress bar in the CLI.
    Spinner: A class for displaying a spinner in the CLI.
"""

class ProgressBar:
    """
    A class for displaying a progress bar in the CLI.

    Attributes:
        message (str): The message to display alongside the progress bar.
        total (int): The total number of items to process.
        style (str, optional): The style of the progress bar. Defaults to "default".
    """

    def __init__(self, message, total, style="default"):
        self.message = message
        self.total = total
        self.style = style
        self.current = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()

    def update(self, increment=1):
        """
        Update the progress bar by the specified increment.

        Args:
            increment (int, optional): The amount to increment the progress bar by. Defaults to 1.
        """
        self.current += increment
        libhammadpy_loaders.progress_bar(self.message, self.current, self.style)

    def finish(self):
        """
        Finish the progress bar and display a completion message.
        """
        libhammadpy_loaders.progress_bar(self.message, self.total, self.style)

class Spinner:
    """
    A class for displaying a spinner in the CLI.

    Attributes:
        message (str): The message to display alongside the spinner.
        duration (int): The duration (in seconds) for which the spinner should be displayed.
        style (str, optional): The style of the spinner. Defaults to "default".
    """

    def __init__(self, message, duration, style="default"):
        self.message = message
        self.duration = duration
        self.style = style

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()

    def start(self):
        """
        Start the spinner.
        """
        libhammadpy_loaders.spinner(self.message, self.duration, self.style)

    def finish(self):
        """
        Finish the spinner and display a completion message.
        """
        pass

if __name__ == "__main__":
    import time

    total_items = 5
    with ProgressBar(message="Processing items", total=total_items) as progress:
        for i in range(total_items):
            # Perform some operation
            progress.update()

    with Spinner(message="Loading", duration=2):
        time.sleep(2)
        pass
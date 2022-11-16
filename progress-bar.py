"""Container module for the ProgressBar class.

Author:
    Carlos Puente: @carlospuenteg
    Paulo Sanchez: @paulosanchez
"""


from time import perf_counter

import cursor
from colorama import Fore


class ProgressBar:
    """Progress bar generator class.

    This class is used to generate a progress bar based on the total amount of
    iterations of a given loop. It is updated using the current iteration
    inside the loop (this can be done selectively).

    It also provides with a timer to estimate the time remaining for the
    completion of the loop and a final elapsed time display.

    Args:
        total (int): Total amount of iterations of the loop.
        text (str, optional): Text to be displayed before the progress bar.
            Defaults to "Progress".
        width (int, optional): Width of the progress bar. Defaults to None.
            If None, the width is set to 80 - (len(text) + 15).
    """

    def __init__(self, total: int, text: str = "Progress",
                 width: int = None) -> None:

        self._start = None

        self.total = total
        self.text = text
        self.width = width

        self._progress = 1e-12

    @property
    def total(self) -> int:
        """Total amount of iterations of the loop.

        Returns:
            int: Total amount of iterations of the loop.
        """

        return self._total

    @total.setter
    def total(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Total iterations must be an integer.")

        self._total = value

    @property
    def text(self) -> str:
        """Text to be displayed before the progress bar.

        Returns:
            str: Text to be displayed before the progress bar.
        """

        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Text must be a string.")

        self._text = value

    @property
    def width(self) -> int:
        """Width of the progress bar.

        Returns:
            int: Width of the progress bar.
        """

        return self._width

    @width.setter
    def width(self, value: int) -> None:
        if value is not None and not isinstance(value, int):
            raise ValueError("Width must be an integer.")

        if value is None:
            self._width = 80 - (len(self._text) + 15)
        else:
            self._width = value

    @property
    def progress(self) -> float:
        """Progress bar progress.

        Returns:
            float: Progress bar progress.
        """

        return self._progress

    @property
    def elapsed(self) -> float:
        """Elapsed time at current status of the progress bar.

        Returns:
            float: Elapsed time at current status of the progress bar.
        """

        return perf_counter() - self._start

    @property
    def remaining(self) -> float:
        """Remaining time until loop end.

        Returns:
            float: Remaining time until loop end.
        """

        return (perf_counter() - self._start) / self._progress \
            * (1 - self._progress) + 1

    def update(self, current: int) -> None:
        """Progress bar update method.

        This method is used to update the progress bar based on the current
        iteration of the loop.

        Args:
            current (int): Current iteration of the loop.
        """

        # Time counter start on first update:

        if self._start is None:
            self._start = perf_counter()

        self._progress = (current ) / (self._total)  # Quick fix.

        percentage = round(self._progress * 100, 4)
        completed = round(self._progress * self._width)
        remaining = self._width - completed

        # Value boundary adjustments:

        percentage = percentage if percentage <= 100.00 else 100.00

        if self._progress < 0:
            self._progress = 1e-12
        elif self._progress > 1:
            return None

        SYMBOL = '━'
        ICON = '√' if self._progress == 1 else '@'
        COLORS = {
            "text": Fore.GREEN if self._progress == 1 else Fore.RED,
            "progress": Fore.GREEN if self._progress == 1 else Fore.YELLOW,
            "remaining": Fore.BLACK
        }

        # Cursor display:

        if self._progress == 1:
            cursor.show()
        else:
            cursor.hide()

        # Progress bar display:

        elapsed = perf_counter() - self._start

        eta = (elapsed / self._progress) * (1 - self._progress) + 1
        eta_format = f"{str(int(eta // 60)).zfill(2)}:{str(int(eta % 60)).zfill(2)}"
        percentage_format = f"{f'{percentage:.2f}'.rjust(6)} %"

        if self._progress < 1:
            print(
                f" {COLORS.get('text')}{ICON} {COLORS.get('text')}{self._text}"
                f" {COLORS.get('progress')}{SYMBOL * completed}"
                f"{COLORS.get('remaining')}{SYMBOL * remaining}"
                f" {COLORS.get('text')}{f'[{percentage_format}]'}"
                f" {COLORS.get('text')}ETA: {eta_format}",
                end='\r'
            )
        else:
            print(
                f" {COLORS.get('text')}{ICON} {COLORS.get('text')}{self._text}"
                f" {COLORS.get('progress')}{SYMBOL * completed}"
                f"{COLORS.get('remaining')}{SYMBOL * remaining}"
                f" {COLORS.get('text')}{f'[{percentage_format}]'}"
                f" {COLORS.get('text')}Elapsed: {elapsed:.2f}s",
                end='\n'
            )

        self.LAST = perf_counter()


if __name__ == "__main__":
    from time import sleep

    pb = ProgressBar(90, text="Progress")

    for i in range(101):
        pb.update(i)
        sleep(0.1)

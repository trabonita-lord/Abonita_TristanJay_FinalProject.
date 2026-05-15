"""Module representing the Habit entity.

This module contains the Habit class, which represents a single habit
tracked by the user, including its frequency and progress over time.
"""

class Habit:
    """Represents a habit with its name, frequency, and progress tracking.

    Attributes:
        name (str): The name of the habit.
        frequency (str): The frequency of the habit (e.g., 'daily', 'weekly').
        progress (dict): A dictionary mapping dates to a boolean completion status.
    """

    def __init__(self, name: str, frequency: str = "daily") -> None:
        """Initialize a new habit.

        Args:
            name (str): Name of the habit.
            frequency (str, optional): Frequency of the habit. Defaults to "daily".
        """
        self.name = name
        self.frequency = frequency
        self.progress = {}

    def mark_complete(self, date: str) -> None:
        """Mark the habit as complete for a given date.

        Args:
            date (str): The date to mark as complete (format: YYYY-MM-DD).
        """
        self.progress[date] = True

    def adjust_habit(self, new_name: str = None, new_frequency: str = None) -> None:
        """Adjust the habit's name or frequency.

        Args:
            new_name (str, optional): New name for the habit.
            new_frequency (str, optional): New frequency for the habit.
        """
        if new_name:
            self.name = new_name
        if new_frequency:
            self.frequency = new_frequency

    def get_progress(self) -> dict:
        """Get the progress dictionary of the habit.

        Returns:
            dict: Dictionary tracking habit completion progress.
        """
        return self.progress

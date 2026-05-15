"""Module representing the Pomodoro tracking entity.

This module contains the PomodoroTracker class, which tracks and counts
the user's pomodoro sessions.
"""

import time
from datetime import datetime

class PomodoroTracker:
    """Tracks Pomodoro sessions for productivity.

    Attributes:
        sessions (dict): Dictionary mapping dates to the number of completed sessions.
    """

    def __init__(self) -> None:
        """Initialize the Pomodoro tracker."""
        self.sessions = {}

    def start_timer(self, work_duration: int = 25, break_duration: int = 5) -> None:
        """Start a Pomodoro timer block.

        Args:
            work_duration (int, optional): Work duration in minutes. Defaults to 25.
            break_duration (int, optional): Break duration in minutes. Defaults to 5.
        """
        multiplier = 60 
        
        print(f"Starting Pomodoro timer: {work_duration} minutes of work.")
        total_work = work_duration * multiplier
        
        while total_work > 0:
            print(f"Working... {total_work} seconds remaining.", end="\r")
            time.sleep(1)
            total_work -= 1
            
        print("\nWork session complete! Take a short break.")
        
        total_break = break_duration * multiplier
        while total_break > 0:
            print(f"Resting... {total_break} seconds remaining.", end="\r")
            time.sleep(1)
            total_break -= 1
            
        print("\nBreak complete! Pomodoro session finished.")

    def log_session(self) -> None:
        """Log a completed Pomodoro session for today."""
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.sessions:
            self.sessions[today] = 0
        self.sessions[today] += 1
        print(f"Pomodoro session logged for {today}. Total: {self.sessions[today]} sessions.")

    def get_sessions(self, date: str) -> int:
        """Get the number of Pomodoro sessions for a specific date.

        Args:
            date (str): The date to check (format: YYYY-MM-DD).

        Returns:
            int: Number of sessions completed on the specified date.
        """
        return self.sessions.get(date, 0)

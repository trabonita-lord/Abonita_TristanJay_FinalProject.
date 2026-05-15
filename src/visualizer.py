"""Visualizer module.

Handles rendering of progress bars and daily CLI summaries.
"""

class ProgressVisualizer:
    """Handles data visualization for habits and productivity."""

    @staticmethod
    def draw_progress_bar(percentage: float, length: int = 20) -> str:
        """Draws a text-based progress bar.
        
        Args:
            percentage (float): Progress percentage (0.0 to 1.0).
            length (int, optional): Length of the bar in characters.
            
        Returns:
            str: A string representing a progress bar.
        """
        filled_length = int(length * percentage)
        bar = '█' * filled_length + '-' * (length - filled_length)
        return f"[{bar}] {int(percentage * 100)}%"

    @staticmethod
    def show_daily_summary(habits: list, date: str) -> None:
        """Shows a summary of all habits for a specific date.
        
        Demonstrates advanced processing using generator expressions and comprehensions.
        
        Args:
            habits (list): List of habit objects.
            date (str): Target date formatted as YYYY-MM-DD.
        """
        print(f"\n--- Daily Summary for {date} ---")
        if not habits:
            print("No habits to track.")
            return

        total_habits = len(habits)
        
        # Advanced Python: list comprehension and generator expression
        completed_habits_list = [h for h in habits if h.progress.get(date, False)]
        completed_count = len(completed_habits_list)

        for habit in habits:
            is_completed = habit.progress.get(date, False)
            status = "✅" if is_completed else "❌"
            print(f"{status} {habit.name} ({habit.frequency})")

        completion_rate = completed_count / total_habits if total_habits > 0 else 0
        print("\nOverall Progress:")
        print(ProgressVisualizer.draw_progress_bar(completion_rate))

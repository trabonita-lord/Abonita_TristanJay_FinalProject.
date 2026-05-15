"""Main logic module for Habit Tracker CLI application.

This script manages the command-line interface and coordinates interactions
between the user, the habit models, pomodoro tracker, and file handlers.
"""

from datetime import datetime
import os

from models.habit import Habit
from models.pomodoro import PomodoroTracker
from utils.file_handler import save_habits_to_file, load_habits_from_file
from utils.decorators import handle_cli_errors, time_execution
from visualizer import ProgressVisualizer

class Colors:
    """Color codes for CLI Styling."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Load habits from file at the start
habits = load_habits_from_file()
pomodoro_tracker = PomodoroTracker()


def clear_console():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_menu():
    """Display the main menu options."""
    print(f"\n{Colors.BOLD}{Colors.HEADER}=== 🌟 WELCOME TO HABIT TRACKER 🌟 ==={Colors.ENDC}")
    print(f"{Colors.CYAN}1.{Colors.ENDC} Add Habit")
    print(f"{Colors.CYAN}2.{Colors.ENDC} View Habits")
    print(f"{Colors.CYAN}3.{Colors.ENDC} Mark Habit as Complete")
    print(f"{Colors.CYAN}4.{Colors.ENDC} Remove Habit")
    print(f"{Colors.CYAN}5.{Colors.ENDC} Display Sorted Habits")
    print(f"{Colors.CYAN}6.{Colors.ENDC} Start Pomodoro Timer")
    print(f"{Colors.CYAN}7.{Colors.ENDC} View Pomodoro Sessions")
    print(f"{Colors.CYAN}8.{Colors.ENDC} View Daily Summary")
    print(f"{Colors.FAIL}9.{Colors.ENDC} Save and Exit")
    print(f"{Colors.HEADER}====================================={Colors.ENDC}")


@handle_cli_errors
def add_habit():
    """Add a new habit."""
    print(f"\n{Colors.BOLD}--- Add a New Habit ---{Colors.ENDC}")
    name = input("Enter the name of the habit: ").strip()
    if not name:
        raise ValueError("Habit name cannot be empty.")
        
    frequency = input("Enter the frequency (daily/weekly): ").lower().strip()
    if frequency not in ["daily", "weekly"]:
        print(f"{Colors.WARNING}Invalid frequency! Defaulting to 'daily'.{Colors.ENDC}")
        frequency = "daily"
        
    habit = Habit(name, frequency)
    habits.append(habit)
    print(f"{Colors.GREEN}✔ Habit '{name}' added successfully!{Colors.ENDC}")


@handle_cli_errors
def view_habits():
    """View all habits and their progress."""
    if not habits:
        print(f"{Colors.WARNING}No habits found!{Colors.ENDC}")
        return
        
    print(f"\n{Colors.BOLD}{Colors.BLUE}--- Your Habits ---{Colors.ENDC}")
    # Using generator expression and enumerate
    habit_lines = (
        f"{Colors.CYAN}{i}.{Colors.ENDC} {Colors.BOLD}{h.name}{Colors.ENDC} "
        f"({h.frequency}) - Logged dates: {list(h.get_progress().keys())}"
        for i, h in enumerate(habits, start=1)
    )
    for line in habit_lines:
        print(line)


@handle_cli_errors
def display_sorted_habits():
    """Advanced processing: Display habits sorted by completion count."""
    if not habits:
        print(f"{Colors.WARNING}No habits found!{Colors.ENDC}")
        return
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}--- Habits Ranked by Engagement ---{Colors.ENDC}")
    # Advanced logic: sorted with custom lambda key
    sorted_habits = sorted(habits, key=lambda h: len(h.progress), reverse=True)
    
    for i, h in enumerate(sorted_habits, start=1):
        count = len(h.progress)
        print(f"{Colors.CYAN}{i}.{Colors.ENDC} {h.name} - {count} times completed")


@handle_cli_errors
def mark_habit_complete():
    """Mark a habit as complete for today."""
    if not habits:
        print(f"{Colors.WARNING}No habits to mark as complete!{Colors.ENDC}")
        return
        
    view_habits()
    print("")
    choice_str = input("Select a habit to mark as complete: ")
    if not choice_str.isdigit():
        raise ValueError("Please enter a valid number!")
        
    choice = int(choice_str) - 1
    if 0 <= choice < len(habits):
        today = datetime.now().strftime("%Y-%m-%d")
        date_input = input(f"Enter the date (YYYY-MM-DD) or press Enter for today ({today}): ").strip()
        date = date_input if date_input else today
        
        habits[choice].mark_complete(date)
        print(f"{Colors.GREEN}✔ Habit '{habits[choice].name}' marked as complete for {date}!{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Invalid choice out of range!{Colors.ENDC}")


@handle_cli_errors
def remove_habit():
    """Remove a habit from the list."""
    if not habits:
        print(f"{Colors.WARNING}No habits to remove!{Colors.ENDC}")
        return
        
    view_habits()
    print("")
    choice_str = input("Select a habit to remove: ")
    if not choice_str.isdigit():
        raise ValueError("Please enter a valid number!")
        
    choice = int(choice_str) - 1
    if 0 <= choice < len(habits):
        removed_habit = habits.pop(choice)
        print(f"{Colors.GREEN}✔ Habit '{removed_habit.name}' removed successfully!{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Invalid choice out of range!{Colors.ENDC}")


@handle_cli_errors
def start_pomodoro():
    """Start a Pomodoro timer and log the session."""
    print(f"\n{Colors.BOLD}--- 🍅 Pomodoro Timer ---{Colors.ENDC}")
    work_input = input("Enter work duration in minutes (default: 25): ")
    break_input = input("Enter break duration in minutes (default: 5): ")
    
    work_duration = int(work_input) if work_input.isdigit() else 25
    break_duration = int(break_input) if break_input.isdigit() else 5
    
    pomodoro_tracker.start_timer(work_duration, break_duration)
    pomodoro_tracker.log_session()


@handle_cli_errors
def view_pomodoro_sessions():
    """View the total Pomodoro sessions for today."""
    today = datetime.now().strftime("%Y-%m-%d")
    total_sessions = pomodoro_tracker.get_sessions(today)
    print(f"\n{Colors.GREEN}🍅 Total Pomodoro sessions for today ({today}): {Colors.BOLD}{total_sessions}{Colors.ENDC}")


@handle_cli_errors
@time_execution
def view_daily_summary():
    """Shows the visual progress bar for today."""
    today = datetime.now().strftime("%Y-%m-%d")
    ProgressVisualizer.show_daily_summary(habits, today)


def main():
    """Main function to run the CLI menu."""
    clear_console()
    while True:
        display_menu()
        choice = input(f"{Colors.BOLD}Enter your choice: {Colors.ENDC}").strip()
        
        clear_console()
        if choice == "1":
            add_habit()
        elif choice == "2":
            view_habits()
        elif choice == "3":
            mark_habit_complete()
        elif choice == "4":
            remove_habit()
        elif choice == "5":
            display_sorted_habits()
        elif choice == "6":
            start_pomodoro()
        elif choice == "7":
            view_pomodoro_sessions()
        elif choice == "8":
            view_daily_summary()
        elif choice == "9":
            save_habits_to_file(habits)
            print(f"{Colors.BLUE}Goodbye, and stay productive! 👋{Colors.ENDC}")
            break
        else:
            print(f"{Colors.FAIL}Invalid choice! Please select a valid number.{Colors.ENDC}")

if __name__ == "__main__":
    main()

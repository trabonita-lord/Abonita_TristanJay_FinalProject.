"""File Handler utility module.

Provides functions to serialize and deserialize habit data to JSON,
demonstrating file handling and list/dict processing.
"""
import json
import os
from models.habit import Habit

def save_habits_to_file(habits: list, file_path: str = "data/habits.json") -> None:
    """Save the list of habits to a JSON file.

    Args:
        habits (list): List of Habit objects.
        file_path (str, optional): Path to the JSON file. Defaults to 'data/habits.json'.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Advanced: Dictionary comprehension inside a list comprehension
    data = [
        {
            "name": habit.name,
            "frequency": habit.frequency,
            "progress": habit.progress
        }
        for habit in habits
    ]
    
    # Advanced: Context Manager for file handling
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print("Habits saved successfully!")

def load_habits_from_file(file_path: str = "data/habits.json") -> list:
    """Load the list of habits from a JSON file.

    Args:
        file_path (str, optional): Path to the JSON file. Defaults to 'data/habits.json'.

    Returns:
        list: List of Habit objects.
    """
    try:
        if not os.path.exists(file_path):
            print("No saved habits found. Starting fresh!")
            return []
            
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if not content.strip():
                return []
            
            data = json.loads(content)
            habits = []
            for item in data:
                habit = Habit(item["name"], item.get("frequency", "daily"))
                habit.progress = item.get("progress", {})
                habits.append(habit)
            print("Habits loaded successfully!")
            return habits
            
    except json.JSONDecodeError:
        print("Corrupted habits file. Starting fresh!")
        return []
    except Exception as e:
        print(f"Error loading files: {e}")
        return []

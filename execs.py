"""
List of execs and their available dates

pre_term_sessions (int) refers to duties exec was scheduled for in the week(s) prior to orientation, defaults to 0
weekdays_not_available (list of strings) expects a list of values in {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}
specific_dates_unavailable (list of strings) expects a list of values in "YYYY-MM-DD" format
training_required (int) refers to number of training duties required, defaults to 0
"""

# Dictionary of execs with their details
EXEC_INFO = {
    "Jungwoo Kim": {
        "weekdays_not_available": ["Monday", "Thursday", "Saturday"],
        "specific_dates_unavailable": ["2024-06-14"]
    },
    "Ayyappan Arunachalam": {
        "weekdays_not_available": ["Monday", "Thursday"],
        "specific_dates_unavailable": [],
        "training_required": 2
    },
    "Felix Ren": {
        "weekdays_not_available": ["Monday", "Thursday", "Saturday"],
        "specific_dates_unavailable": []
    },
    "Molly Kim": {
        "weekdays_not_available": ["Monday", "Wednesday"],
        "specific_dates_unavailable": [],
        "pre_term_sessions": 2
    },
    "Rain Luo": {
        "weekdays_not_available": ["Tuesday", "Wednesday", "Friday"],
        "specific_dates_unavailable": [],
        "training_required": 2
    },
    "Richard Zhang": {
        "weekdays_not_available": ["Monday"],
        "specific_dates_unavailable": [],
        "pre_term_sessions": 3
    },
    "Max Jin": {
        "weekdays_not_available": ["Monday", "Thursday", "Saturday"],
        "specific_dates_unavailable": [],
        "pre_term_sessions": 3
    },
    "Ian MacDonald": {
        "weekdays_not_available": ["Monday", "Tuesday", "Thursday", "Saturday"],
        "specific_dates_unavailable": [],
        "pre_term_sessions": 3
    },
    "Bernard Lucas": {
        "weekdays_not_available": ["Monday", "Thursday"],
        "specific_dates_unavailable": ["2024-06-14", "2024-06-15", "2024-06-16", "2024-06-17", "2024-06-18", "2024-06-19", "2024-06-20", "2024-06-21"]
    },
    "Thomas Penner": {
        "weekdays_not_available": ["Monday", "Wednesday"],
        "specific_dates_unavailable": [],
        "pre_term_sessions": 3
    },
    "Andre Wen": {
        "weekdays_not_available": ["Monday", "Wednesday", "Friday"],
        "specific_dates_unavailable": [],
        "training_required": 2
    },
    "Howard Chan": {
        "weekdays_not_available": ["Wednesday", "Friday", "Saturday"],
        "specific_dates_unavailable": []
    },
    "Lisa Huynh": {
        "weekdays_not_available": ["Monday", "Wednesday", "Friday"],
        "specific_dates_unavailable": ["2024-05-18", "2024-05-25", "2024-06-08", "2024-06-29"]
    },
    "August Tan": {
        "weekdays_not_available": ["Tuesday"],
        "specific_dates_unavailable": [],
        "training_required": 2
    },
    "Ethan Truong": {
        "weekdays_not_available": ["Thursday", "Friday", "Saturday"],
        "specific_dates_unavailable": [],
        "training_required": 2
    },
    "Darren Shui": {
        "weekdays_not_available": ["Tuesday", "Wednesday", "Friday"],
        "specific_dates_unavailable": [],
        "training_required": 2
    },
    "Jack Wang": {
        "weekdays_not_available": ["Monday", "Tuesday", "Wednesday", "Thursday"],
        "specific_dates_unavailable": [],
        "training_required": 2
    },
    "Yang Lu": {
        "weekdays_not_available": ["Monday", "Thursday"],
        "specific_dates_unavailable": [],
        "training_required": 2
    },
    "Tina Qiu": {
        "weekdays_not_available": ["Wednesday", "Thursday", "Friday", "Saturday"],
        "specific_dates_unavailable": [],
        "training_required": 2
    },
    "Hubert Phu": {
        "weekdays_not_available": ["Tuesday"],
        "specific_dates_unavailable": ["2024-05-18", "2024-06-01", "2024-06-15", "2024-06-29"]
    }
}

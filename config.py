"""
Environment variables for exec_scheduler.py to be configured prior to running the script

FIRST_SESSION_DATE (string) and LAST_SESSION_DATE (string) expects "YYYY-MM-DD" format
SESSION_DAYS (list of strings) expects a list of values in {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}
DATES_WITHOUT_SESSIONS (list of strings) expects a list of values in "YYYY-MM-DD" format 
"""

# The first and last dates of the session
FIRST_SESSION_DATE = "2024-05-30"
LAST_SESSION_DATE = "2024-08-06"

# Weekdays when the sessions are held
SESSION_DAYS = ['Tuesday', 'Wednesday', 'Friday', 'Saturday']

# Specific dates when no sessions will be held (e.g., tournament dates)
DATES_WITHOUT_SESSIONS = ["2024-06-25", "2024-08-03"]

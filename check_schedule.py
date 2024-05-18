import csv
from dateutil.parser import parse
from execs import EXEC_INFO

# Configuration
LOG_FILE = 'exec_duties_log.txt'
SCHEDULE_FILE = 'exec_duties_schedule.csv'

checks_passed = True

# Read exec information
exec_info = {name: {
    'pre_term_sessions': info.get('pre_term_sessions', 0),
    'weekdays_not_available': info['weekdays_not_available'],
    'specific_dates_unavailable': [parse(date) for date in info['specific_dates_unavailable']],
    'training_required': info.get('training_required', 0)
} for name, info in EXEC_INFO.items()}

# Read log file to get the number of duties per exec
exec_duties = {}
with open(LOG_FILE, 'r') as logfile:
    for line in logfile:
        if ', total number of duties:' in line:
            parts = line.strip().split(',')
            name = parts[0]
            duties = int(parts[1].split(': ')[1])
            exec_duties[name] = duties

# Calculate average expected duties per exec
total_duties = sum(exec_duties.values())
total_execs = len(exec_info)
avg_duties_per_exec = total_duties / total_execs

# Check if any exec has abs(expected number of duties per exec - that exec's total number of duties) > 2
for name, duties in exec_duties.items():
    expected_duties = avg_duties_per_exec
    if abs(expected_duties - duties) > 2:
        checks_passed = False 
        print(f"Error: {name} has {duties} duties, which differs from the expected number by more than 2.")

# Read schedule file to check for invalid assignments and training sessions
exec_schedule = {}
with open(SCHEDULE_FILE, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        exec_name = row['Subject'].replace(" (T)", "")
        date = parse(row['Start Date'])
        if exec_name not in exec_schedule:
            exec_schedule[exec_name] = []
        exec_schedule[exec_name].append(date)

# Check if any exec was assigned duty on a day of the week or date they weren't supposed to be
weekday_mapping = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}

for name, dates in exec_schedule.items():
    weekdays_not_available = [weekday_mapping[day] for day in exec_info[name]['weekdays_not_available']]
    specific_dates_unavailable = exec_info[name]['specific_dates_unavailable']
    for date in dates:
        if date.weekday() in weekdays_not_available or date in specific_dates_unavailable:
            checks_passed = False
            print(f"Error: {name} was assigned duty on {date.strftime('%Y-%m-%d')} which they are not available for.")

# Check if any exec did not receive enough training sessions
training_sessions_required = {name: info['training_required'] for name, info in exec_info.items()}
training_sessions_assigned = {name: 0 for name in exec_info.keys()}

with open(SCHEDULE_FILE, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if " (T)" in row['Subject']:
            exec_name = row['Subject'].replace(" (T)", "")
            training_sessions_assigned[exec_name] += 1

for name, required in training_sessions_required.items():
    assigned = training_sessions_assigned[name]
    if assigned < required:
        checks_passed = False
        print(f"Warning: {name} did not receive enough training sessions. Assigned: {assigned}, Required: {required}")

# Check if every session has exactly three execs
with open(SCHEDULE_FILE, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    session_counts = {}
    for row in reader:
        date = parse(row['Start Date']).strftime('%Y-%m-%d')
        if date not in session_counts:
            session_counts[date] = 0
        session_counts[date] += 1

for date, count in session_counts.items():
    if count != 3:
        checks_passed = False
        print(f"Error: Session on {date} does not have exactly three execs. It has {count} exec(s).")

if checks_passed:
    print("All checks passed!")

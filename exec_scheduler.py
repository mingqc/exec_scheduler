import csv
import math
from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse
import numpy as np

# Import configurations
from config import FIRST_SESSION_DATE, LAST_SESSION_DATE, DATES_WITHOUT_SESSIONS, SESSION_DAYS
from execs import EXEC_INFO

# Convert string dates to datetime objects
first_session_date = parse(FIRST_SESSION_DATE)
last_session_date = parse(LAST_SESSION_DATE)
dates_without_sessions = [parse(date) for date in DATES_WITHOUT_SESSIONS]

# Mapping weekdays to dateutil constants
weekday_mapping = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}

# Create a list of all potential session dates
session_dates = list(rrule(DAILY, dtstart=first_session_date, until=last_session_date,
                            byweekday=[weekday_mapping[day] for day in SESSION_DAYS]))

# Remove no-session dates
session_dates = [date for date in session_dates if date not in dates_without_sessions]

# Prepare execs data structure
execs = {name: {
    'pre_term_sessions': info.get('pre_term_sessions', 0),
    'weekday_availability': [weekday_mapping[day] for day in info['weekdays_not_available']],
    'specific_dates_unavailable': [parse(date) for date in info['specific_dates_unavailable']],
    'training_required': info.get('training_required', 0)  # Default to 0 if not specified
} for name, info in EXEC_INFO.items()}

# Track assigned duties (excluding training duties)
exec_duties = {name: info['pre_term_sessions'] for name, info in execs.items()}
training_duties = {name: 0 for name in execs.keys()}  # Track assigned training duties separately

# Function to check if an exec is available on a given date
def is_available(exec_name, date):
    weekday = date.weekday()
    return weekday not in execs[exec_name]['weekday_availability'] and date not in execs[exec_name]['specific_dates_unavailable']

# Calculate the number of training sessions needed
total_training_needed = sum(execs[name]['training_required'] for name in execs)
num_training_sessions = math.ceil(total_training_needed / 3)

# Schedule training sessions
def schedule_training_sessions(session_dates, num_training_sessions):
    training_sessions = []
    session_index = 0

    while num_training_sessions > 0 and session_index < len(session_dates):
        date = session_dates[session_index]
        available_execs = [name for name in execs if is_available(name, date) and execs[name]['training_required'] > 0]

        if len(available_execs) >= 3:
            # Sort the available execs by training required in descending order
            available_execs.sort(key=lambda name: execs[name]['training_required'], reverse=True)

            # Select the top 3 execs
            assigned = available_execs[:3]

            for name in assigned:
                execs[name]['training_required'] -= 1
                training_duties[name] += 1

            training_sessions.append((date, [(name + " (T)") for name in assigned]))
            num_training_sessions -= 1

        session_index += 1

    # Ensure remaining session duties are assigned if we have less than 3 available execs
    while num_training_sessions > 0 and session_index < len(session_dates):
        date = session_dates[session_index]
        available_execs = [name for name in execs if is_available(name, date) and execs[name]['training_required'] > 0]
        if available_execs:
            assigned = np.random.choice(available_execs, min(len(available_execs), 3), replace=False)
            for name in assigned:
                exec_duties[name] += 1
            training_sessions.append((date, [name for name in assigned]))
            num_training_sessions -= 1
        session_index += 1
    
    return training_sessions

# Ensure each exec is assigned enough duties to balance the total
def get_duties_per_exec():
    total_sessions = len(session_dates)
    total_duties_needed = total_sessions * 3
    for name in execs:
        total_duties_needed -= exec_duties[name]
    exec_duties_needed = {name: total_duties_needed // len(execs) for name in execs}
    remainder = total_duties_needed % len(execs)
    sorted_execs = sorted(execs.keys(), key=lambda x: exec_duties[x])

    for i in range(remainder):
        exec_duties_needed[sorted_execs[i]] += 1

    return exec_duties_needed

exec_duties_needed = get_duties_per_exec()

# Adjust exec_duties to include the calculated needed duties
for name in exec_duties_needed:
    exec_duties[name] += exec_duties_needed[name]

# Schedule regular sessions
def schedule_regular_sessions(session_dates, training_sessions):
    regular_sessions = []
    exec_queue = []
    session_dates_set = set(session_dates)  # Convert to set for quick lookup
    training_dates = {date for date, _ in training_sessions}

    # Priority queue for execs based on current duties to balance the load
    def get_next_exec():
        execs_sorted = sorted(execs.keys(), key=lambda x: exec_duties[x])
        for exec_name in execs_sorted:
            if exec_name not in exec_queue:
                return exec_name

    for date in session_dates:
        if date in training_dates:
            continue  # Skip training dates

        assigned_execs = []

        # First try to assign execs from the queue
        for queued_exec in exec_queue[:]:
            if is_available(queued_exec, date):
                assigned_execs.append(queued_exec)
                exec_queue.remove(queued_exec)
                if len(assigned_execs) == 3:
                    break

        # Assign remaining slots using priority queue
        while len(assigned_execs) < 3:
            exec_name = get_next_exec()
            if is_available(exec_name, date) and exec_name not in assigned_execs:
                assigned_execs.append(exec_name)
            else:
                exec_queue.append(exec_name)

        # Ensure we have exactly 3 assigned execs
        while len(assigned_execs) < 3:
            next_exec = exec_queue.pop(0)
            assigned_execs.append(next_exec)

        for exec_name in assigned_execs:
            exec_duties[exec_name] += 1

        regular_sessions.append((date, assigned_execs))

    return regular_sessions

# Generate schedule
training_sessions = schedule_training_sessions(session_dates, num_training_sessions)
regular_sessions = schedule_regular_sessions(session_dates, training_sessions)

# Rebalance duties
def rebalance_duties(regular_sessions):
    min_duties = min(exec_duties.values())
    max_duties = max(exec_duties.values())

    while max_duties - min_duties > 1:
        # Find exec with max and min duties
        max_exec = max(exec_duties, key=exec_duties.get)
        min_exec = min(exec_duties, key=exec_duties.get)

        # Find a duty to swap
        for date, execs in regular_sessions:
            if max_exec in execs and is_available(min_exec, date):
                execs[execs.index(max_exec)] = min_exec
                exec_duties[max_exec] -= 1
                exec_duties[min_exec] += 1
                break

        min_duties = min(exec_duties.values())
        max_duties = max(exec_duties.values())

rebalance_duties(regular_sessions)

# Output schedule
def generate_google_calendar_output(sessions):
    events = []
    for date, execs in sessions:
        for exec in execs:
            event = {
                'Subject': exec,
                'Start Date': date.strftime('%Y-%m-%d'),
                'Start Time': '',
                'End Date': date.strftime('%Y-%m-%d'),
                'End Time': '',
                'All Day Event': 'True',
                'Description': '',
                'Location': '',
                'Private': 'True'
            }
            events.append(event)
    return events

# Combine sessions
combined_sessions = training_sessions + regular_sessions

# Output to Google Calendar format
google_calendar_events = generate_google_calendar_output(combined_sessions)

# Write to CSV file
with open('exec_duties_schedule.csv', 'w', newline='') as csvfile:
    fieldnames = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'All Day Event', 'Description', 'Location', 'Private']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for event in google_calendar_events:
        writer.writerow(event)

print("Schedule has been written to exec_duties_schedule.csv")

# Calculate total number of duties (including pre-term duties but excluding training duties)
total_duties = sum(exec_duties.values())

# Calculate the total number of execs
total_execs = len(execs)

# Calculate the average expected number of duties per exec
avg_duties_per_exec = total_duties / total_execs

# Write to log file
with open('exec_duties_log.txt', 'w') as logfile:
    # Log execs who did not receive enough training
    for name, required_training in training_duties.items():
        if execs[name]['training_required'] > 0:
            logfile.write(f"WARNING: {name} did not receive enough training sessions. Assigned: {required_training}\n")
            logfile.write("\n")

    logfile.write(f"Total number of duties (including pre-term duties): {total_duties}\n")
    logfile.write(f"Total number of execs: {total_execs}\n")
    logfile.write(f"Average expected number of duties per exec: {avg_duties_per_exec:.2f}\n\n")
    for name, duties in exec_duties.items():
        pre_term_duties = execs[name]['pre_term_sessions']
        training_duty_count = training_duties[name]
        log_message = f"{name}, total number of duties: {duties}"
        if pre_term_duties > 0:
            log_message += f", pre-term duties: {pre_term_duties}"
        if training_duty_count > 0:
            log_message += ", training duties not included"
        logfile.write(log_message + "\n")


print("Log has been written to exec_duties_log.txt")

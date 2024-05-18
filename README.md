# Exec Duties Scheduler

This script generates the exec duties schedule for a club. Note that training session duties may require manual swaps.

## Setup

### Virtual Environment

To set up a virtual environment, run:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Note: if on Windows, instead of `source venv/bin/activate`, run:

```bash
venv\Scripts\activate
```

Deactivate your virtual environment with:

```bash
deactivate
```

## Configuration

Before generating the schedule, add exec details in `exec.py` and adjust parameters in `config.py`.

## Generating the Schedule

To generate the exec schedule, run:

```bash
python3 exec_scheduler.py
```

## Sanity Check

Run a sanity check with:

```bash
python3 check_schedule.py
```

This reads from the generated CSV and log files to check that:

1. Greatest number of duties - Fewest number of duties < 2
2. Availability constraints are met
3. Training sessions were assigned properly
4. Each session has exactly three execs (TODO: set this to be configurable)

## Output

The resulting output is in `exec_duties_schedule.csv`. This can be imported directly into Google Calendar:
1. Go to Calendar
2. Click on the Settings Gear Icon
3. Select `Import`

For more information, view the logs at `exec_duties_log.txt`.

If any exec cannot make a training session, then this will be outputted.

## Important Notes

- **Pre-term duties** refer to duties assigned prior to orientation.
- **Training sessions** are intentionally not counted in the number of exec duties (we want them to get more practice!).
- **Training scheduling**: The check is expected to fail since we do not use a backtracking algorithm. Adjustments will be made manually.
- **Scheduling algorithm**: Uses a round-robin with a priority queue and naive rebalancing.

## TODO

- Add an environment variable to set `execs_per_session` depending on the weekday, as some terms may not always have three execs.



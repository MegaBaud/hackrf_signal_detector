# Alert logic for SDR carrier wave detection

import collections, datetime

# Could alternatively use max values for alerting, but it produces a LOT of alert toggling.
# Using the average of the past 50 averages.
THRESHOLD = 3.0  # Change as desired (TODO make this a param)
ALERT_FILE = 'ALERTS.txt'

def compare_and_update_alerts(running_metadata_db, baseline_db, active_alerts, f=ALERT_FILE):
    """
    Compare frequency dB metadata to the baseline, producing alerts if necessary.

    database format:  db[freq][0] is min, db[freq][1] is max, and db[freq][2] is a deque of averages.

    active_alerts is a dict of all frequences, set to None if no alert, and a timestamp if alert exists.
    """
    temp_alerts_list = list()

    # get a list of active alerts
    for freq in running_metadata_db:
        # Averages comparison
        if sum(running_metadata_db[freq][2]) / len(running_metadata_db[freq][2]) - THRESHOLD > sum(baseline_db[freq][2]) / len(baseline_db):
        # max value comparison
        # if running_metadata_db[freq][1] > baseline_db[freq][1] + THRESHOLD:
            temp_alerts_list.append(freq)
    
    # DEBUG - check calculations for specific frequencies
    # print()


    # check active alerts - have any gone away?
    for freq in active_alerts:
        if active_alerts[freq]:
            if freq not in temp_alerts_list:
                # Remove alerts not present from data structure, but log to file when the alert went away
                with open(f, 'a') as a_file:
                    a_file.write('{}  {} Hz previously detected at {} fallen below threshold.\n'.format(
                              datetime.datetime.now(), freq, active_alerts[freq]) )
                active_alerts[freq] = None

    # now log any new alerts
    for freq in temp_alerts_list:
        if not active_alerts.get(freq):  # only write a new timestamp if it doesn't exist
            t = datetime.datetime.now()
            active_alerts[freq] = t
            with open(f, 'a') as a_file:
                a_file.write('{}  {} Hz detected at {:.2f} dB, {:.2f} dB higher than the baseline max.\n'.format(
                              t, freq, running_metadata_db[freq][1], running_metadata_db[freq][1] - baseline_db[freq][1]) )

def generate_alerts_db(db):
    active_alerts = dict()
    for freq in db:
        active_alerts[freq] = None
    return active_alerts

        

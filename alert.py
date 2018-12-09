# Alert logic for SDR carrier wave detection

import collections, datetime

THRESHOLD = 3.0  # 3 dB increase is default alert behavior, change as desired
ALERT_FILE = 'ALERTS.txt'

def compare_and_update_alerts(running_metadata_db, baseline_db, active_alerts, f=ALERT_FILE):
    """
    Compare and produce alerts, if necessary.

    db[freq][0] is min, db[freq][1] is max, and db[freq][2] is a deque of averages.
    """
    temp_alerts_list = list()

    # get a list of alerts
    for freq in running_metadata_db:
        if running_metadata_db[freq][1] > baseline_db[freq][1] + THRESHOLD:
            temp_alerts_list.append(freq)

    # check active alerts - have any gone away?
    for freq in active_alerts:
        if freq not in temp_alerts_list:
            # Remove alerts not present anymore, but log when they occured
            with open(f, 'a') as a_file:
                a_file.write('{}  {} Hz previously detected at {} fallen below threshold.\n'.format(
                              datetime.datetime.now(), freq, active_alerts[freq]) )
            active_alerts[freq] = None

    # now log any new alerts
    for freq in temp_alerts_list:
        if not active_alerts.get(freq):
            t = datetime.datetime.now()
            active_alerts[freq] = t
            with open(f, 'a') as a_file:
                a_file.write('{}  {} Hz detected at {}dB, {} higher than the baseline max.\n'.format(
                              t, freq, baseline_db[freq][1], baseline_db[freq][1] - running_metadata_db[freq][1]) )

def generate_alerts_db(db):
    active_alerts = dict()
    for freq in db:
        active_alerts[freq] = 'dummyTimestamp'
    return active_alerts

        

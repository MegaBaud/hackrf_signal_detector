# Use hackrf_sweep to keep track of average dB

def generateDB(F_start, F_end, step):
"""
create a dict database (JSON?) (use a 3rd party DB maybe?) to keep track
of each frequency's dB during the spectrum sweep.

Example output of the hackrf_sweep:
    2018-12-03, 21:09:42, 2400000000, 2405000000, 1000000.00, 20, -65.12, -65.81, -60.12, -56.41, -60.79
    2018-12-03, 21:09:42, 2410000000, 2415000000, 1000000.00, 20, -66.18, -69.06, -64.06, -61.60, -74.51
    2018-12-03, 21:09:42, 2405000000, 2410000000, 1000000.00, 20, -68.33, -66.74, -66.00, -75.13, -63.93
    2018-12-03, 21:09:42, 2415000000, 2420000000, 1000000.00, 20, -60.17, -72.45, -64.26, -66.47, -59.21

Keep track of date, time (note, 24hr turnover bugs? TODO), frequency bin, and the list of dBs
"""
    if F_start + step >= F_end:
        print('Starting Frequency + step must be lower than Ending Frequency')
        return None
    db = dict() # Possibly add samples or other metadata here
    
    for i in range(F_start, F_end, step):
        db[F_start] = {avg=float('-inf'), data=list()}

    return db



    

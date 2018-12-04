# Use hackrf_sweep to keep track of average dB

import collections

NUM_STORED_DATA_POINTS = 50
NUM_STORED_AVERAGES = 50

def read_data(file_loc, data_db, deque_length=NUM_STORED_DATA_POINTS):
    """Injest hackrf_sweep data.  Example data:

      date, time, hz_low, hz_high, hz_bin_width, num_samples, dB readings in time
    2018-12-03, 22:25:45, 2400000000, 2405000000, 1000000.00, 20, -60.82, -65.38, -72.08, -67.92, -63.53
    2018-12-03, 22:25:45, 2410000000, 2415000000, 1000000.00, 20, -71.69, -62.32, -68.31, -64.31, -61.38
    2018-12-03, 22:25:45, 2405000000, 2410000000, 1000000.00, 20, -66.88, -61.43, -63.67, -68.80, -82.03
    2018-12-03, 22:25:45, 2415000000, 2420000000, 1000000.00, 20, -64.02, -60.92, -61.43, -63.24, -69.91

    data_db format:
    { low_hz0: deque([dB0, dB1, dB2, ...], maxlen=deque_length),
      low_hz1:...
    }
    """
    with open(file_loc, 'r') as f:
        for line in f:
            x = line.split()
            
            low_hz = x[2]
            current_hz = data_db.get(low_hz)
            
            # does the DB entry exist?
            if not current_hz:
                data_db[low_hz] = collections.deque(maxlen=deque_length)

            # stick the newest entries in the DB.  Deque will overwrite the oldest data
            for i in x[6:]:
                data_db[low_hz].append(i)


def update_averages(avg_db, data_db, deque_length=NUM_STORED_AVERAGES):
    """Update the averages in avg_db based on updates to data_db.

    avg_db format:
    { low_hz0: deque([avg0, avg1, avg2, ...], maxlen=deque_length),
      low_hz1:...
    }
    """
    if num_samples_to_avg > deque_length:
        print('ERROR:  Cannot average more than stored amount.')

    for freq in data_db:
        current_hz = avg_db.get(freq)

        # does the DB entry exist?
        if not current_hz:
            avg_db[freq] = collections.deque(maxlen=deque_length)

        # update the avg DB.  Deque will overwrite the oldest data
        avg_db[freq].append(sum(data_db[freq]) / len(data_db[freq]))



        

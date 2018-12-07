# Parse the output of hackrf_sweep to keep track of average dB

import collections

NUM_STORED_DATA_POINTS = 50
NUM_STORED_AVERAGES = 50

def read_data(file_loc, data_db, metadata_db, update=True, data_deque_length=NUM_STORED_DATA_POINTS, metadata_deque_length=NUM_STORED_AVERAGES):
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
            x = line.split(',')
            
            low_hz = int(x[2])
            current_hz = data_db.get(low_hz)
            
            # does the DB entry exist?
            if not current_hz:
                data_db[low_hz] = collections.deque(maxlen=data_deque_length)

            # stick the newest entries in the DB.  Deque will overwrite the oldest data
            for i in x[6:]:
                data_db[low_hz].append(float(i))

    if update:
        for freq in data_db:
            if not metadata_db.get(freq):  # must create deque if it doesn't exist
                metadata_db[freq] = [-100.0, -60.0, collections.deque(maxlen=metadata_deque_length)]
            
            # For each frequency, update min, max, and current average.
            metadata_db[freq][0] = min(data_db[freq])
            metadata_db[freq][1] = max(data_db[freq])
            metadata_db[freq][2].append(sum(data_db[freq]) / len(data_db[freq]))

        

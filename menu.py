# SDR Menu - start here

import copy, os, subprocess, sys, time
from alert import compare_and_update_alerts, generate_alerts_db
from db_funct import read_data

NUM_DATA_FILES_TO_KEEP = 50
PROJ_DIRECTORY = '/home/rock64/SDR/hackrf_signal_detector'


def get_sdr_data(f_name):
    sdr_cmd = 'hackrf_sweep -1 -n 32768 > {}'.format(f_name)

    print('Now calling "{}"'.format(sdr_cmd))
    subprocess.call(sdr_cmd, stdout=subprocess.DEVNULL, shell=True) # Here be dragons
    subprocess.call('clear', shell=True)


def get_dummy_baseline(data_db, metadata_db, use_prev=False):
    if not use_prev:
        base_dir = '/home/rock64/SDR/hackrf_signal_detector/data'
        baseline_files = [os.path.join(base_dir, 'top_bench/top_bench32768_{0:02d}.txt'.format(i)) for i in range(50)]
    else:
        base_dir = '/home/rock64/SDR/hackrf_signal_detector/baseline_data'
        baseline_files = [os.path.join(base_dir, 'spectrum_data{0:02d}.txt'.format(i)) for i in range(NUM_DATA_FILES_TO_KEEP)]

    print('Processing previously recorded baseline...', end='')
    for f_name in baseline_files:
        # We have 50 baseline spectrum files, so could use a data deque length of 250 (5 samples per freq).
        # But since dummy data is usually 10 samples (50 data points).... test different performances
        read_data(f_name, data_db, metadata_db, True, 50, 20)
        print('.',end='')
        sys.stdout.flush()

    print('\n')
    return copy.deepcopy(metadata_db)


def get_spectrum_baseline(data_db, metadata_db):
    # arbitrarily choosing 50 samples, should probably do more
    for i in range(NUM_DATA_FILES_TO_KEEP):
        f_name = os.path.join(PROJ_DIRECTORY, 'baseline_data/spectrum_data{0:02d}.txt'.format(i))
        get_sdr_data(f_name)
        read_data(f_name, data_db, metadata_db, True, 50, 20)

    return copy.deepcopy(metadata_db)


def start():
    subprocess.call('clear', shell=True)
    print('\n\n\n' + ' '*10 + '*'*34)
    print(' '*10 + '**  SDR Carrier Wave Dectector  **')
    print(' '*10 + '*'*34 + '\n\n\n')

    print('Press enter when ready to begin scanning.  This will become the spectrum baseline to compare later.')
    return input()

def main():
    start()
    
    data_db, metadata_db, baseline_db = dict(), dict(), dict()
    
    # If script is called with DEBUG, use dummy data.  Otherwise scan
    debug, use_prev = False, False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'DEBUG':
            debug = True
        elif sys.argv[1] == 'USE_PREV_BASELINE':
            use_prev = True
        else:
            print('Invalid input.  Run script with "DEBUG" param or no params at all.')
            sys.exit()

    if debug or use_prev:
        baseline_db = get_dummy_baseline(data_db, metadata_db, use_prev)
    else:
        baseline_db = get_spectrum_baseline(data_db, metadata_db)
     
    # Now we have the min, max, and average of our spectrum stored in baseline_db for alert comparisons.
    _ = 'Use the following two commands in separate windows to track the scans:' \
        '\n    python3 dashboard.py    <-- this will show you min/max/average frequency data in bins around a frequency.' \
        '\n    tail ALERTS.txt         <-- this will output any new alerts, or removal of old alerts.'
    input('Baseline obtained!  Press enter to start perpetual scanning.\n\n' + _)
    
    active_alerts = generate_alerts_db(data_db)  # dict of all frequencies, set to None
    
    if debug:
        # Loop through dummy data file of choice
        base_dir = '/home/rock64/SDR/hackrf_signal_detector/data'
        baseline_files =     [os.path.join(base_dir, 'top_bench/top_bench32768_{0:02d}.txt'.format(i)) for i in range(50)]
        rf_1010Mhz_0dB =     [os.path.join(base_dir, 'rf_source/top_bench/1010Mhz/00dB_top_bench32768_{}.txt'.format(i)) for i in range(10)]
        rf_1010Mhz_neg10dB = [os.path.join(base_dir, 'rf_source/top_bench/1010Mhz/-10dB_top_bench32768_{}.txt'.format(i)) for i in range(10)]
        rf_960Mhz_0dB =      [os.path.join(base_dir, 'rf_source/top_bench/960Mhz/00dB_top_bench32768_{}.txt'.format(i)) for i in range(10)]
        rf_960Mhz_neg10dB =  [os.path.join(base_dir, 'rf_source/top_bench/960Mhz/-10dB_top_bench32768_{}.txt'.format(i)) for i in range(10)]
        rf_750Mhz_0dB =      [os.path.join(base_dir, 'rf_source/top_bench/750Mhz/00dB_top_bench32768_{}.txt'.format(i)) for i in range(10)]
        rf_750Mhz_neg10dB =  [os.path.join(base_dir, 'rf_source/top_bench/750Mhz/-10dB_top_bench32768_{}.txt'.format(i)) for i in range(10)]

        data_file_to_use = rf_1010Mhz_0dB

        while True:  # ctrl+c to exit
            # go back and forth between the data file and spectrum data to re-establish baseline
            for i in range(5):
                for f_name in data_file_to_use:
                    read_data(f_name, data_db, metadata_db, True, 50, 20, baseline_db)
                    compare_and_update_alerts(metadata_db, baseline_db, active_alerts)
                    time.sleep(0.02)
                print('Loop {} of 5 of RF data processed.'.format(i))

            for f_name in baseline_files:
                read_data(f_name, data_db, metadata_db, True, 50, 20, baseline_db)
                compare_and_update_alerts(metadata_db, baseline_db, active_alerts)
            print('\nBaseline re-processed\n')

    else:  # not debug

        while True:  # ctrl+c to exit
            # Loop through aquired spectrum data
            for i in range(NUM_DATA_FILES_TO_KEEP):
                
                f_name = os.path.join(PROJ_DIRECTORY, 'live_data/spectrum_data{0:02d}.txt'.format(i))
                get_sdr_data(f_name)
                read_data(f_name, data_db, metadata_db, True, 50, 20, baseline_db)
                compare_and_update_alerts(metadata_db, baseline_db, active_alerts)
                time.sleep(0.02)

            
if __name__ == '__main__':
    main()


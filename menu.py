# SDR Menu

import copy, os, subprocess, sys
from alert import compare_and_update_alerts, generate_alerts_db
from db_funct import read_data

import time

NUM_DATA_FILES_TO_KEEP = 20
DATA_DIRECTORY = '/home/rock64/SDR/hackrf_signal_detector/data'


def modify_current_frequency():
    print('modify_current_frequency called')

def view_previous_alerts():
    print('view_previous_alerts called')

def change_scanning_parameters():
    print('change_scanning_parameters called')

def inputLoop():
    
    while True:
        print('\nCurrent Freq: {}\n'.format(None))
        print('---SDR Menu---\n')
        print('1) Modify Current Freqency')
        print('2) View Previous Alerts')
        print('3) Change Scanning Parameters')
        i = input('>>>')
    
        if i == '1':
            modify_current_frequency()
        elif i == '2':
            view_previous_alerts()
        elif i == '3':
            change_scanning_parameters()
        else:
            print('Invalid input receieved.  Please enter 1, 2, or 3.  Ctrl+C to exit.')

def get_sdr_data(file_name, data_db, metadata_db):
    sdr_cmd = 'hackrf_sweep -1 -n 32768 > {}'.format(file_name)

    print('\n\n***** now calling "{}"'.format(sdr_cmd))
    subprocess.call(sdr_command, stdout=subprocess.DEVNULL, shell=True)

    # TODO throw a clear here?

    read_data(file_name, data_db, metadata_db)

def get_dummy_baseline():
    # Using data here:  /home/rock64/SDR/hackrf_signal_detector/data/top_bench/top_bench32768_xx.txt
    # There's also data with 16384 and 65536 samples too, but 32768 seems like a good balance

    base_dir = '/home/rock64/SDR/hackrf_signal_detector/data'
    baseline_files = [os.path.join(base_dir, 'top_bench/top_bench32768_{0:02d}.txt'.format(i)) for i in range(50)]
    rf_960Mhz_0dB = [os.path.join(base_dir, 'rf_source/top_bench/960Mhz/00dB_top_bench32768_{}.txt'.format(i)) for i in range(10)]


    data_db, baseline_db = dict(), dict()


    # parse baseline
    for f_name in baseline_files:
        read_data(f_name, data_db, metadata_db, 1000, 50)  # longer deque for baseline_db





def get_spectrum_baseline():
    pass  # TODO get_sdr_data 2 min?

def start():
    subprocess.call('clear', shell=True)
    print('\n\n\n' + ' '*10 + '*'*34)
    print(' '*10 + '**  SDR Carrier Wave Dectector  **')
    print(' '*10 + '*'*34 + '\n\n\n')

    print('Press enter to begin scanning for RF Spectrum baseline.')
    return input()

def main():
    start()
    
    data_db, metadata_db, baseline_db = dict(), dict(), dict()
    
    # If script is called with DEBUG, use dummy data.  Otherwise scan
    try:
        if sys.argv[1] == 'DEBUG':
            baseline_db = get_dummy_baseline()
        else:
            print('Invalid input.  Run script with "DEBUG" param or no params at all.')
            sys.exit()
    except:
        baseline_db = get_spectrum_baseline()

    # We've now got the min, max, and average of our spectrum.  Store in baseline_db for alert comparisons.
    baseline_db = copy.deepcopy(metadata_db)

    active_alerts = generate_alerts_db(current_db)

    while True:  # ctrl+c to exit
        for i in range(NUM_DATA_FILES_TO_KEEP):
            filename = os.path.join(DATA_DIRECTORY, 'spectrum_data{0:02d}.txt'.format(i))
            get_sdr_data(filename, data_db, metadata_db)
            compare_and_update_alerts(metadata_db, baseline_db, active_alerts)

            time.sleep(2)

    


if __name__ == '__main__':
    main()



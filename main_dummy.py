# Main driver for SDR project

import datetime, time, os, subprocess, sys
from pprint import pprint as p
from db_funct import read_data, update_averages


# Using data here:  /home/rock64/SDR/hackrf_signal_detector/data/top_bench/top_bench32768_xx.txt
# There's also data with 16384 and 65536 samples too, but 32768 seems like a good balance

base_dir = '/home/rock64/SDR/hackrf_signal_detector/data'
baseline_files = [os.path.join(base_dir, 'top_bench/top_bench32768_{0:02d}.txt'.format(i)) for i in range(50)]
rf_960Mhz_0dB = [os.path.join(base_dir, 'rf_source/top_bench/960Mhz/00dB_top_bench32768_{}.txt'.format(i)) for i in range(10)]


data_db, avg_db, average = dict(), dict(), dict()


# parse baseline
for f_name in baseline_files:
        read_data(f_name, data_db)  # deque length 50 by default
        update_averages(avg_db, data_db, 20) # experiment with avg deque length

min_max_db = dict()
for freq in avg_db:
    min_max_db[freq] = ''

# closest_bin = min(avg_db.keys(), key=lambda k: abs(k-960000000))
# p(closest_bin)
# p(avg_db.get(closest_bin))

for i in [955000000, 960000000, 965000000]:
    print('{}:\n{}'.format(i, avg_db.get(i)))

#p(avg_db[960 000 000])

sys.exit()



while True: # ctrl+c to exit
    # time.sleep(1)
    
    for i in range(10):
        file_name = 'file{}.txt'.format(str(i))
        cmd = sdr_cmd + file_name
        print('\nnow calling "{}"\n'.format(cmd))
        # subprocess.call(cmd, shell=True) # Super dangerous, don't do this ;)
        subprocess.call(cmd, stdout=subprocess.DEVNULL, shell=True) # EVEN MORE DANGEROUS
        
        read_data(file_name, data_db)
        update_averages(avg_db, data_db, 10)
        print('0.95Ghz bin avg: {}'.format(average['  999500000']))
        print('1Ghz bin avg: {}'.format(average[' 1000000000']))
        #p(avg_db)
    
    # Distill the last averages into one actionable number, alert if necessary
    if average:
        # if THRESHOLD * average[freq] < sum(avg_db[freq]) / len(avg_db[freq]):
        if average[freq] + 10.0 < sum(avg_db[freq]) / len(avg_db[freq]):
            # PANIC
            # print('ALERT:  Frequency {} increased by at least {}%.'.format(freq, (THRESHOLD-1)*100))
            print('ALERT:  Frequency bin {} increased by at least 20dB!!!'.format(freq))
            sys.exit()
    
    # Update distilled average
    for freq in avg_db:
        average[freq] = sum(avg_db[freq]) / len(avg_db[freq])

    print('2.3Ghz bin avg: {}'.format(average[' 2300000000']))

    print('2.3Ghz bin avg: {}'.format(average[' 2300000000']))
    print('2.3Ghz bin avg: {}'.format(average[' 2300000000']))

# print('Data:\n')
# p(data_db)
# print('\n\n\nAvg:\n')
# p(avg_db)





# Main driver for SDR project

import datetime, time, os, subprocess, sys
from pprint import pprint as p
from db_funct import read_data, update_averages


sdr_cmd = 'hackrf_sweep -1 -f 10:6000 -n 16384 > '

data_db, avg_db, average = dict(), dict(), dict()

THRESHOLD = 2.00 # note this is linear, so 3 dB.  Might be worth changing

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





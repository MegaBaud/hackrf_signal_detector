import time, os, subprocess

SHARED_FILE = 'snapshot.txt_copy'
bin_size = 1000000.0

freq = float(input('Enter desired center frequency: '))
num = int(input('Enter how many bins to monitor: '))

freq_of_interest = [freq + (i+1)*bin_size for i in range(-1 * num//2, num//2)]

while True:  # ctrl+c to exit
    subprocess.call('clear', shell=True)
    print('\n\n Frequency    last_val   min     max  running_avg baseline_avg')
    print('--------------------------------------------------------------')

    # typical filesize is 315520, reducing for safety, but could cause problems too
    # while os.path.getsize(SHARED_FILE) < 315400:
    #     time.sleep(0.02)
    
    try:  # if the file gets overwritten, just exit out of the loop and retry
        freq_of_interest = [freq + (i+1)*bin_size for i in range(-1 * num//2, num//2)]
        with open(SHARED_FILE, 'r') as f:
            for line in f:
                x = line.split(', ')
                for i in range(len(x)):
                    x[i] = float(x[i])
                curr_freq, last_reading, minimum, maximum, average, baseline_avg = x

                if curr_freq in freq_of_interest:
                    print('{}:  {:.02f}  {:.02f}  {:.02f}   {:.02f}     {:.02f}'.format(str(curr_freq).rjust(12),
                           last_reading, minimum, maximum, average, baseline_avg) )
                    freq_of_interest.remove(curr_freq)
                if len(freq_of_interest) == 0:
                    break
        time.sleep(0.5)
    except:
        pass  # Everything is TOTALLY FINE AND THREADSAFE I SWEAR

    time.sleep(1)


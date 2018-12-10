import time, subprocess

SHARED_FILE = 'snapshot.txt'
bin_size = 1000000.0

freq = float(input('Enter desired center frequency: '))
num = int(input('Enter how many bins to monitor: '))


freq_of_interest = [freq + (i+1)*bin_size for i in range(-1 * num//2, num//2)]

while True:  # ctrl+c to exit
    subprocess.call('clear', shell=True)
    print('\n\n Frequency    last_val   min     max  running_avg')
    print('-------------------------------------------------')

    with open(SHARED_FILE, 'r') as f:
        for line in f:
            x = line.split(',')
            for i in range(len(x)):
                x[i] = float(x[i])
            curr_freq, last_reading, minimum, maximum, average = x

            if curr_freq in freq_of_interest:
                print('{}:  {:.02f}  {:.02f}  {:.02f}  {:.02f}'.format(str(curr_freq).rjust(10), last_reading,
                       minimum, maximum, average) ) 

    time.sleep(2)


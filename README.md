Using the new *hackrf_sweep* function of the HackRF One SDR (Software Defined Radio) scan from 10Mhz to 6Ghz, keeping a running track of each frequency's amplitude.  Doesn't tell you _what_ signals are there, just that there are signals.

Future work:  improve file handling technique, as that is the biggest bottleneck.  The HackRF One can scan about 30% faster without this bottleneck.

# max_primesv2
Second version of max primes without a sieve.  

## Installation
This script requires Python 3.  
You can find all of the available downloads here https://www.python.org/downloads/

## Useage
Run it on your favorite command line.  This program is OS agnostic.  It requires two command line parameters

1. The first is an integer which is to specificy the size of the set of numbers to calculate on each processor.  For instance a size of 100 will send 0 through 99 to the first process and then 100 through 199 to the next process.

2. The second command line parameter is how long the program will run for before quitting.  This will receive a floating point number.

* NOTE: By default the program records the amount of available CPU's and uses all of them for the duration of the program.
#!/usr/bin/python
import sys, math, re, time, os, copy, traceback, subprocess, signal
import multiprocessing as mp
from multiprocessing import Process, Queue

def findPrimes(startIndex, calcRange, q, runTime, numProcs, endTime):
	endIndex = startIndex + calcRange
	print ("endIndex: " + str(endIndex))

	# Keep a human meaningful of ID's of different threads.
	threadId = startIndex / calcRange

	currentNumber = startIndex
	isPrime = True
	highestPrimeChild = 0

	if currentNumber < 3:
		print ("Found a prime: 1")
		print ("Found a prime: 2")
		currentNumber = 3

	# This number is to be used as the 
	divisor = 3


	# outer while loop should start here because if it starts on an even number we do not want to calc it.
	# outer while loop will have both a timer to check the termination condition
	# and it will also check to ensure the current number is below the calcRange index.
	# Each iteration will add the calc range * 12 to the start index.

	while time.time() < endTime:

		if currentNumber % 2 == 0:
			currentNumber += 1
		
		while currentNumber <= endIndex:					# 27367 for 60
		# while currentNumber != -1:						# 4951 for 2 seconds  			#27529 for 60
			while divisor < currentNumber:
				if currentNumber / divisor > 1 and currentNumber % divisor == 0:
					isPrime = False
				divisor += 1

			if isPrime == True:
				
				highestPrimeChild = currentNumber

			currentNumber += 2
			isPrime = True
			divisor = 3

		currentNumber = endIndex + (numProcs * calcRange)
		endIndex = currentNumber + calcRange

		if time.time() < endTime:
			print ("Highest prime in thread " + str(int(threadId)) + " is " + str(highestPrimeChild))
			q.put(highestPrimeChild)

	# outer while loop will end here.  After each iteration of the calc range, 
	# a single highest prime will be placed in the queue.

def main(args):
	print ("You are in the main function.")
	# Get the run time from the command line and convert it to a floating point. 
	runTime = float(args[1])
	endTime = time.time() + runTime	

	# Initialize the 
	q = Queue()
	
	timeLeft = runTime

	numProcs = mp.cpu_count()
	
	highestPrime = []
	calcRange = int(args[2])

	# Create a background process to calculate primes until it receives a signal
	for i in range(0, numProcs):
		print (i)
		p = Process(target = findPrimes, args = (calcRange * i, calcRange, q, runTime, numProcs, endTime))
		p.start()

	while timeLeft > 0:
		print ("There are: " + str(timeLeft) + " seconds left to find a higher prime.")
		time.sleep(1)
		timeLeft -= 1

	while not q.empty():
		highestPrime.append(q.get())

	print 
	print ("Time is up!")
	print

	print
	print (highestPrime[len(highestPrime) - 1])
	print

	print (highestPrime)	

	for i in range(0, numProcs):
		p.join()

	q.close()
	# After sending the signal this is to ensure the process is joined.
	# Very likely uncessary.
	

if __name__ == '__main__':
	main(sys.argv)
#!/usr/bin/python
import sys, math, time, os
import multiprocessing as mp
from multiprocessing import Process, Queue

def findPrimes(startIndex, calcRange, q, numProcs, endTime):
	endIndex = startIndex + calcRange

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
				# if one wants to see every prime found a print statement can be added here.
				if time.time() < endTime:
					print ("Highest prime in thread so far " + str(int(threadId)) \
						+ " is " + str(highestPrimeChild))
			currentNumber += 2
			isPrime = True
			divisor = 3
			# Due the the threads ending at different times I had to mute some of the progress of the primes to 
			# not have the threads leak after the timer is done.
			# Another theory on how to address this would be to terminate the process and only keep primes up 
			# to this point with the timer.
			# This will be attempted in version three after the submission.
			#if time.time() < endTime:	# This could be replaced by a Do While loop to save one of these checks.
				#print ("Highest prime in thread " + str(int(threadId)) + " is " + str(highestPrimeChild))

		currentNumber = endIndex + (numProcs * calcRange)
		endIndex = currentNumber + calcRange
		if time.time() < endTime:	# This could be replaced by a Do While loop to save one of these checks.
			print ("Highest prime in thread so far " + str(int(threadId)) \
				+ " is " + str(highestPrimeChild))
			q.put(highestPrimeChild)


	# outer while loop will end here.  After each iteration of the calc range, 
	# a single highest prime will be placed in the queue.

def main(args):
	# Get the run time from the command line and convert it to a floating point. 
	runTime = float(args[2])
	endTime = time.time() + runTime	

	# Initialize queue and other variables
	q = Queue()
	timeLeft = runTime
	numProcs = mp.cpu_count()
	highestPrimeList = []		#List of higher primes to hold as they are taken from the queue.
	calcRange = int(args[1])	#This adjusts the range of numbers to be computed for each thread.

	primesCalculated = 0
	whileCounter = 0		
	highestPrime = 0

	# Create a background process to calculate primes until it receives a signal
	for i in range(0, numProcs):
		print (i)
		p = Process(target = findPrimes, args = (calcRange * i, calcRange, q, numProcs, endTime))
		p.start()

	while timeLeft > 0:
		print
		print ("There are: " + str(timeLeft) + " seconds left to find a higher prime.")
		print
		time.sleep(1)
		timeLeft -= 1

	while not q.empty():
		highestPrimeList.append(q.get())

	primesCalculated = len(highestPrimeList)

	# Count back the number of different processes used to ensure the highest prime from
	# any one of the processes is the highest overall prime number.
	while numProcs > whileCounter:
		if highestPrimeList[primesCalculated - whileCounter - 1] > highestPrime:
			highestPrime = highestPrimeList[primesCalculated - whileCounter - 1]
		whileCounter += 1

	print ()
	print ("Time is up!")
	print ()
	print ("The Highest prime found in the given time was: " + str(highestPrime))
	print ()

	# Clean up all of my child processes.
	for i in range(0, numProcs):
		p.join()

	q.close()
	# After sending the signal this is to ensure the process is joined.
	# Very likely uncessary.
	

if __name__ == '__main__':
	main(sys.argv)
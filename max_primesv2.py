#!/usr/bin/python
import sys, math, re, time, os, copy, traceback, subprocess, signal
import multiprocessing as mp
from multiprocessing import Process, Queue
import queue



def findPrimes(startIndex, calcRange, q, runTime):
	print ("The find primes function is running.")
	print ("StartIndex in my thread is: " + str(startIndex))

	endTime = time.time() + runTime	#Change this to command line args

	currentNumber = startIndex
	isPrime = True
	highestPrime = 0

	if currentNumber < 3:
		print ("Found a prime: 1")
		print ("Found a prime: 2")
		currentNumber = 3

	# This number is to be used as the 
	divisor = 3

	if currentNumber % 2 == 0:
		currentNumber += 1


	while time.time() < endTime:		#27367 for 60
	# while currentNumber != -1:						# 4951 for 2 seconds  			#27529 for 60
		while divisor < currentNumber:
			if currentNumber / divisor > 1 and currentNumber % divisor == 0:
				isPrime = False
			divisor += 1

		if isPrime == True:
			print (str(currentNumber) + " is a prime!")
			highestPrime = currentNumber


		currentNumber += 2
		isPrime = True
		divisor = 3

	q.put(highestPrime)


def main(args):
	print ("You are in the main function.")

	# Initialize the 
	startIndex = 0
	q = Queue()
	runTime = int(args[1])

	numProcs = mp.cpu_count()
	
	highestPrime = []
	calcRange = 1000

	# Create a background process to calculate primes until it receives a signal
	for i in range(0, numProcs):
		p = Process(target = findPrimes, args = (startIndex * i, calcRange, q, runTime))
		p.start()

	for i in range(0, numProcs):
		highestPrime.append(q.get())

	for i in range(0, numProcs):
		p.join()

	print (highestPrime)
	

	# After sending the signal this is to ensure the process is joined.
	# Very likely uncessary.
	

if __name__ == '__main__':
	main(sys.argv)
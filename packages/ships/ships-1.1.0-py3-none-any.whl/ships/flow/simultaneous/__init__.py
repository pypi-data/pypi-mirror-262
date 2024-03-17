

'''
	def move (item):
		print (f"Processing item: {item}")
		time.sleep (item)

	simultaneously (
		items = [1, 1, 1, 1, 1, 1, 1, 1],
		capacity = 4,
		move = move
	)
'''


import threading
import time

def simultaneously (
	items = [],
	capacity = 2,
	move = lambda : None
):
	#
	#	capacity = 2
	#
	semaphore = threading.Semaphore (capacity)

	#
	#	A process with a semaphore limit
	#
	def process_with_semaphore (item):
		with semaphore:
			move (item)

	#
	#	threads for processing
	#
	threads = []
	for item in items:
		thread = threading.Thread (
			target = process_with_semaphore, 
			args = (item,)
		)
		
		thread.start ()
		threads.append (thread)
	
	#
	#	Wait for all threads to complete
	#
	for thread in threads:
		thread.join ()
		


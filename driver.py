# File name:      driver.py
# Author:         Dalton Cole

from helper_functions import *

def main():
	if len(sys.argv) != 3:
		print('Usage: python3 driver.py <config file> <problem>')
		quit()

	# {'input_file': '', 'runs': 1, 'random_seed': 1, 'search_algorithm': '', 
	#  'fitness_evaluations': 1, 'log_file_path': './', 
	#  'solution_file_path': './', 'algorithm_solution_file_path': './'}
	config_dict = config_parser(sys.argv[1])

	# Set problem file
	config_dict['input_file'] = sys.argv[2]

	#random.seed(config_dict['random_seed'])

	# Create log file
	create_log_file(config_dict)

	### Constants ###
	population_size = 100
	#################

	# Multiprocess
	manager = multiprocessing.Manager()
	return_dict = manager.dict()
	jobs = []

	# ctrl-c handler
	signal.signal(signal.SIGINT, signal_handler)
	# signal.signal(signal.SIGINT, partial(signal_handler, return_dict, config_dict)) # With partial

	max_height = 0
	shapes = []
	with open(config_dict['input_file'], 'r') as f:
		max_height, _ = f.readline().split()
		max_height = int(max_height)
		for line in f:
			shapes.append(line)

	
	# Start run
	for run in range(config_dict['runs']):
		p = multiprocessing.Process(target=run_algorithm, args=(config_dict, max_height, shapes, population_size, run, return_dict))
		jobs.append(p)
		p.start()

	for proc in jobs:
		proc.join()

	# Write to algorithm log file
	write_algorithm_log(config_dict['algorithm_solution_file_path'], config_dict['runs'], return_dict)


if __name__ == '__main__':
	main()


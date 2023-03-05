#The output is sorted which might be useful for our case since we need to timing analysis, but it defeats the purpose of the algorithm since it 
#supposed to output m randomly chosen packets if n=m+f

import socket
import struct
import random
from datetime import datetime, timedelta
import GenerateMessages


def threshold_pool(n: int, m: int, f: int):
    """
    Function to read messages from input file and output messages within a threshold of m
    """
    with open('input.txt', 'r') as input_file, open('output.txt', 'w+') as output_file:
        max_time = datetime.min  # initialize with minimum datetime value
        count = 0  # initialize counter
        batch = 0  # initialize batch number
        msgs = []  # initialize message buffer
        pool = []  # initialize pool buffer
        lines = (line.strip().split('\t') for line in input_file)
        lines = sorted(lines, key=lambda x: datetime.strptime(x[2], '%Y-%m-%d %H:%M:%S'))

        for i, (src, dest, time_str, msg) in enumerate(lines):
            # split line into fields and convert time to datetime object
            time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

            # update max_time regardless of whether time is within threshold m
            max_time = max(max_time, time)

            # check if time is within threshold m and count is less than n
            if (time - max_time).total_seconds() <= m and count < n:
                count += 1

                # add the message to the pool
                pool.append((src, dest, time_str, msg))

                # check if the pool is full and print the messages
                if len(pool) == m + f:
                    batch += 1
                    # write the messages along with the ending time
                    output_file.write(f'BATCH {batch} - ThresholdPool\n')
                    for src, dest, time_str, msg in pool:
                        output_file.write(f'{src}\t{dest}\t{time_str}\t{msg}\t{time_str}\tthreshold_pool\n')
                    # clear the pool and reset the count and max_time
                    pool.clear()
                    count = 0
                    max_time = datetime.min

        # check if there are any messages remaining in the pool and print them
        if pool:
            batch += 1
            # write the messages along with the ending time
            output_file.write(f'BATCH {batch} - ThresholdPool\n')
            for src, dest, time_str, msg in pool:
                output_file.write(f'{src}\t{dest}\t{time_str}\t{msg}\t{time_str}\tthreshold_pool\n')


def mix(n_messages, n_nodes, random_time, thres, f):
    """
    Function to generate input messages and call the timed function with various time thresholds
    """
    config = GenerateMessages.setup(n_nodes)
    GenerateMessages.generate_input(n_messages, n_nodes, config, random_time, fixed_prob)

    threshold_pool(n_messages, thres, f)


n_nodes = 20
n_messages = 10000
thres = 10
f = 2
random_time = 10000
fixed_prob = 0.15

mix(n_messages, n_nodes, random_time, thres, f)

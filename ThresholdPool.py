import random
from typing import List
from datetime import datetime

import GenerateMessages


def thresholdpool(n: int, m: int, f: int) -> None:
    """
    Function to read messages from input file and output messages according to Threshold Pool Mix algorithm
    if n = m + f, then send m randomly chosen packets from the pool
    """
    # Initialize pool with m packets
    pool: List[str] = []
    with open('input.txt', 'r') as input_file, open('output.txt', 'w+') as output_file:
        count = 0  # initialize counter
        lines = (line.strip().split('\t') for line in input_file)
        lines = sorted(lines, key=lambda x: datetime.strptime(x[2], '%Y-%m-%d %H:%M:%S'))
        msgs = []  # initialize message buffer
        for i, (src, dest, time_str, msg) in enumerate(lines):
            # split line into fields and convert time to datetime object
            time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            # check if number of packets received is equal to m + f
            if len(pool) == m + f:
                # send m random packets from pool
                random.shuffle(pool)
                msgs = pool[:m]
                pool = pool[m:]
                # write batch separator and messages
                end_time = time
                output_file.write(f'\nBATCH {i // m} - Threshold Pool Mix\n')
                for msg in msgs:
                    output_file.write(msg + str(end_time) + '\tthresholdpool\n')
                msgs = []
                count -= m
            # add message to pool if count is less than n
            if count < n:
                count += 1
                # add message to pool
                pool.append(f'{src}\t{dest}\t{time_str}\t{msg}\t')
                # check if pool is full
                if len(pool) == m + f:
                    # send m random packets from pool
                    random.shuffle(pool)
                    msgs = pool[:m]
                    pool = pool[m:]
                    # write batch separator and messages
                    end_time = time
                    output_file.write(f'\nBATCH {i // m} - Threshold Pool Mix\n')
                    for msg in msgs:
                        output_file.write(msg + str(end_time) + '\tthresholdpool\n')
                    msgs = []
                    count -= m


def mix(n_messages, n_nodes, random_time, thres, f):
    """
    Function to generate input messages and call the thresholdpool function with various parameters
    """
    config = GenerateMessages.setup(n_nodes)
    GenerateMessages.generate_input(n_messages, n_nodes, config, random_time, fixed_prob)

    thresholdpool(n_messages, thres, f)


n_nodes = 20
n_messages = 10000
thres = 10
f = 5
random_time = 10000
fixed_prob = 0.15

mix(n_messages, n_nodes, random_time, thres, f)


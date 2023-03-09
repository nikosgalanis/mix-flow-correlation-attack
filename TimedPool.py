import random
from datetime import datetime, timedelta
from typing import List
import GenerateMessages


def timedpool(n: int, m: int, f: int, t: int) -> None:
    """
    Function to read messages from input file and output messages according to Timed Pool Mix algorithm
    if timer runs out (t), and n > f, then send (n - f) randomly chosen packets.
    """
    # Initialize pool with m packets
    pool: List[str] = []
    with open('input.txt', 'r') as input_file, open('output.txt', 'w+') as output_file:
        max_time = datetime.min  # initialize with minimum datetime value
        count = 0  # initialize counter
        lines = (line.strip().split('\t') for line in input_file)
        lines = sorted(lines, key=lambda x: datetime.strptime(x[2], '%Y-%m-%d %H:%M:%S'))
        msgs = []  # initialize message buffer
        for i, (src, dest, time_str, msg) in enumerate(lines):
            # split line into fields and convert time to datetime object
            time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            # update max_time regardless of whether time is within threshold m
            max_time = max(max_time, time)
            # check if time is within threshold m and count is less than n
            if (time - max_time).total_seconds() <= m and count < n:
                count += 1
                # add message to pool
                pool.append(f'{src}\t{dest}\t{time_str}\t{msg}\t')
                # update the end time in every message, so eventually it is the input time of the last message
                end_time = time
                # check if pool is full
                if len(pool) == m:
                    # start timer
                    timer = datetime.now() + timedelta(seconds=t)
                    while True:
                        # check if timer has timed out
                        if time >= timer:
                            # send packets only if pool has more than f packets
                            if len(pool) > f:
                                # send n-f random packets from pool
                                random.shuffle(pool)
                                msgs = pool[:n - f]
                                pool = pool[n - f:]
                                break
                            else:
                                # reset timer and wait for more packets to arrive in pool
                                timer = datetime.now() + timedelta(seconds=t)
                                continue
                        else:
                            # wait for timer to time out
                            continue
                    # shuffle the output order
                    random.shuffle(msgs)
                    output_file.write(f'\n')
                    # write batch separator and messages
                    for msg in msgs:
                        output_file.write(msg + str(end_time) + '\ttimedpool\n')
                    msgs = []
                    count -= n - f


def mix(n_messages, n_nodes, random_time, thres, fixed_prob, f, t):
    """
    Function to generate input messages and call the timedpool function with various parameters
    """
    config = GenerateMessages.setup(n_nodes)
    GenerateMessages.generate_input(n_messages, n_nodes, config, random_time, fixed_prob)

    timedpool(n_messages, thres, f, t)


# n_nodes = 20
# n_messages = 100
# thres = 10
# f = 5
# t = 5
# random_time = 10000
# fixed_prob = 0.15

# mix(n_messages, n_nodes, random_time, thres,fixed_prob,  f, t)

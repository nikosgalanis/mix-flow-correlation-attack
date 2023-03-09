import random
from datetime import datetime, timedelta

import GenerateMessages


def timedDynamicPool(n: int, m: int, f: int, p: float, t: int) -> None:
    """
    Function to read messages from input file and output messages according to Timed Dynamic-Pool Mix algorithm
    if timer (t) runs out, AND n>=m+f, then send max(1, (p[n-f]))
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
                                # calculate number of packets to send
                                packets_to_send = max(1, int(p * (n - f)))
                                # send packets randomly chosen from pool
                                random.shuffle(pool)
                                msgs = pool[:packets_to_send]
                                pool = pool[packets_to_send:]
                                break
                            else:
                                # reset timer and wait for more packets to arrive in pool
                                timer = datetime.now() + timedelta(seconds=t)
                                continue
                        else:
                            # wait for timer to time out
                            continue
                    # shuffle the osutput order
                    random.shuffle(msgs)
                    # write batch separator and messages
                    output_file.write(f'\n')
                    for msg in msgs:
                        output_file.write(msg + str(end_time) + '\ttimedDynamicPool\n')
                    msgs = []
                    count -= packets_to_send


def mix(n_messages, n_nodes, random_time, thres, fixed_prob, f, t, p):
    """
    Function to generate input messages and call the timedDynamicPool function with various parameters
    """
    config = GenerateMessages.setup(n_nodes)
    GenerateMessages.generate_input(n_messages, n_nodes, config, random_time, fixed_prob)

    timedDynamicPool(n_messages, thres, f, t, p)

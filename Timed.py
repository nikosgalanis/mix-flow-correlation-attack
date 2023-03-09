from datetime import datetime, timedelta
import random
import GenerateMessages


def timed(n, t):
    """
    Function to read messages from input file and output messages within a time threshold of t
    """
    with open('input.txt', 'r') as input_file, open('output.txt', 'w+') as output_file:
        batch = 1  # initialize batch number
        lines = (line.strip().split('\t') for line in input_file)
        lines = sorted(lines, key=lambda x: datetime.strptime(x[2], '%Y-%m-%d %H:%M:%S'))
        msgs = []  # initialize message buffer
        for i, (src, dest, time_str, msg) in enumerate(lines):
            # convert time to datetime object
            time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            # 1st message defines the time for the 1st batch
            if i == 0:
                end_time = time + timedelta(seconds=t)
            # check if time is within the specified time threshold
            if time <= end_time:
                # add message to buffer
                msgs.append((src, dest, time.strftime('%Y-%m-%d %H:%M:%S'), msg))
            else:
                # if the message falls outside the current 10-second window,
                # write all messages in the buffer to the output file
                if msgs:
                    # shuffle the output order
                    random.shuffle(msgs)
                    output_file.write(f'\n')
                    for m in msgs:
                        output_file.write(f'{m[0]}\t{m[1]}\t{m[2]}\t{m[3]}\t{end_time}\t{"timed"}\n')
                    batch += 1
                    msgs = []
                # update the end time to the next 10-second window
                end_time = time + timedelta(seconds=t)
                # add the current message to the buffer
                msgs.append((src, dest, time.strftime('%Y-%m-%d %H:%M:%S'), msg))
        # write remaining messages as last batch if not empty
        if msgs:
            # output_file.write(f'\nBATCH {batch} - Timed\n')
            for m in msgs:
                output_file.write(f'{m[0]}\t{m[1]}\t{m[2]}\t{m[3]}\t{end_time}\n')


def mix(n_messages, n_nodes, random_time, time_window, fixed_prob):
    """
    Function to generate input messages and call the timed function with various time thresholds
    """
    config = GenerateMessages.setup(n_nodes)
    GenerateMessages.generate_input(n_messages, n_nodes, config, random_time, fixed_prob)

    timed(n_messages, time_window)

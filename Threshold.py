from datetime import datetime, timedelta
import GenerateMessages


def threshold(n, m):
    """
    Function to read messages from input file and output messages within a threshold of m
    """
    with open('input.txt', 'r') as input_file, open('output.txt', 'w+') as output_file:
        max_time = datetime.min  # initialize with minimum datetime value
        count = 0  # initialize counter
        batch = 0  # initialize batch number
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
                # output the message with maximum time
                msgs.append(f'{src}\t{dest}\t{max_time.strftime("%Y-%m-%d %H:%M:%S")}\t{msg}\t')
                # update the end time in every message, so eventually it is the input time of the last message
                end_time = time
                # write batch separator and messages when count is a multiple of m (Change Values)
                if count % m == 0:
                    # compute the output time, i.e the input time of the last message
                    # output_file.write(f'\nBATCH {batch} - Threshold\n')
                    output_file.write(f'\n')
                    # write the messages along with the ending time
                    for msg in msgs:
                        output_file.write(msg + str(end_time) + '\tthreshold\n')
                    msgs = []
                    batch += 1


def mix(n_messages, n_nodes, random_time, thres):
    """
    Function to generate input messages and call the timed function with various time thresholds
    """
    config = GenerateMessages.setup(n_nodes)
    GenerateMessages.generate_input(n_messages, n_nodes, config, random_time, fixed_prob)

    threshold(n_messages, thres)


n_nodes = 20
n_messages = 10000
thres = 10
random_time = 10000
fixed_prob = 0.15

mix(n_messages, n_nodes, random_time, thres)

from datetime import datetime, timedelta

import GenerateMessages


def ThresholdOrTimed(threshold, time_window):
    """
    Function to generate input messages and output messages within a time threshold of t or n >= m packets threshold
    """

    # Initialize variables
    batch_num = 1
    msgs = []
    end_time = None
    threshold_count = 0

    with open('input.txt', 'r') as input_file, open('output.txt', 'w+') as output_file:
        lines = (line.strip().split('\t') for line in input_file)
        lines = sorted(lines, key=lambda x: datetime.strptime(x[2], '%Y-%m-%d %H:%M:%S'))

        for i, (src, dest, time_str, msg) in enumerate(lines):
            # Convert time to datetime object
            time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

            # First message defines the time for the first batch
            if i == 0:
                end_time = time + timedelta(seconds=time_window)

            # Check if time is within the specified time threshold
            if time <= end_time:
                # Add message to buffer
                msgs.append((src, dest, time.strftime('%Y-%m-%d %H:%M:%S'), msg))
                threshold_count += 1
                # Check if threshold is met or time window has elapsed
                if threshold_count == threshold or time >= end_time:
                    # Write all messages in the buffer to the output file
                    if msgs:
                        output_file.write(f'\nBATCH {batch_num} - Threshold or Timed Mix\n')
                        for m in msgs:
                            output_file.write(
                                f'{m[0]}\t{m[1]}\t{m[2]}\t{m[3]}\t{end_time}\t{"threshold" if threshold_count == threshold else "timed"}\n')
                        batch_num += 1
                        msgs = []
                        threshold_count = 0
                        end_time = time + timedelta(seconds=time_window)
            else:
                # If the message falls outside the current time window,
                # write all messages in the buffer to the output file
                if msgs:
                    output_file.write(f'\nBATCH {batch_num} - Threshold or Timed Mix\n')
                    for m in msgs:
                        output_file.write(f'{m[0]}\t{m[1]}\t{m[2]}\t{m[3]}\t{end_time}\t{"timed"}\n')
                    batch_num += 1
                    msgs = []
                    threshold_count = 0
                # Update the end time to the next time window
                end_time = time + timedelta(seconds=time_window)

        # Write remaining messages as last batch if not empty
        if msgs:
            output_file.write(f'\nBATCH {batch_num} - Threshold or Timed Mix\n')
            for m in msgs:
                output_file.write(f'{m[0]}\t{m[1]}\t{m[2]}\t{m[3]}\t{end_time}\t{"timed"}\n')


def mix(n_messages, n_nodes, random_time, time_window):
    """
    Function to generate input messages and call the timed function with various time thresholds
    """
    config = GenerateMessages.setup(n_nodes)
    GenerateMessages.generate_input(n_messages, n_nodes, config, random_time, fixed_prob)

    ThresholdOrTimed(threshold, time_window)


n_nodes = 20
n_messages = 10000
time_window = 10
random_time = 10000
fixed_prob = 0.15
threshold = 10

mix(n_messages, n_nodes, random_time, time_window)

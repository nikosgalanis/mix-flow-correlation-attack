import socket
import struct
import random
from datetime import datetime, timedelta

# define the characters that can be used in the message content
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

n_nodes = 20

in_nodes_ip = []
out_nodes_ip = []

for i in range(20):
    in_nodes_ip.append(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))

for i in range(20):
    out_nodes_ip.append(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))


def message_maker():
    """
    Function used to generate a random packet with the following fields:
    - source IP
    - destination IP
    - message content
    - exact time the message was sent
    """
    # randomize the scr and destination IP
    src = in_nodes_ip[random.randint(0, 19)]
    dest = out_nodes_ip[random.randint(0, 19)]
    # randomize the message
    msg = ''.join(random.choice(letters) for i in range(10))
    # randomize the time that the message was sent
    now = datetime.now() + timedelta(seconds=random.randint(1, 100))
    msg_time = now.strftime('%Y-%m-%d %H:%M:%S')
    # create the packet as a tuple of the above info and return it
    packet = (src, dest, msg_time, msg)
    return packet


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
                    # output_file.write(f'\nBATCH {batch} - Timed\n')
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
            #output_file.write(f'\nBATCH {batch} - Timed\n')
            for m in msgs:
                output_file.write(f'{m[0]}\t{m[1]}\t{m[2]}\t{m[3]}\t{end_time}\n')


def generate_input(n):
    """
    Function to generate n random messages, sort them by time and write them to input file
    """
    packets = []
    for i in range(n):
        packet = message_maker()
        packets.append(packet)

    # sort packets by time
    packets = sorted(packets, key=lambda packet: packet[2])

    # write sorted packets to input file
    with open('input.txt', 'w') as input_file:
        for packet in packets:
            input_file.write(f'{packet[0]}\t{packet[1]}\t{packet[2]}\t{packet[3]}\n')


def mix(n, t_values):
    """
    Function to generate input messages and call the timed function with various time thresholds
    """
    generate_input(n)
    for t in t_values:
        timed(n, t)


if __name__ == '__main__':
    n = 300
    t_values = [5]
    mix(n, t_values)

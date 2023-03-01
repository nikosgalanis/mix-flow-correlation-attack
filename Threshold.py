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


def mix(n, m_values):
    """
    Function to generate input messages and call the threshold function with various threshold values
    """
    generate_input(n)
    for m in m_values:
        threshold(n, m)


if __name__ == '__main__':
    n = 100
    m_values = [10]  # Change value on line 51
    mix(n, m_values)

import socket
import struct
import random
from datetime import datetime, timedelta


def setup(n_nodes):    
    # initialize lists for fixed (but random) src and dest IPs
    in_nodes_ip = []
    out_nodes_ip = []

    # generate them at random
    for i in range(n_nodes):
        in_nodes_ip.append(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))

    for i in range(n_nodes):
        out_nodes_ip.append(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))

    # we want each source to have a "favorite" destination
    dests = {}

    # delect the favorite dest at random from the available dest IPs
    for i in in_nodes_ip:
        dests[i] = out_nodes_ip[random.randint(0, n_nodes - 1)]

    # return the info we created
    return (in_nodes_ip, out_nodes_ip, dests)

def message_maker(n_nodes, config, random_time, fixed_prob):
    """
    Function used to generate a random packet with the following fields:
    - source IP
    - destination IP
    - message content
    - exact time the message was sent
    """
    # unpack the config of the src and dest nodes
    (in_nodes_ip, out_nodes_ip, dests) = config
    # define the characters that can be used in the message content
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    # randomize the scr IP
    src = in_nodes_ip[random.randint(0, n_nodes - 1)]
    # choise a (0,1) value, in order to decide if the node will comunicate with their favorite dest, or with a random one
    prob = random.random()
    # communicating with favorite
    if prob < fixed_prob:
        dest = dests[src]
    # communicating with any other
    else:
        dest = out_nodes_ip[random.randint(0, n_nodes - 1)]

    # randomize the message
    msg = ''.join(random.choice(letters) for i in range(10))
    # randomize the time that the message was sent
    now = datetime.now() + timedelta(seconds=random.randint(1, random_time))
    msg_time = now.strftime('%Y-%m-%d %H:%M:%S')
    # create the packet as a tuple of the above info and return it
    packet = (src, dest, msg_time, msg)
    return packet


def generate_input(n_messages, n_nodes, config, random_time, fixed_prob):
    """
    Function to generate n random messages, sort them by time and write them to input file
    """
    # unpack the configuration
    (in_nodes_ip, out_nodes_ip, dests) = config
    # initialize list of packets
    packets = []
    # create the appropriate number of packets
    for i in range(n_messages):
        packet = message_maker(n_nodes, config, random_time, fixed_prob)
        packets.append(packet)

    # sort packets by time
    packets = sorted(packets, key=lambda packet: packet[2])

    # write sorted packets to input file
    with open('input.txt', 'w') as input_file:
        for packet in packets:
            input_file.write(f'{packet[0]}\t{packet[1]}\t{packet[2]}\t{packet[3]}\n')

"""
Step 1: Data Collection
-Get input packets time of entering mix network
-Get output packets time of arriving at node

Step 2: Flow Pattern Extraction
-Transform list of input packets and output packets into pattern vectors

Step 3: Distance Function Selection
-Determine the distance between the pattern vectors
-Distance Function 1: Mutual Information
-Distance Function 2: Frequency-spectrum-based matched filter

Step 4: Flow Correlation
-Selecting the OUTPUT link whose traffic has the minimum distance to INPUT flow pattern vector
"""
import math
import struct
import random
from datetime import datetime, timedelta
import numpy as np
from sklearn import metrics
import pywt
from scipy import signal, fftpack
from collections import defaultdict

with open("output.txt", 'r') as f:
    lines = list(map(lambda x: x.split('\t'), f.readlines()))

# TODO: change when we connect all the files, to datetime.now()
first_src_time = datetime.strptime(lines[1][2], '%Y-%m-%d %H:%M:%S') - timedelta(seconds=1)
first_dest_time = datetime.strptime(lines[1][4], '%Y-%m-%d %H:%M:%S') - timedelta(seconds=1)

timed_window = 5


def dataCollection():
    # Read lines 
    with open("output.txt", 'r') as f:
        lines = list(map(lambda x: x.split('\t'), f.readlines()))

    first_src_time = datetime.strptime(lines[1][2], '%Y-%m-%d %H:%M:%S')
    first_dest_time = datetime.strptime(lines[1][4], '%Y-%m-%d %H:%M:%S')
    # Get batches
    batches = []
    start_idx = 1
    for i, line in enumerate(lines[1:]):
        if line == ['\n']:
            batches.append(lines[start_idx: i + 1])
            start_idx = i + 2
    batches.append(lines[start_idx:])

    """
    Create A (src dict)

    in_ips: {src_ip: [batch_0, batch_1,..., batch_n]}
    batch_n = [in_time0, in_time1,...,in_time_n]
    """
    # Get unique source ips 
    unique_src_ips = set()
    for batch in batches:
        for entry in batch:
            unique_src_ips.add(entry[0])

    # Create dictionary
    A_mapping = dict.fromkeys(unique_src_ips, None)

    for unique_src_ip in unique_src_ips:
        A_mapping[unique_src_ip] = []
        for batch in batches:
            batch_msgs = []
            for entry in batch:
                if entry[0] == unique_src_ip:
                    batch_msgs.append(entry[2])
            A_mapping[unique_src_ip].append(batch_msgs)

    """
    Create B (dest dict)

    out_ips: {dest_ip: [batch_0, batch_1,..., batch_n]}
    batch_n = [out_time0, out_time1,...,out_time_n]
    """

    # Get unique source ips 
    unique_dest_ips = set()
    for batch in batches:
        for entry in batch:
            unique_dest_ips.add(entry[1])

    # Create dictionary
    B_mapping = dict.fromkeys(unique_dest_ips, None)

    for unique_dest_ip in unique_dest_ips:
        B_mapping[unique_dest_ip] = []
        for batch in batches:
            batch_msgs = []
            for entry in batch:
                if entry[1] == unique_dest_ip:
                    batch_msgs.append(entry[4])
            B_mapping[unique_dest_ip].append(batch_msgs)

    return A_mapping, B_mapping


in_batch, out_batch = dataCollection()

"""
    in_ips: {src_ip: [batch_0, batch_1,..., batch_n]}
    batch_n = [in_time0, in_time1,...,in_time_n]

    j = ip
    k = batch_no
    X: [X0,1, X0,2 ... ] [X1,1 ... ] []
"""


def flowPatternExtraction(in_batch, out_batch):
    in_j = in_batch.keys()
    out_j = out_batch.keys()

    mix_type = "timed"

    X = []
    Y = []
    in_ips = []
    out_ips = []

    if mix_type == "threshold":

        for in_key in in_j:
            in_ips.append(in_key)
            batches = in_batch[in_key]
            end_time_prev = first_src_time
            x_j = []
            for batch in batches:
                n_packs = len(batch)
                if n_packs == 0:
                    x_j_k = 0
                else:
                    # we want the in time of the last msg
                    end_time_str = batch[-1]
                    end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

                    delta_time = (end_time - end_time_prev).total_seconds()

                    x_j_k = n_packs / delta_time

                    end_time_prev = end_time

                x_j.append(x_j_k)

            X.append(x_j)

        for out_key in out_j:
            out_ips.append(out_key)
            batches = out_batch[out_key]
            end_time_prev = first_dest_time
            y_j = []
            for batch in batches:
                n_packs = len(batch)
                if n_packs == 0:
                    y_j_k = 0
                else:
                    # it doesnt matter, all of them have same out time
                    end_time_str = batch[0]
                    end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

                    delta_time = (end_time - end_time_prev).total_seconds()
                    y_j_k = n_packs / delta_time

                    end_time_prev = end_time

                y_j.append(y_j_k)

            Y.append(y_j)

    if mix_type == "timed":

        for in_key in in_j:
            in_ips.append(in_key)
            batches = in_batch[in_key]
            x_j = []
            for batch in batches:
                n_packs = len(batch)
                if n_packs == 0:
                    x_j_k = 0
                else:
                    delta_time = timed_window
                    x_j_k = n_packs / delta_time

                x_j.append(x_j_k)

            X.append(x_j)

        for out_key in out_j:
            out_ips.append(out_key)
            batches = out_batch[out_key]
            y_j = []
            for batch in batches:
                n_packs = len(batch)
                if n_packs == 0:
                    y_j_k = 0
                else:
                    delta_time = timed_window
                    y_j_k = n_packs / delta_time

                y_j.append(y_j_k)

            Y.append(y_j)

    X_array = np.asarray(X)
    Y_array = np.asarray(Y)

    return X_array, Y_array, in_ips, out_ips


X, Y, in_ips, out_ips = flowPatternExtraction(in_batch, out_batch)

"""
X: alice, bob, charlie

Y: diana, elen, frank, g, i, k, l , m, n

for every i:
    find the j that they are communicating

"""


def dist_mutual_info(X, Y, in_ips, out_ips):
    similar_nodes = {}
    for i, in_ip in enumerate(in_ips):
        j, _ = min(enumerate(Y), key=lambda jy: 1 / metrics.mutual_info_score(X[i], jy[1]))
        similar_nodes[in_ip] = out_ips[j]

    return similar_nodes


def dist_fsb_matched_filter(X, Y, in_ips, out_ips):
    # TODO: Problem -> Does not calculate distance correctly (pred/true flow extraction changes each run)
    similar_nodes = {}
    n_nodes = X.shape[0]
    for i in range(n_nodes):
        min_value = 10
        x_freq = np.fft.fft(X[i])
        for j in range(n_nodes):
            y_freq = np.fft.fft(Y[j])

            inner_x_y = np.inner(x_freq, y_freq)

            inner_y_y = np.inner(y_freq, y_freq).real
            sqr_inner_y_y = math.sqrt(inner_y_y).real

            if inner_x_y == 0:
                continue

            corr = sqr_inner_y_y / inner_x_y
            if corr.real < min_value:
                min_value = corr.real
                similar_nodes[in_ips[i]] = out_ips[j]

    return similar_nodes


def extract_true_flow_correlation():
    most_frequent_dest = defaultdict(lambda: defaultdict(int))

    with open("output.txt", "r") as f:
        for line in f:
            line = line.split('\t')
            if (line != ['\n']):
                src_ip, dest_ip = line[0], line[1]
                most_frequent_dest[src_ip][dest_ip] += 1

    # Create a dictionary that maps each source IP to the most frequent destination IP it communicates with
    result = {}
    for src_ip, dest_ips in most_frequent_dest.items():
        most_frequent_dest_ip = max(dest_ips, key=dest_ips.get)
        result[src_ip] = most_frequent_dest_ip

    # Print the result
    return result


def flowCorrelationAttack(pred_res, true_res):
    correct = 0
    for i in pred_res.keys():
        if pred_res[i] == true_res[i]:
            correct += 1
    print(correct / len(pred_res.keys()))

    return correct / len(pred_res.keys())


def attack(distance_func):
    # 1st step: collect the data from the mix traffic
    in_batch, out_batch = dataCollection()
    # 2nd step: create the flow pattern vectors
    X, Y, in_ips, out_ips = flowPatternExtraction(in_batch, out_batch)
    # 3rd step: calculate the distance between the X and Y vectors
    if distance_func == 'mutual_info':
        pred_res = dist_mutual_info(X, Y, in_ips, out_ips)
    else:
        pred_res = dist_fsb_matched_filter(X, Y, in_ips, out_ips)
    print(pred_res)
    print("\n")
    # compute the true values by directly looking at the information flow, to extract metrics
    true_res = extract_true_flow_correlation()
    print(true_res)
    # operate the attack and extract the detection rate metric
    det_rate = flowCorrelationAttack(pred_res, true_res)
    # return the attack success
    return det_rate


print(attack("oop"))

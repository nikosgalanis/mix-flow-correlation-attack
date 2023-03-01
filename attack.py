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
import struct
import random
from datetime import datetime, timedelta


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


# print(out_batch)



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

    if mix_type == "threshold":
        
        for in_key in in_j:
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
                    print(end_time)
                    print(end_time_prev)
                    print (delta_time)
                    print("\n\n")
                    x_j_k = n_packs / delta_time

                    end_time_prev = end_time
                
                x_j.append(x_j_k)
            
            X.append(x_j)

                


        for out_key in out_j:
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

    return X, Y

X, Y = flowPatternExtraction(in_batch, out_batch)

print(len(X[1]))


def dist_mutual_info():
    # TODO: Implement Mutual Information distance function
    pass


def dist_fsb_matched_filter():
    # TODO: Implement Frequency-Spectrum-Based matched filter distance function
    pass


def distanceFunctionSelection():
    # TODO: Implement Distance Function Selection
    pass


def flowCorrelationAttack():
    # TODO: Implement Attack
    pass

"""
Create stats and graphs for the Flow-Corellation Attack
"""
import sys
sys.path.insert(1, 'MixTypes')

import Timed
import Threshold
import ThresholdOrTimed
import ThresholdandTimed
import ThresholdPool
import TimedDynamicPool
import TimedPool

import attack
import matplotlib as mpl
import matplotlib.pyplot as plt
from tqdm import tqdm

# import warnings
# warnings.filterwarnings("ignore")

# res = input("Select type of mix: A for Timed | B for Threshold\n").upper()

def run_stats(min_mess, max_mess, n_nodes, time_window, threshold, fixed_prob, f, p, dist_func):

    step = int((max_mess - min_mess) / 15)
    if step < 2:
        print("Margins too narrow, unable to launch attack. Exiting...\n")
        return

    n_messages = [i for i in range(min_mess, max_mess, step)]
    print(n_messages)
        
    n_nodes = 20
    time_window = 5
    threshold = 10
    fixed_prob = 0.1
    f = 5
    p = 0.5

    dist_func = "tou_mike"

    accs = [[], [], [], [], [], [], []]
    accs_threshold = []

    for n_mess in tqdm(n_messages):
        random_time = 2 * n_mess
        # Timed
        Timed.mix(n_mess, n_nodes, random_time, time_window,fixed_prob)
        res = attack.attack(dist_func, time_window)
        accs[0].append(res)
        
        # Threshold
        Threshold.mix(n_mess, n_nodes, random_time, threshold, fixed_prob)
        res = attack.attack(dist_func, time_window)
        accs[1].append(res)

        # TimedPool
        TimedPool.mix(n_mess, n_nodes, random_time, threshold, fixed_prob, f, time_window)
        res = attack.attack(dist_func, time_window)
        accs[2].append(res)    

        # TimedDynamicPool
        TimedDynamicPool.mix(n_mess, n_nodes, random_time, threshold, fixed_prob, f, time_window, p)
        res = attack.attack(dist_func, time_window)
        accs[3].append(res)    
        
        # ThresholdOrTimed
        ThresholdOrTimed.mix(n_mess, n_nodes, random_time, time_window, fixed_prob, threshold)
        res = attack.attack(dist_func, time_window)
        accs[4].append(res)    
        
        # ThresholdandTimed
        ThresholdandTimed.mix(n_mess, n_nodes, random_time, threshold, fixed_prob, time_window)
        res = attack.attack(dist_func, time_window)
        accs[5].append(res)    
        
        # ThresholdPool
        ThresholdPool.mix(n_mess, n_nodes, random_time, threshold, fixed_prob, f)
        res = attack.attack(dist_func, time_window)
        accs[6].append(res)    

    # threshold
    # plt.plot(n_messages, accs[0], label='timed', marker='o')
    plt.plot(n_messages, accs[1], label='threshold', marker='o')
    plt.plot(n_messages, accs[2], label='timedpool', marker='o')
    plt.plot(n_messages, accs[3], label='TimedDynamicPool', marker='o')
    plt.plot(n_messages, accs[4], label='ThresholdOrTimed', marker='o')
    plt.plot(n_messages, accs[5], label='ThresholdandTimed', marker='o')
    plt.plot(n_messages, accs[6], label='ThresholdPool', marker='o')

    plt.xlabel("Sample Size (Packets)", fontsize=15)
    plt.ylabel("Detection Rate", fontsize=15)
    plt.legend()
    plt.show()